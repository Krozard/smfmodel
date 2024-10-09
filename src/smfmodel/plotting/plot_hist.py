# plot_hist

def plot_hist(data_arrays, params):
    """
    Plots an overlaid histogram and rolling average for a list of data arrays.
    
    Parameters:
        data_arrays (list): list of data arrays
        params (dict): Dictionary of plotting params
            
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import pandas as pd

    n_bins = params['n_bins']
    window_size = params['window_size']
    show_bars = params['show_bars']
    show_roll = params['show_roll']
    color_palette = params['color_palette']
    labels = params['labels']
    save = params['save']
    show_mean = params['show_mean']
    show_cdf = params['show_cdf']
    
    # Set up color palette
    palette = sns.color_palette(color_palette, len(data_arrays))  # Using seaborn for a color palette
    
    # Init figure
    plt.figure(figsize=(10, 6))
    
    # Get max and min values in the datasets
    min_data = np.inf
    max_data = -np.inf
    for array in data_arrays:
        if min(array) < min_data:
            min_data = min(array)
        if max(array) > max_data:
            max_data = max(array)
    
    # Loop through each data array
    for i, data in enumerate(data_arrays):
        # Generate histogram data
        counts, bins = np.histogram(data, bins=n_bins)

        # Calculate the center of the bins for plotting
        bin_centers = (bins[:-1] + bins[1:]) / 2

        # Convert counts to a pandas Series for rolling average calculation
        counts_series = pd.Series(counts)

        # Compute rolling average
        rolling_average = counts_series.rolling(window=window_size, center=True).mean()

        if show_bars:
            # Plot the histogram
            plt.bar(bin_centers, counts, width=np.diff(bins), color=palette[i], edgecolor='black', alpha=0.1)

        if show_roll:
            # Plot the rolling average
            plt.plot(bin_centers, rolling_average, color=palette[i], linewidth=2, label=labels[i])  
            
        if show_mean:
            mean_value = np.mean(data)
            max_height = np.max(counts)
            plt.axvline(mean_value, color=palette[i], linestyle='dashed', linewidth=1)
            plt.text(mean_value + mean_value/4, max_height/2, f'Mean: {mean_value:.4f}', color=palette[i])
            
        if show_cdf:
            from scipy.stats import gaussian_kde
            # Create a kernel density estimate (KDE) for PDF
            kde = gaussian_kde(data)
            x = np.linspace(min_data, max_data, 1000)
            pdf = kde(x)  # PDF values
            # Compute the CDF
            cdf = np.cumsum(pdf) * (x[1] - x[0]) 
            # Find the maximum value of the CDF
            max_cdf = np.max(cdf)
            # Calculate the threshold (half of the maximum CDF)
            threshold = max_cdf / 2
            # Find the x value where the PDF first crosses the threshold
            cross_index = np.where(cdf > threshold)[0][0]  # Index where PDF drops below the threshold
            value_at_half_max = x[cross_index]
            plt.plot(x, cdf, color=palette[i], linewidth=2, label=f'CDF {labels[i]}')
            plt.axvline(value_at_half_max, color=palette[i], linestyle='dashed', linewidth=1, label=f'Half-Max: {value_at_half_max:.4f}')
            
    # Add labels and legend
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histograms with Rolling Averages')
    plt.legend()
    ax = plt.gca()
    # Remove the right and upper spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    if save:
        pass
    else:
        plt.show()