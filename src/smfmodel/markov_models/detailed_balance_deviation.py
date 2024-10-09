# detailed_balance_deviation
import numpy as np
from .solve_steady_state import solve_steady_state

def detailed_balance_deviation(transition_matrix):
    """
    Calculate how far the transition matrix is from satisfying detailed balance.

    Parameters:
        transition_matrix (np.ndarray): The transition matrix to check.

    Returns:
        deviations (np.ndarray): A matrix of deviations for each pair of states.
        sum_deviations (float): The sum of all deviations in the deviation matrix.
        max_deviation (float): The maximum deviation.
        mean_deviation (float): The mean deviation.
    """
    steady_state = solve_steady_state(transition_matrix)
    n = len(steady_state)
    deviations = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            deviations[i, j] = steady_state[i] * transition_matrix[i, j] - steady_state[j] * transition_matrix[j, i]
    
    max_deviation = np.max(np.abs(deviations))
    mean_deviation = np.mean(np.abs(deviations))
    sum_deviations = np.sum(deviations)

    return deviations, sum_deviations, max_deviation, mean_deviation