#generate_transition_matrix_solutions

def generate_transition_matrix_solutions(observed_proportions, variance_threshold, condition, params):
    """
    Generates transition matrices for given observed proportions and variance thresholds.

    Parameters:
        observed_proportions (np.ndarray): The observed steady-state proportions.
        variance_threshold (np.ndarray): Threshold of variance to determine success.
        condition (str): String to give the tqdm progress context.
        params (dict): Map of addtional parameters to pass.

    Returns:
        transition_matrix_solutions (list): List of successful transition matrices.
    """
    from tqdm import tqdm
    import numpy as np
    from .random_transition_matrix import random_transition_matrix
    from .solve_steady_state import solve_steady_state

    total_matrices = params['total_matrices']
    size = params['size']
    allow_self_transitions = params['allow_self_transitions']
    constrain_transitions_to_adjacent = params['constrain_transitions_to_adjacent']

    transition_matrix_solutions = []
    generated_matrices = 0
    
    with tqdm(total=total_matrices, desc=f"Generating {total_matrices} matrices for {condition}") as pbar:
        while generated_matrices < total_matrices:
            T = random_transition_matrix(size=size, allow_self_transitions=allow_self_transitions, constrain_transitions_to_adjacent=constrain_transitions_to_adjacent)  # Generate a random transition matrix
            steady_state = solve_steady_state(T)  # Calculate steady-state proportions
            abs_delta = np.abs(steady_state - observed_proportions) # Get the difference between the observed proportions and the T-steady state
            variance_test = variance_threshold - abs_delta # Substract the difference from the variance threshold
            T_steady_state_within_threshold = np.all(variance_test > 0) # If the solution is within threshold, variable is True
            
            if T_steady_state_within_threshold:
                transition_matrix_solutions.append(T)
                generated_matrices += 1
                pbar.set_postfix({'Matrices generated': generated_matrices})
                pbar.update(1)  # Update progress bar for each successful matrix generation
    
    return transition_matrix_solutions