# check_detailed_balance

def check_detailed_balance(transition_matrix, threshold):
    """
    Check if the transition matrix satisfies the detailed balance condition.

    Parameters:
        transition_matrix (np.ndarray): The transition matrix to check.
        threshold (float): The deviation from detailed balance to threshold.

    Returns:
        bool: True if detailed balance holds, False otherwise.
    """
    from .solve_steady_state import solve_steady_state
    
    steady_state = solve_steady_state(transition_matrix)
    n = len(steady_state)

    for i in range(n):
        for j in range(n):
            deviation = (steady_state[i] * transition_matrix[i, j]) - (steady_state[j] * transition_matrix[j, i])
            if abs(deviation) > threshold:
                return False
    return True