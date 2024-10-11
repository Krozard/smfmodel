# clr_transform

def clr_transform(data):
    """
    Apply the Centered Log-Ratio (CLR) transformation to compositional data.

    Parameters:
    data (np.ndarray)
        A 2D array of shape (n_samples, n_classes) where each row is a compositional 
        vector that sums to 1.

    Returns:
    clr_data (np.ndarray)
        The CLR-transformed data of the same shape as input, where each row has been 
        log-ratio transformed.
    """
    import numpy as np
    # Geometric mean for each row
    geometric_mean = np.exp(np.mean(np.log(data), axis=1))
    # CLR transformation
    return np.log(data / geometric_mean[:, np.newaxis])
