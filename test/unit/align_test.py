# 
#   RawIO
#   Copyright (c) 2021 Yusuf Olokoba.
#

from PIL import Image
from rawio.align import align_exposures

def test_align ():
    exposure_paths = [
        "test/media/align/1.jpg",
        "test/media/align/2.jpg",
        "test/media/align/3.jpg",
        "test/media/align/4.jpg",
        "test/media/align/5.jpg",
        "test/media/align/6.jpg",
    ]
    exposures = [Image.open(path) for path in exposure_paths]
    results = align_exposures(exposures)
    [exposure.save(f"{i}.jpg") for i, exposure in enumerate(results)]

def test_align_rotation ():
    exposure_paths = [
        "test/media/align_rotation/1.jpg",
        "test/media/align_rotation/2.jpg",
        "test/media/align_rotation/3.jpg",
        "test/media/align_rotation/4.jpg",
        "test/media/align_rotation/5.jpg",
    ]
    exposures = [Image.open(path) for path in exposure_paths]
    results = align_exposures(exposures)
    [exposure.save(f"{i}.jpg") for i, exposure in enumerate(results)]