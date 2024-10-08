# solve_steady_state
import numpy as np

def solve_steady_state(T):
    """
    Calculate the steady state proportions from a transition matrix.

    Parameters:
        T (numpy.ndarray): Transition matrix (square matrix).

    Returns:
        numpy.ndarray: Steady state proportions (1D array).
    """
    
    # Number of states
    n = T.shape[0]

    # Create the augmented matrix by appending a row for the sum of proportions
    A = np.vstack((T.T - np.eye(n), np.ones(n)))
    b = np.zeros(n + 1)
    b[-1] = 1  # Sum of probabilities should equal 1

    # Solve the linear system A * x = b
    steady_state = np.linalg.lstsq(A, b, rcond=None)[0]

    return steady_state