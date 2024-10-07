# plot_2D_contour

def plot_2D_contour(adata, x_label, y_label, condition, params):
    """
    Plots a 2D contour plot from an input adata.
    
    Parameters:
        adata (AnnData): The AnnData object
        x_label (str): The x-axis category
        y_label (str): The y-axis category
        condition (str): The condition to plot
        params (dict): Dictionary of plotting parameters
        
    Returns:
        None
        
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    import anndata as ad

    subset = adata[adata.obs['condition'] == condition].copy()
    array1 = subset.X[:, subset.uns['Transition_array_state_map'][x_label]]
    array2 = subset.X[:, subset.uns['Transition_array_state_map'][y_label]]

    levels = params['levels']
    x_lower = params['x_lower']
    x_upper = params['x_upper']
    y_lower = params['y_lower']
    y_upper = params['y_upper']
    save_density_plot = params['save']

    plt.figure(figsize=(4, 4))
    sns.kdeplot(x=array1, y=array2, cmap='viridis', fill=False, thresh=0, levels=levels)

    title = f'{y_label} versus {x_label} for {condition} Allele'
    plt.title(title, pad=20)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_lower, x_upper)
    plt.ylim(y_lower, y_upper)
    ax = plt.gca()
    # Remove the right and upper spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    if save_density_plot:
        save_name = f'/{title} {y_label} vs {x_label}'
        plt.savefig(save_name, bbox_inches='tight', pad_inches=0.1)
        plt.close()
    else:
        plt.show()