# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from typing import Callable, List

from .timestamp import exposure_timestamp

def group_exposures (exposure_paths: List[str], similarity_fn: Callable[[Image.Image, Image.Image], bool], workers: int=8) -> List[List[str]]: # INCOMPLETE # Threading
    """
    Group a set of exposures using a similarity function.

    Parameters:
        exposure_paths (list): Paths to exposures to group.
        similarity_fn (callable): Pairwise similarity function returning a boolean.
        workers (int): Number of workers for IO.
    
    Returns:
        list: Groups of exposure paths.
    """
    # Check
    if not exposure_paths:
        return []
    # Trivial case
    if len(exposure_paths) == 1:
        return [exposure_paths]
    
    # # Load all exposures into memory
    # with ThreadPoolExecutor(max_workers=workers) as executor:
    #     # Sort by timestamp
    #     exposures = executor.map(lambda path: Image.open(path), exposure_paths)
    #     exposures_with_paths = zip(exposure_paths, exposures)
    #     exposures_with_paths = sorted(exposures_with_paths, key=lambda pair: exposure_timestamp(pair[1]))
    #     exposure_paths, exposures = list(zip(*exposures_with_paths))
    #     # Compute pairwise similarity
    #     pairwise_similarities = executor.map(lambda pair: similarity_fn(*pair), [(exposures[i], exposures[i+1]) for i in range(len(exposures) - 1)])
    #     pairwise_similarities = list(pairwise_similarities) # So we can see it when debugging
    # # Group
    # groups = []
    # current_group = [exposure_paths[0]]
    # for i, similar in enumerate(pairwise_similarities):
    #     if not similar:
    #         groups.append(current_group)
    #         current_group = []
    #     current_group.append(exposure_paths[i+1])
    # groups.append(current_group)

    # Load exposures
    exposures = [Image.open(path) for path in exposure_paths]
    exposures_with_paths = zip(exposure_paths, exposures)
    exposures_with_paths = sorted(exposures_with_paths, key=lambda pair: exposure_timestamp(pair[1]))
    # Group
    current_path, current_exposure = exposures_with_paths.pop(0)
    groups = []
    current_group = [current_path]
    while exposures_with_paths:
        path, exposure = exposures_with_paths.pop(0)
        if not similarity_fn(current_exposure, exposure):
            groups.append(current_group)
            current_group = []
        current_group.append(path)
        current_path, current_exposure = path, exposure
    groups.append(current_group)

    return groups