# manova

def check_zero_variance(df):
    """Check for columns with zero variance and remove them."""
    import pandas as pd
    zero_variance_columns = df.loc[:, df.var() == 0].columns
    if len(zero_variance_columns) > 0:
        print(f"Removing columns with zero variance: {zero_variance_columns.tolist()}")
        df = df.drop(columns=zero_variance_columns)
    return df

def prepare_manova_data(condition_1, condition_2, variables):
    """
    Prepare data for MANOVA from two experimental conditions.

    Parameters:
    -----------
    condition_1 : np.ndarray
        A 2D array of shape (n_samples, n_classes) representing the first condition,
        where each row is an observation of class proportions.
    condition_2 : np.ndarray
        A 2D array of shape (n_samples, n_classes) representing the second condition,
        where each row is an observation of class proportions.

    Returns:
    --------
    df : pd.DataFrame
        A pandas DataFrame with the combined data from both conditions, where each 
        column represents a class and the 'Condition' column represents the group (1 or 2).
    """
    import numpy as np
    import pandas as pd
    # Create labels for the two conditions
    n_samples_1 = condition_1.shape[0]
    n_samples_2 = condition_2.shape[0]

    # Stack both conditions together
    data = np.vstack([condition_1, condition_2])

    # Create a grouping variable ('Condition')
    condition_labels = np.array([1] * n_samples_1 + [2] * n_samples_2)

    # Convert to DataFrame, with columns for each class and the condition label
    df = pd.DataFrame(data, columns=[f'Class_{i}' for i in variables])
    df['Condition'] = condition_labels

    # Check and remove zero variance columns
    df = check_zero_variance(df)

    return df

def manova_test(condition_1, condition_2, variables):
    """
    Perform MANOVA to compare class proportions between two conditions.

    Parameters:
    -----------
    condition_1 : np.ndarray
        A 2D array of shape (n_samples, n_classes) representing the first condition,
        where each row is an observation of class proportions.
    condition_2 : np.ndarray
        A 2D array of shape (n_samples, n_classes) representing the second condition,
        where each row is an observation of class proportions.

    Returns:
    --------
    result : MANOVA object
        The MANOVA result object from statsmodels, containing test statistics.
    """
    import numpy as np
    import pandas as pd
    from statsmodels.multivariate.manova import MANOVA
    # Prepare data
    df = prepare_manova_data(condition_1, condition_2, variables)
    
    # Adjust the formula based on the remaining columns in the DataFrame
    class_columns = df.columns.difference(['Condition'])
    formula = ' + '.join(class_columns) + ' ~ Condition'
    # Perform MANOVA using statsmodels
    maov = MANOVA.from_formula(formula, data=df)
    result = maov.mv_test()

    return result

def perform_anovas(condition_1, condition_2, variables):
    """
    Perform one-way ANOVA for each dependent variable (class proportions).

    Parameters:
    -----------
    df : pd.DataFrame
        A pandas DataFrame containing the class proportions and the Condition column.

    Returns:
    --------
    anova_results : dict
        A dictionary with each class as the key and its corresponding ANOVA results.
    """
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    anova_results = {}
    df = prepare_manova_data(condition_1, condition_2, variables)
    # Iterate over each class column (dependent variable)
    for class_column in df.columns.difference(['Condition']):
        # Build the formula for the univariate ANOVA
        formula = f'{class_column} ~ Condition'
        
        # Fit the model using ordinary least squares (OLS)
        model = ols(formula, data=df).fit()
        
        # Perform the ANOVA
        anova_table = sm.stats.anova_lm(model, typ=2)
        
        # Store the result for each class
        anova_results[class_column] = anova_table
    
    return anova_results

def apply_bonferroni_correction(anova_results):
    """
    Apply Bonferroni correction to the p-values from the ANOVAs.

    Parameters:
    -----------
    anova_results : dict
        A dictionary of ANOVA results for each class.

    Returns:
    --------
    corrected_pvals : dict
        A dictionary with the Bonferroni-corrected p-values for each class.
    """
    from statsmodels.stats.multitest import multipletests

    pvals = [result['PR(>F)'][0] for result in anova_results.values()]
    
    # Apply Bonferroni correction
    corrected_pvals = multipletests(pvals, method='bonferroni')[1]
    
    # Return a dictionary with class names and corrected p-values
    return {class_name: corrected_pval for class_name, corrected_pval in zip(anova_results.keys(), corrected_pvals)}
