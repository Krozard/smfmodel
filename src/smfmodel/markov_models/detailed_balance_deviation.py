# detailed_balance_deviation
import numpy as np
from .solve_steady_state import solve_steady_state

def detailed_balance_deviation(transition_matrix):
    """
    Calculate how far the transition matrix is from satisfying detailed balance.

    Parameters:
        transition_matrix (np.ndarray): The transition matrix to check.

    Returns:
        deviation (np.ndarray): Deviation from detailed balance
    """
    steady_state = solve_steady_state(transition_matrix)

    deviation = steady_state[0] * transition_matrix[0, 1] - steady_state[1] * transition_matrix[1, 0]

    return deviation