import pandas as pd
from scipy import signal
from wormimtools.utils import interp1d  
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Mapping from original sample names to more readable ones
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

def load_and_clean(path="/Users/amoore/projects/stable_txts/confocal_database.pkl"):
    """
    Loads and cleans data from a specified pickle file.
    
    Args:
    - path (str): Path to the pickle file containing the dataset.

    Returns:
    - pd.DataFrame: A cleaned DataFrame with interpolated values and necessary columns.
    """
    # Load data from a pickle file
    raw_data = pd.read_pickle(path)   # Replace with your database path
    data = raw_data.copy(deep=True)
    # Select relevant columns and clean data
    clean_data = data.loc[:, ("ID","diet", "rep", 'stage', "channel0_arr_vals_raw", "channel1_arr_vals_raw")]
    # Apply interpolation to the raw values in channel0
    clean_data["vals"] = clean_data["channel0_arr_vals_raw"].apply(interp1d, args=(3000,)) # Interpolate to 3000 values
    # Apply interpolation to the raw values in channel1, handle missing values gracefully
    clean_data["vals2"] = clean_data["channel1_arr_vals_raw"].map(lambda x: interp1d(x, 3000) if type(x) != float else x)

    return clean_data


def _filter_on_diet(df, groups):
    """
    Filters the DataFrame based on diet.

    Args:
    - df (pd.DataFrame): The DataFrame to filter.
    - groups (list): A list of diets to filter by.

    Returns:
    - pd.DataFrame: A filtered DataFrame containing only the specified diets.
    """
    return df[df['diet'].isin(groups)]

def filter_on_diet_and_channel(df, groups):
    """
    Filters the DataFrame based on concatenated diet and channel information.

    Args:
    - df (pd.DataFrame): The DataFrame to filter.
    - groups (list): A list of concatenated diet and channel strings to filter by.

    Returns:
    - pd.DataFrame: A filtered DataFrame containing only the specified diet and channel combinations.
    """
    return df[df['diet_and_channel'].isin(groups)]


def generate_worm_params(df, num_channels=2):
    """
    Generates parameters for each worm based on peak analysis from fluorescence data.

    Args:
    - df (pd.DataFrame): DataFrame containing the worms' data.
    - num_channels (int): Number of fluorescence channels to analyze.

    Returns:
    - pd.DataFrame: A DataFrame containing the calculated parameters for each worm.
    """
    rows = []

    for _, data in df.iterrows():
        for i in range(num_channels):
            # Select the appropriate channel data
            vals = data["vals"] if i == 0 else data[f"vals{i+1}"]

            if isinstance(vals, np.ndarray):
                # Find peaks with a minimum height of 2500
                peaks, _ = signal.find_peaks(vals, height=2500)
                # Calculate average peak value if peaks are present
                avg_peak = np.mean(vals[peaks]) if len(peaks) > 0 else 0
                # Calculate total fluorescence at peak locations
                total_peak_flo = np.sum(vals[peaks])
                # Store calculated parameters in a dictionary
                d = {"ID": data["ID"],
                     "diet_and_channel": (data["diet"] + f"_{i}"), 
                     'stage': data['stage'], 
                     'peaks': len(peaks), 
                     'avg_peak': avg_peak, 
                     'avg_peak_pos': np.mean(peaks) if len(peaks) > 0 else None, 
                     'vals': vals, 
                     'total_peak_flo': total_peak_flo}
                # Append the dictionary to the list of rows
                rows.append(d)

    return pd.DataFrame(rows)

def generate_section_params(df, num_sections=9, channels=2):
    """
    Generates parameters by dividing each worm into sections and analyzing fluorescence data within each section.

    Args:
    - df (pd.DataFrame): DataFrame containing the worms' data.
    - num_sections (int): Number of sections to divide each worm into.
    - channels (int): Number of fluorescence channels to analyze.

    Returns:
    - pd.DataFrame: A DataFrame containing the calculated parameters for each section of each worm.
    """
    rows = []

    for _, data in df.iterrows():
        for i in range(channels):
            vals = data["vals"] if i == 0 else data[f"vals{i+1}"]
            if isinstance(vals, np.ndarray):
                # Split the array into the specified number of sections
                sections = np.array_split(vals, num_sections)
                for k, section in enumerate(sections):
                    # Find peaks within each section
                    peaks, _ = signal.find_peaks(section, height=2500)
                    # Calculate sum of peaks and log-transform if non-zero
                    peak_sum = sum(section[peaks])
                    log_sum = np.log(peak_sum) if peak_sum > 0 else 0
                    # Calculate sum of section values and log-transform if non-zero
                    row_sum = sum(section)
                    log_row_sum = np.log(row_sum) if row_sum > 0 else 0
                    # Store calculated parameters in a dictionary
                    d = {
                        "ID": data["ID"], 
                        "diet_and_channel": (data["diet"] + f"_{i}"), 
                        "rep": data["rep"], 
                        "sect": str(k+1), 
                        "vals": section, 
                        "row_sum": row_sum, 
                        "log_row_sum": log_row_sum,
                        "peak_sum": peak_sum,
                        "log_peak_sum": log_sum,
                        "avg_peak": np.mean(section[peaks]) if len(peaks) > 0 else 0, 
                        "peaks": len(peaks)
                    }
                    # Append the dictionary to the list of rows
                    rows.append(d)

    return pd.DataFrame(rows)


def plot_spatial(df, x, y, hue):
    """
    Plots spatial fluorescence data with seaborn.

    Args:
    - df (pd.DataFrame): DataFrame containing the data to plot.
    - x (str): The name of the DataFrame column to use for the x-axis.
    - y (str): The name of the DataFrame column to use for the y-axis.
    - hue (str): The name of the DataFrame column to use for color encoding.

    Returns:
    - tuple: A tuple containing the matplotlib Figure and Axes objects.
    """
    # Set the seaborn theme
    sns.set_theme(style="white")
    # Create a new figure and axes
    fig, ax = plt.subplots(1)

    # Plot the data using seaborn's lineplot function
    ax = sns.lineplot(x=x, y=y, hue=hue, data=df)

    # Move the legend to the upper left corner and update labels with readable names
    sns.move_legend(ax, "upper left", labels=[name_map[n] for n in ax.get_legend_handles_labels()[1]], title=hue)

    # Set axis labels
    ax.set(xlabel=x, ylabel=y)

    return fig, ax
