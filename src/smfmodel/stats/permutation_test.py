# permutation_test

# Assume condition_1 and condition_2 are arrays of shape (n_samples, n_classes)
def permutation_test(condition_1, condition_2, apply_clr_transform=False, n_permutations=1000):
    """
    Perform a permutation test to compare two sets of proportions (arrays) and 
    determine if the difference in their centroids is statistically significant.

    Parameters:
    condition_1 (np.ndarray)
        A 2D array of shape (n_samples, n_classes) representing the first condition,
        where each row is an observation of class proportions that sum to 1.
    condition_2 (np.ndarray)
        A 2D array of shape (n_samples, n_classes) representing the second condition,
        where each row is an observation of class proportions that sum to 1.
    apply_clr_transform (bool)
        Whether to apply CLR transformation to the data. Generally used on compositional data.
    n_permutations (int)
        The number of permutations to perform. This determines the size of the null
        distribution used for the test.

    Returns:
        observed_distance (float)
            The Euclidean distance between the centroids (mean proportion vectors) of 
            the two conditions.
        p_value (float)
            The proportion of permutations where the distance between randomly permuted 
            centroids is greater than or equal to the observed distance. This is the 
            estimated p-value of the test.
    
    Notes:
    - This is a non-parametric test that does not assume any specific distribution for 
      the data. It tests whether the difference in the means (centroids) of the two 
      conditions is greater than expected by chance.
    """
    import numpy as np
    from scipy.spatial.distance import euclidean
    from sklearn.utils import resample
    from tqdm import tqdm

    if apply_clr_transform:
        from .clr_transform import clr_transform
        # Apply CLR transformation to both conditions
        condition_1 = clr_transform(condition_1)
        condition_2 = clr_transform(condition_2)

    # Calculate the original (observed) centroids for both conditions
    centroid_1 = np.mean(condition_1, axis=0)
    centroid_2 = np.mean(condition_2, axis=0)
    
    # Compute the Euclidean distance between the two centroids
    observed_distance = euclidean(centroid_1, centroid_2)

    # Combine the data from both conditions into one dataset
    combined_data = np.vstack([condition_1, condition_2])
    
    # Store the number of samples in the first condition
    n_1 = len(condition_1)

    # Initialize an empty list to store distances from permuted data
    permuted_distances = []
    
    # Perform permutation test by shuffling data and calculating distances
    with tqdm(total=n_permutations, desc=f"Permutation {n_permutations}") as pbar:
        for _ in range(int(n_permutations)):
            # Randomly shuffle the combined data
            permuted_data = resample(combined_data)
            
            # Split the permuted data into two new conditions
            new_cond_1 = permuted_data[:n_1]  # First 'n_1' samples
            new_cond_2 = permuted_data[n_1:]  # Remaining samples
            
            # Calculate the centroids for the permuted data
            permuted_centroid_1 = np.mean(new_cond_1, axis=0)
            permuted_centroid_2 = np.mean(new_cond_2, axis=0)
            
            # Calculate the distance between the new centroids and store it
            permuted_distances.append(euclidean(permuted_centroid_1, permuted_centroid_2))

            pbar.update(1)  # Update progress bar for each permutation

    # Convert the list of permuted distances to a NumPy array for easier comparison
    permuted_distances = np.array(permuted_distances)
    
    # Calculate the p-value: the proportion of permuted distances greater than or 
    # equal to the observed distance
    p_value = np.mean(permuted_distances >= observed_distance)
    
    return observed_distance, p_value
