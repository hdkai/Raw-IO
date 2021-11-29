# 
#   RawIO
#   Copyright (c) 2021 Yusuf Olokoba.
#

from PIL import Image
from pytest import fixture, mark
from torchvision.transforms.functional import to_tensor, to_pil_image

from rawio.lens import tca_model, tca_grid, tca_correction

IMAGE_PATHS = [
    "test/media/tca/1.jpg",
    "test/media/tca/2.jpg",
]

@mark.parametrize("image_path", IMAGE_PATHS)
def test_tca (image_path):
    image = Image.open(image_path)
    model = tca_model(image)
    grid = tca_grid(model, image.width, image.height)
    result = tca_correction(to_tensor(image).unsqueeze(dim=0), grid)
    result = to_pil_image(result.squeeze(dim=0))
    result.save(f"tca.jpg")