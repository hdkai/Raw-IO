# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from cv2 import createAlignMTB
from numpy import asarray
from PIL import Image
from typing import List

def align_exposures_mtb (exposures: List[Image.Image]) -> List[Image.Image]:
    """
    Align exposures using Media Threshold Bitmap alignment.

    Parameters:
        exposures (list): List of PIL.Image exposures.

    Returns:
        list: List of aligned PIL.Image exposures.
    """
    # Check
    if not exposures:
        return None
    # Check
    if len(exposures) == 1:
        return exposures[0]
    # Convert
    exifs = [exposure.info.get("exif") for exposure in exposures]
    exposure_arrays = [asarray(exposure) for exposure in exposures]
    # Align
    createAlignMTB().process(exposure_arrays, exposure_arrays)
    # Convert
    exposures = [Image.fromarray(exposure) for exposure in exposure_arrays]
    for exposure, exif in zip(exposures, exifs):
        exposure.info["exif"] = exif
    return exposures

def align_exposures_ecc (exposures: List[Image.Image]) -> List[Image.Image]: # INCOMPLETE # Use affine model
    """
    Align exposures using Evangelidis & Psarakis.

    Parameters:
        exposures (list): List of PIL.Image exposures.

    Returns:
        list: List of aligned PIL.Image exposures.
    """
    pass