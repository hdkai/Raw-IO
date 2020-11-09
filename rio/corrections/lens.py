# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from lensfunpy import Database, Modifier
from numpy import ndarray
from PIL import Image
from torch import from_numpy, stack
from torch.nn.functional import grid_sample
from torchvision.transforms import ToPILImage, ToTensor

from ..device import get_io_device

def lens_correction (image: Image.Image) -> Image.Image:
    """
    Appply lens distortion correction on an image.

    This requires the images to have valid EXIF metadata tags.

    Parameters:
        images (PIL.Image): Input image.

    Returns:
        PIL.Image: Corrected image.
    """
    # Compute sample grid
    grid = _compute_sample_grid(image)
    if grid is None:
        return image
    # Save EXIF
    exif = image.info.get("exif")
    # Sample
    device = get_io_device()
    image_tensor = ToTensor()(image).unsqueeze(dim=0).to(device)
    grid = from_numpy(grid).unsqueeze(dim=0).to(device)
    result_tensor = grid_sample(image_tensor, grid, mode="bilinear", padding_mode="zeros", align_corners=False)
    # Convert
    result = ToPILImage()(result_tensor.squeeze(dim=0).cpu())
    result.info["exif"] = exif
    return result

def _compute_sample_grid (image: Image.Image) -> ndarray:
    """
    Create a modifier for the camera and lens used to capture a given image.
    This function relies on the image's EXIF metadata to function.

    Parameters:
        image (PIL.Image): Input image.
        
    Returns:
        Modifier: Modifier for the camera and lens, or `None` if there is insufficient metadata.
    """
    # EXIF tags
    CAMERA_MAKER_EXIF_TAG = 271
    CAMERA_MODEL_EXIF_TAG = 272
    LENS_MAKER_EXIF_TAG = 42035
    LENS_MODEL_EXIF_TAG = 42036
    FOCAL_LENGTH_EXIF_TAG = 37386
    F_NUMBER_EXIF_TAG = 33437
    # Get metadata
    metadata = image.getexif()
    camera_maker, camera_model = metadata.get(CAMERA_MAKER_EXIF_TAG), metadata.get(CAMERA_MODEL_EXIF_TAG)
    lens_maker, lens_model = metadata.get(LENS_MAKER_EXIF_TAG), metadata.get(LENS_MODEL_EXIF_TAG)
    # Check
    if not all([camera_maker, camera_model, lens_model]):
        return None
    # Find model
    database = Database()
    cameras = database.find_cameras(camera_maker, camera_model)
    if len(cameras) == 0:
        return None
    lenses = database.find_lenses(cameras[0], lens_maker, lens_model)
    if len(lenses) == 0:
        return None
    # Get focal length and f number
    focal_length = metadata.get(FOCAL_LENGTH_EXIF_TAG, 20)
    f_number = metadata.get(F_NUMBER_EXIF_TAG, 8)
    focal_length = focal_length[0] / focal_length[1] if isinstance(focal_length, tuple) else focal_length
    f_number = f_number[0] / f_number[1] if isinstance(f_number, tuple) else f_number
    # Create modifier
    modifier = Modifier(lenses[0], cameras[0].crop_factor, image.width, image.height)
    modifier.initialize(focal_length, f_number)
    # Compute sample grid
    sample_grid = modifier.apply_geometry_distortion() # (H,W,2)
    # Normalize
    sample_grid[:,:,0] = 2. * sample_grid[:,:,0] / image.width - 1.
    sample_grid[:,:,1] = 2. * sample_grid[:,:,1] / image.height - 1.
    return sample_grid