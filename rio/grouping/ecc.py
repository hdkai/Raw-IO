# 
#   Rio
#   Copyright (c) 2020 Homedeck, LLC.
#

from typing import Callable

def ecc_similarity (trials: int=100) -> Callable[[str, str], bool]:
    """
    Create a similarity function which uses the technique described in Evangelidis & Psarakis.

    Parameters:
        trials (int): Number of Monte Carlo trials for estimating the binomial distribution.

    Returns:
        callable: Pairwise similarity function returning a boolean.
    """
    pass