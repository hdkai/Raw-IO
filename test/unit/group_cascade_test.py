# 
#   Rio
#   Copyright (c) 2021 Homedeck, LLC.
#

from cv2 import drawMatches
from imageio import imwrite
from numpy import asarray
from pathlib import Path
from PIL import Image
from pytest import fixture, mark

from rio.grouping import group_exposures, timestamp_similarity, wavelet_similarity

@fixture
def similarity_fn ():
    timestamp_fn = timestamp_similarity()
    wavelet_fn = wavelet_similarity(hamming_threshold=0.16)
    def fn (path_a, path_b):
        if timestamp_fn(path_a, path_b):
            return True
        if wavelet_fn(path_a, path_b):
            return True
        return False
    return fn

def test_group_cascade_ambient_a (similarity_fn): # fails, on brightest exposure
    exposure_paths = [
        "test/media/group/6.jpg",
        "test/media/group/7.jpg",
        "test/media/group/8.jpg",
        "test/media/group/9.jpg",
        "test/media/group/10.jpg",
    ]
    groups = group_exposures(exposure_paths, similarity_fn)
    assert len(groups) == 1 and len(groups[0]) == 5

def test_group_cascade_ambient_b (similarity_fn):
    exposure_paths = [
        "test/media/group/14.jpg",
        "test/media/group/15.jpg",
        "test/media/group/16.jpg",
    ]
    groups = group_exposures(exposure_paths, similarity_fn)
    assert len(groups) == 1 and len(groups[0]) == 3

def test_group_cascade_flash_a (similarity_fn):
    exposure_paths = [
        "test/media/group/1.jpg",
        "test/media/group/2.jpg",
        "test/media/group/3.jpg",
        "test/media/group/4.jpg",
        "test/media/group/5.jpg",
    ]
    groups = group_exposures(exposure_paths, similarity_fn)
    assert len(groups) == 1 and len(groups[0]) == 5

def test_group_cascade_flash_b (similarity_fn):
    exposure_paths = [
        "test/media/group/17.jpg",
        "test/media/group/18.jpg",
    ]
    groups = group_exposures(exposure_paths, similarity_fn)
    assert len(groups) == 1 and len(groups[0]) == 2

def test_group_cascade_flash_c (similarity_fn): # fails, between dark and flash exposures
    exposure_paths = [
        "test/media/group/11.jpg",
        "test/media/group/12.jpg",
        "test/media/group/13.jpg",
    ]
    groups = group_exposures(exposure_paths, similarity_fn)
    assert len(groups) == 1 and len(groups[0]) == 3

def test_group_cascade_aerial (similarity_fn):
    exposure_paths = [
        "test/media/group/19.jpg",
        "test/media/group/20.jpg",
        "test/media/group/21.jpg",
        "test/media/group/22.jpg",
        "test/media/group/23.jpg",
        "test/media/group/24.jpg",
    ]
    groups = group_exposures(exposure_paths, similarity_fn)
    assert len(groups) == 2 and all([len(group) == 3 for group in groups])

def test_group_cascade_full_shoot (similarity_fn):
    #exposure_paths = [str(path) for path in (Path.home() / "Desktop" / "Margaret" / "brackets").glob("*.jpg")]
    exposure_paths = [str(path) for path in (Path.home() / "Downloads").glob("*.jpg")]
    groups = group_exposures(exposure_paths, similarity_fn)
    print(len(groups))