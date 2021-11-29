# 
#   RawIO
#   Copyright (c) 2021 Yusuf Olokoba.
#

from PIL import Image
from pytest import fixture, mark

from rawio.align import align_verticals, align_level

IMAGE_PATHS = [
    "test/media/level/3.jpg",
    "test/media/level/9.jpg",
    "test/media/level/16.jpg",
    "test/media/level/53.jpg",
    "test/media/level/69.jpg",
    "test/media/level/71.jpg",
    "test/media/level/81.jpg",
    "test/media/level/93.jpg",
    "test/media/level/98.jpg",
]

@mark.parametrize("image_path", IMAGE_PATHS)
def test_straighten_image (image_path):
    image = Image.open(image_path)
    result = align_level(image)
    result = align_verticals(result, constrain_crop=False)
    result.save(f"straight.jpg")