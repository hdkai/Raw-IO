# 
#   Rio
#   Copyright (c) 2021 Homedeck, LLC.
#

from cv2 import getPerspectiveTransform, getRotationMatrix2D, transform, warpPerspective
from lsd import line_segment_detector
from numpy import abs, array, asarray, arctan2, float32, pi, rad2deg, zeros_like
from PIL import Image
from sklearn.linear_model import RANSACRegressor

def align_verticals (image: Image.Image, max_trials: int=2000) -> Image.Image: # INCOMPLETE # Threshold # Constrain crop
    """
    Straighten verticals in an image.

    It is highly recommended to level the image before straightening.

    Parameters:
        image (PIL.Image): Input image.
        max_trials (int): Maximum trials for fitting geometry model.

    Returns:
        PIL.Image: Result image.
    """
    # Extract lines
    scale = 1200. / image.width
    min_length = image.width * 0.05
    image_arr = asarray(image)
    lines = line_segment_detector(image_arr, scale=scale, angle_tolerance=18.)
    lines = lines[lines[:,6] > min_length,:4]
    # Get vertical lines
    MAX_ANGLE = 12.
    lines_t = rad2deg(arctan2(lines[:,3] - lines[:,1], lines[:,2] - lines[:,0]) % pi) - 90.
    vertical_mask = abs(lines_t) < MAX_ANGLE
    # Get line intersection points with image midpoint
    mid_line = array([ 0., image.height / 2., image.width, image.height / 2. ])[None,:]
    d_a = lines[:,2:4] - lines[:,0:2]
    d_b = mid_line[:,2:4] - mid_line[:,0:2]
    d_p = lines[:,0:2] - mid_line[:,0:2]
    d_a_perp = zeros_like(d_a)
    d_a_perp[:,0] = -d_a[:,1]
    d_a_perp[:,1] = d_a[:,0]
    projection = (d_a_perp * d_p).sum(axis=1) / (d_a_perp * d_b).sum(axis=1)
    intersection = projection[:,None] * d_b + mid_line[:,0:2]
    lines_x = 2. * intersection[:,0] / image.width - 1.
    # Apply vertical mask
    lines = lines[vertical_mask]
    lines_x = lines_x[vertical_mask]
    lines_t = lines_t[vertical_mask]
    # Regress with RANSAC
    ransac = RANSACRegressor(max_trials=max_trials, random_state=0) # We need to suppress stochasticity
    try:
        ransac.fit(lines_x.reshape(-1, 1), lines_t)
    except ValueError:
        print("Failed to fit lines to level image")
        return image
    # Filter converging
    lines = lines[ransac.inlier_mask_]
    lines_x = lines_x[ransac.inlier_mask_]
    lines_t = lines_t[ransac.inlier_mask_]
    # Rotate anchors about their centers
    left_anchor = lines[lines_x.argmin()]       # leftmost line
    right_anchor = lines[lines_x.argmax()]      # rightmost line
    left_theta = lines_t[lines_x.argmin()]
    right_theta = lines_t[lines_x.argmax()]
    left_anchor_center = 0.5 * (left_anchor[:2] + left_anchor[2:])
    right_anchor_center = 0.5 * (right_anchor[:2] + right_anchor[2:])
    M_left = getRotationMatrix2D(tuple(left_anchor_center), left_theta, 1.)
    M_right = getRotationMatrix2D(tuple(right_anchor_center), right_theta, 1.)
    upright_left = transform(left_anchor.reshape(2, 2)[None,:], M_left)[0]       # (2,2)
    upright_right = transform(right_anchor.reshape(2, 2)[None,:], M_right)[0]    # (2,2)
    # Compute homography
    src_rect = array([ left_anchor[:2], left_anchor[2:], right_anchor[:2], right_anchor[2:] ], dtype=float32)
    dst_rect = array([ upright_left[0], upright_left[1], upright_right[0], upright_right[1] ], dtype=float32)
    H = getPerspectiveTransform(src_rect, dst_rect)
    # Warp and constrain crop # INCOMPLETE
    result = warpPerspective(image_arr, H, (image.width, image.height))

    # Return
    result = Image.fromarray(result)
    result.info["exif"] = image.info.get("exif")
    return result