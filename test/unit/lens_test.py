# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from PIL import Image
from pytest import fixture, mark

from rio.corrections import lens_correction

def test_lens_correction ():
    image_path = "test/media/lens/1.jpg"
    image = Image.open(image_path)
    result = lens_correction(image)
    result.save(f"lens.jpg")
    assert result.getexif() is not None

def test_lens_correction_no_exif ():
    image_path = "test/media/lens/1.jpg"
    image = Image.open(image_path)
    result = lens_correction(image)
    result.save(f"lens.jpg")