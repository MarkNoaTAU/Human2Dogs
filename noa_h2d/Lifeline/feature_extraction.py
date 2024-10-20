import numpy as np
import pandas as pd

def sample_shannon_diversity(relative_abundance):
    """
        Shannon diversity calculate: given pi is the vector of relative abundance of speices i in the sample then the sample shannon diversity index is the entopy aka:
        - \sum_i pi*ln(pi)
    """
    if type(relative_abundance) != pd.Series:
        raise ValueError("Input should be pd.Series, a sample")
    if not ((relative_abundance >= 0).all() & (relative_abundance.sum() <=1)):
        raise ValueError("Sample shannon diversity expect the data to be relative abundance.")
    return -(relative_abundance * relative_abundance.apply(lambda x: np.log(x) if x != 0 else 0)).sum()


def sample_richness(relative_abundance):
    """ number of non-zero taxa """
    return (relative_abundance != 0).sum()


