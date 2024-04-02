from wormimtools import BarcodePlotter
from wormimtools.utils import interp1d, normalize

def plot_by_id_2d(df, id, norm_val=10000, new_len=3500, cmap1=None, cmap2=None, save=None):
    """
    Plots 2D barcodes for a specified ID from a DataFrame.

    Args:
    - df (pd.DataFrame): The DataFrame containing the worm imaging data.
    - id (str): The ID of the data to plot.
    - norm_val (int, optional): The value to normalize the data. Defaults to 10000.
    - new_len (int, optional): The new length for the interpolated data. Defaults to 3500.
    - cmap1, cmap2 (str, optional): Colormap names for the two channels.
    - save (str, optional): Path to save the plot. If None, the plot is not saved.

    Returns:
    None. Displays or saves the 2D barcode plot.
    """
    plotter = BarcodePlotter()
    level = "ID"
    if len(id) == 5:  # Checks if the ID corresponds to the old format
        level = "OLD_ID"

    # Normalize and interpolate data for both channels
    c1 = interp1d(normalize(df.xs(id, level=level)["channel0_arr_vals_raw"].values[0], norm_val=norm_val), new_len=new_len)
    c2 = interp1d(normalize(df.xs(id, level=level)["channel1_arr_vals_raw"].values[0], norm_val=norm_val), new_len=new_len)

    # Plot 2D barcodes using the BarcodePlotter
    plotter.plot_barcodes_dual([[c1, c2]], cmap1=cmap1, cmap2=cmap2, save=save)

def plot_by_id_1d(df, id, norm_val=10000, new_len=3500, save=None):
    """
    Plots 1D barcodes for a specified ID from a DataFrame.

    Args:
    - df (pd.DataFrame): The DataFrame containing the worm imaging data.
    - id (str): The ID of the data to plot.
    - norm_val (int, optional): The value to normalize the data. Defaults to 10000.
    - new_len (int, optional): The new length for the interpolated data. Defaults to 3500.
    - save (str, optional): Path to save the plot. If None, the plot is not saved.

    Returns:
    None. Displays or saves the 1D barcode plot.
    """
    plotter = BarcodePlotter()
    level = "ID"
    if len(id) == 5:  # Checks if the ID corresponds to the old format
        level = "OLD_ID"

    # Normalize and interpolate data for the first channel
    c1 = interp1d(normalize(df.xs(id, level=level)["channel0_arr_vals_raw"].values[0], norm_val=norm_val), new_len=new_len)

    # Plot 1D barcodes using the BarcodePlotter
    plotter.plot_barcodes_single([c1], save=save)

def plot_wrapper_1d(df, norm_value=10000, new_len=3500, save=None):
    """
    Wrapper function to plot 1D barcodes for all entries in a DataFrame.

    Args:
    - df (pd.DataFrame): The DataFrame containing the worm imaging data.
    - norm_value (int, optional): The value to normalize the data. Defaults to 10000.
    - new_len (int, optional): The new length for the interpolated data. Defaults to 3500.
    - save (str, optional): Path to save the plots. If None, the plots are not saved.

    Returns:
    None. Displays or saves the 1D barcode plots.
    """
    plotter = BarcodePlotter()
    # Normalize and interpolate data for all entries in the DataFrame
    data = [[interp1d(normalize(datum, norm_value), new_len=new_len)] for datum in df["channel0_arr_vals_raw"].values]
    
    # Plot 1D barcodes for all entries
    plotter.plot_barcodes_single(data, save)

def plot_wrapper_2d(df, norm_value=10000, new_len=3500, cmap1=None, cmap2=None, save=None):
    """
    Wrapper function to plot 2D barcodes for all entries in a DataFrame.

    Args:
    - df (pd.DataFrame): The DataFrame containing the worm imaging data.
    - norm_value (int, optional): The value to normalize the data. Defaults to 10000.
    - new_len (int, optional): The new length for the interpolated data. Defaults to 3500.
    - cmap1, cmap2 (str, optional): Colormap names for the two channels.
    - save (str, optional): Path to save the plots. If None, the plots are not saved.

    Returns:
    None. Displays or saves the 2D barcode plots.
    """
    plotter = BarcodePlotter()
    res = []
    data1 = df["channel0_arr_vals_raw"].values
    data2 = df["channel1_arr_vals_raw"].values
    for i, _ in enumerate(data1):
        # Normalize and interpolate data for both channels for each entry
        c1 = interp1d(normalize(data1[i], norm_value), new_len=new_len)
        c2 = interp1d(normalize(data2[i], norm_value), new_len=new_len)
        res.append([c1, c2])

    # Plot 2D barcodes for all entries
    plotter.plot_barcodes_dual(res, cmap1=cmap1, cmap2=cmap2, save=save)
