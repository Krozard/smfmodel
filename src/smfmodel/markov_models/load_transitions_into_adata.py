# load_transitions_into_adata

def load_transitions_into_adata(transition_matrix_solutions, transition_names, condition):
    """
    Loads a list of transition matrices into an AnnData object.
    
    Parameters:
        transition_matrix_solutions (list): A list of ndarrays.
        transition_names (list): A list of strings corresponding to the transition names.
        condition (str): The condition metadata id
        
    Returns:
        adata (AnnData): An anndata object
        
    """
    import numpy as np
    import anndata as ad
    
    transitions_list = []
    
    for matrix in transition_matrix_solutions:
        h = np.hstack(matrix) # Flatten the matrix
        transitions_list.append(h) # Add to the transition list
        
    transitions_matrix = np.array(transitions_list) # Turn the transtion list into an ndarray
    adata = ad.AnnData(transitions_matrix) # Build an AnnData around the ndarray
    adata.var_names = transition_names # Give names to the transitions
    adata.obs['condition'] = [condition] * adata.shape[0] # Add metadata
    adata.obs['condition'] = adata.obs['condition'].astype('category')
    
    return adata