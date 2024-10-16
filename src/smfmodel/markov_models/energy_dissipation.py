#energy_dissipation
import numpy as np
from .solve_steady_state import solve_steady_state

def energy_dissipation(transition_matrix):
    """
    Calculate the energy dissipation rate of a system at steady state given its transition matrix.

    Parameters:
        transition_matrix (np.ndarray): The transition matrix to check.

    Returns:
        dissipation_rate (float): The rate of energy dissipation.
    """
    steady_state = solve_steady_state(transition_matrix)
    n = len(steady_state)

    # the following line only works for single-cycle systems
    J = steady_state[0] * transition_matrix[0,1] - steady_state[1] * transition_matrix[1,0]

    rate_product_clockwise = 1
    rate_product_counter_clockwise = 1
    for i in range(n):
            if i == n-1:
                j = 0
            else:
                j = i + 1
            rate_product_clockwise *= transition_matrix[i, j]
            rate_product_counter_clockwise *= transition_matrix[j, i]
    dissipation_rate = J*np.log(rate_product_clockwise/rate_product_counter_clockwise)

    return dissipation_rate