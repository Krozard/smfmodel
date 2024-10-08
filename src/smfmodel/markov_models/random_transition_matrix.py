# random_transition_matrix
import numpy as np

def random_transition_matrix(size=4, allow_self_transitions=False, constrain_transitions_to_adjacent=True):
    """
    Creates a random kinetic transition matrix of given size with values between 0 and 1, 
    where the diagonal is zero (no self-transitions).

    Parameters:
        size (int):
        allow_self_transitions (bool):
        constrain_transitions_to_adjacent (bool):

    Returns:
        matrix (np.ndarray): A square transition matrix

    """

    # Create a random matrix of variable 'size' with values between 0 and 1
    matrix = np.random.rand(size, size)
    
    if not allow_self_transitions:
        # Set diagonal to zero (no self-transitions)
        np.fill_diagonal(matrix, 0)
    
    if constrain_transitions_to_adjacent:
        for i in range(size):
            for j in range(size):
                if np.abs(i-j) == 2:
                    matrix[i, j] = 0
                
    row_sums = matrix.sum(axis=1, keepdims=True)  # Calculate row sums
    matrix = matrix / row_sums  # Normalize rows to sum to 1
    
    return matrix