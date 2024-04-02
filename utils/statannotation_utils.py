from statannotations.Annotator import Annotator
import seaborn as sns
import matplotlib.pyplot as plt

# Mapping from original sample names to more readable names for plotting
name_map = {
    'JUB66_RFP_0': 'JUb66(RFP)', 
    'JUB66_RFP_IN_CEMBIO_0': 'JUb66(RFP) in CeMbio', 
    'MK_JUB66_RFP_IN_JUB66_0': 'MK JUb66(RFP)',
    'OP50_RFP_0': 'OP50(RFP)', 
    'JUB66_RFP_ONTO_PA01_GFP_0': 'JUb66(RFP) swapped onto PA01(GFP)',
    'JUB66_RFP_ONTO_PA01_GFP_1': 'PA01(GFP) swapped from JUb66(RFP)', 
    'JUB66_RFP_ONTO_OP50_GFP_0': 'JUb66(RFP) swapped onto OP50(GFP)',
    'JUB66_RFP_ONTO_OP50_GFP_1': 'OP50(GFP) swapped from JUb66(RFP)',
    'JUB66_RFP_IN_CEMBIO_ONTO_PA01_GFP_0': 'JUb66(RFP) in CeMbio swapped onto PA01(GFP)',
    'JUB66_RFP_IN_CEMBIO_ONTO_PA01_GFP_1': 'PA01(GFP) swapped from CeMbio'
}

def significance_boxplot(df, x, y, order, pairs='all', orient='h'):
    """
    Creates boxplots with significance annotations using the statannotations package.

    Args:
    - df (pd.DataFrame): The data frame containing the data.
    - x (str): The name of the column to be used as the x-axis (categorical).
    - y (str): The name of the column to be used as the y-axis (numeric).
    - order (list): The order in which to display the x-axis categories.
    - pairs (list, optional): Pairs of categories for which to test significance. Defaults to 'all'.
    - orient (str, optional): Orientation of the boxplot, 'h' for horizontal or 'v' for vertical. Defaults to 'h'.

    Returns:
    - matplotlib.figure.Figure: The figure object containing the plot.
    - matplotlib.axes._subplots.AxesSubplot: The axes object containing the plot.
    """
    # Generate all possible pairs for significance testing if 'pairs' is set to 'all'
    if pairs == 'all':
        pairs = []
        for i in range(len(order) - 1):
            for g in order[i+1:]:
                pairs.append((order[i], g))

    # Plot the initial boxplot
    fig, ax = plt.subplots(1)
    ax = sns.boxplot(data=df, x=x, y=y, order=order)

    # Configure and apply the annotations
    annotator = Annotator(ax, pairs, data=df, x=x, y=y, order=order)
    annotator.configure(test='Brunner-Munzel', text_format='star', comparisons_correction='bonferroni', loc='inside')
    annotator.apply_and_annotate()

    # If horizontal orientation is specified, create a new plot with horizontal boxplots
    if orient == 'h':
        fig2, ax2 = plt.subplots(1)
        sns.boxplot(ax=ax2, x=y, y=x, data=df, order=order)

        # Configure and apply annotations for the horizontal plot
        annotator.new_plot(ax=ax2, plot='boxplot', orient='h', x=y, y=x, order=order, pairs=pairs, data=df)
        annotator.apply_and_annotate()

        # Set y-axis labels to more readable names using the name_map
        ax2.set_yticklabels([name_map[n] for n in order])

        return fig2, ax2

    return fig, ax