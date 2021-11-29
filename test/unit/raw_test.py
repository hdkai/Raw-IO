# 
#   RawIO
#   Copyright (c) 2021 Yusuf Olokoba.
#

from pytest import fixture, mark

from rawio.raw import rawread

@mark.parametrize("image_path", [
    "test/media/raw/1.arw",
    "test/media/raw/2.arw",
    "test/media/raw/3.cr2",
    "test/media/raw/4.cr2",
])
def test_single_raw (image_path):
    image = rawread(image_path)
    image.save("raw.jpg")