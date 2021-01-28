# 
#   Rio
#   Copyright (c) 2021 Homedeck, LLC.
#

from PIL import Image
from pytest import fixture, mark
from torchvision.transforms.functional import to_tensor, to_pil_image

from rio.lens import lens_grid, lens_correction

def test_lens_correction ():
    image_path = "test/media/lens/1.jpg"
    image = Image.open(image_path)
    metadata = image.getexif()
    assert metadata, "Metadata must be present"
    grid = lens_grid(metadata, image.width, image.height)
    if grid is not None:
        result = lens_correction(to_tensor(image).unsqueeze(dim=0), grid)
        result = to_pil_image(result.squeeze(dim=0))
        result.save(f"lens.jpg")