# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from pathlib import Path
from PIL import Image
from pytest import fixture, mark

from rio.grouping import group_exposures, wavelet_similarity

def test_group_wavelet_ambient_a (): # fails, on brightest exposure
    exposure_paths = [
        "test/media/group/6.jpg",
        "test/media/group/7.jpg",
        "test/media/group/8.jpg",
        "test/media/group/9.jpg",
        "test/media/group/10.jpg",
    ]
    groups = group_exposures(exposure_paths, wavelet_similarity())
    assert len(groups) == 1 and len(groups[0]) == 5

def test_group_wavelet_ambient_b ():
    exposure_paths = [
        "test/media/group/14.jpg",
        "test/media/group/15.jpg",
        "test/media/group/16.jpg",
    ]
    groups = group_exposures(exposure_paths, wavelet_similarity())
    assert len(groups) == 1 and len(groups[0]) == 3

def test_group_wavelet_flash_a ():
    exposure_paths = [
        "test/media/group/1.jpg",
        "test/media/group/2.jpg",
        "test/media/group/3.jpg",
        "test/media/group/4.jpg",
        "test/media/group/5.jpg",
    ]
    groups = group_exposures(exposure_paths, wavelet_similarity())
    assert len(groups) == 1 and len(groups[0]) == 5

def test_group_wavelet_flash_b ():
    exposure_paths = [
        "test/media/group/17.jpg",
        "test/media/group/18.jpg",
    ]
    groups = group_exposures(exposure_paths, wavelet_similarity())
    assert len(groups) == 1 and len(groups[0]) == 2

def test_group_wavelet_flash_c (): # fails, between dark and flash exposures
    exposure_paths = [
        "test/media/group/11.jpg",
        "test/media/group/12.jpg",
        "test/media/group/13.jpg",
    ]
    groups = group_exposures(exposure_paths, wavelet_similarity())
    assert len(groups) == 1 and len(groups[0]) == 3

def test_group_wavelet_aerial ():
    exposure_paths = [
        "test/media/group/19.jpg",
        "test/media/group/20.jpg",
        "test/media/group/21.jpg",
        "test/media/group/22.jpg",
        "test/media/group/23.jpg",
        "test/media/group/24.jpg",
    ]
    groups = group_exposures(exposure_paths, wavelet_similarity())
    assert len(groups) == 2 and all([len(group) == 3 for group in groups])

def test_group_wavelet_full_shoot ():
    exposure_paths = [str(path) for path in (Path.home() / "Desktop" / "Margaret" / "brackets").glob("*.jpg")]
    groups = group_exposures(exposure_paths, wavelet_similarity(hamming_threshold=0.15))
    print(len(groups))

def test_similarity (): # 0.195
    path_a = "/Users/yusuf/Desktop/b/1.jpg"
    path_b = "/Users/yusuf/Desktop/b/2.jpg"
    similarity = wavelet_similarity()(path_a, path_b)
    print(similarity)