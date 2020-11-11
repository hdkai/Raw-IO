# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from cv2 import AlignMTB
from PIL import Image
from typing import List

def align_exposures (exposures: List[Image.Image]) -> List[Image.Image]: # INCOMPLETE
    """
    Align a set of exposures using Media Threshold Bitmap alignment.

    Parameters:
        exposures (list): List of PIL.Image exposures.

    Returns:
        list: List of aligned PIL.Image exposures.
    """
    pass