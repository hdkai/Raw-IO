# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from cv2 import createMergeMertens
from numpy import asarray, clip, uint8
from PIL import Image
from typing import List

def exposure_fusion (exposures: List[Image.Image]) -> Image.Image:
    """
    Blend exposures using Exposure Fusion (Mertens et al.).

    Parameters:
        exposures (list): List of PIL.Image exposures.

    Returns:
        PIL.Image: Blended image.
    """
    # Check
    if not exposures:
        return None
    # Check
    if len(exposures) == 1:
        return exposures[0]
    # Convert
    metadata = exposures[0].info.get("exif")
    exposure_arrays = [asarray(exposure) for exposure in exposures]
    # Fuse
    fusion = createMergeMertens().process(exposure_arrays)
    fusion = clip(fusion * 255., 0., 255.).astype(uint8)
    # Convert
    result = Image.fromarray(fusion)
    result.info["exif"] = metadata
    return result