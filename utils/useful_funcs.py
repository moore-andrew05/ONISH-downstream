from wormimtools import BarcodePlotter
from wormimtools.utils import interp1d, normalize




def plot_by_id_2d(df, id, norm_val=10000, new_len=3500, cmap1 = None, cmap2 = None, save=None):
    plotter = BarcodePlotter()
    level="ID"
    if len(id) == 5:
        level = "OLD_ID"


    c1 = interp1d(normalize(df.xs(id, level=level)["channel0_arr_vals_raw"].values[0], norm_val=norm_val), new_len=new_len)
    c2 = interp1d(normalize(df.xs(id, level=level)["channel1_arr_vals_raw"].values[0], norm_val=norm_val), new_len=new_len)

    plotter.plot_barcodes_dual([[c1, c2]], cmap1 = cmap1, cmap2=cmap2, save=save)

def plot_by_id_1d(df, id, norm_val=10000, new_len=3500, save=None):
    plotter = BarcodePlotter()
    level="ID"
    if len(id) == 5:
        level = "OLD_ID"


    c1 = interp1d(normalize(df.xs(id, level=level)["channel0_arr_vals_raw"].values[0], norm_val=norm_val), new_len=new_len)

    plotter.plot_barcodes_single([c1], save=save)

def plot_wrapper_1d(df, norm_value=10000, new_len=3500, save=None):
    plotter = BarcodePlotter()
    data = [[interp1d(normalize(data, norm_value), new_len=new_len)] for data in df["channel0_arr_vals_raw"].values]
    plotter.plot_barcodes_single(data, save)

def plot_wrapper_2d(df, norm_value=10000, new_len=3500, cmap1 = None, cmap2 = None, save=None):
    plotter = BarcodePlotter()
    res = []
    data1 = df["channel0_arr_vals_raw"].values
    data2 = df["channel1_arr_vals_raw"].values
    for i,point in enumerate(data1):
        c1 = interp1d(normalize(data1[i], norm_value),new_len=new_len)
        c2 = interp1d(normalize(data2[i], norm_value),new_len=new_len)
        res.append([c1,c2])
    plotter.plot_barcodes_dual(res, cmap1=cmap1, cmap2=cmap2, save=save)