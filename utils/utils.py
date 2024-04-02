import pandas as pd
from scipy import signal
from wormimtools.utils import interp1d
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


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
    # Load in data and pull requested groups from the diet column
    raw_data = pd.read_pickle(path)   # Replace with your database path
    data = raw_data.copy(deep=True)
    clean_data = data.loc[:, ("ID","diet", "rep", 'stage', "channel0_arr_vals_raw", "channel1_arr_vals_raw")]
    clean_data["vals"] = clean_data["channel0_arr_vals_raw"].apply(interp1d,args = (3000,)) # Interpolate to 3000 values
    clean_data["vals2"] = clean_data["channel1_arr_vals_raw"].map(lambda x: interp1d(x, 3000) if type(x) != float  else x)

    return clean_data


def _filter_on_diet(df, groups):
    return df[df['diet'].isin(groups)]

def filter_on_diet_and_channel(df, groups):
    return df[df['diet_and_channel'].isin(groups)]



def generate_worm_params(df, num_channels = 2):
    # Generates dataframe for figures, calculates peaks, mean of peak values, and mean of peak position. 
    # Peak calling threshold is set to 2500. 

    rows = []

    for row in df.iterrows():

        data = row[1]
        for i in range(num_channels):
            vals = data["vals"] if i == 0 else data[f"vals{i+1}"]

            if isinstance(vals, np.ndarray):
                peaks, _ = signal.find_peaks(vals, height=2500)
                if len(peaks) == 0:
                    avg_peak = 0
                else:
                    avg_peak = np.mean(vals[peaks])
                
                total_peak_flo = np.sum(vals[peaks])
                d = {"ID": data["ID"],
                    "diet_and_channel": (data["diet"] + f"_{i}"), 
                    'stage': data['stage'], 
                    'peaks': len(peaks), 
                    'avg_peak': avg_peak, 
                    'avg_peak_pos': np.mean(peaks) if len(peaks) > 0 else None, 
                    'vals': vals, 
                    'total_peak_flo': total_peak_flo}
    
                rows.append(d)

    return pd.DataFrame(rows)

def generate_section_params(df, num_sections=9, channels=2):
    # Generates dataframe for row sums, splitting each sample into `num_sections` rows. 
    # num_sections can be any integer. 


    rows = []
    num_sections = num_sections

    for row in df.iterrows():
        data = row[1]
        for i in range(channels):
            vals = data["vals"] if i == 0 else data[f"vals{i+1}"]
            if isinstance(vals, np.ndarray):
                s = np.array_split(vals, num_sections)
                for k, v in enumerate(s):
                    peaks, _ = signal.find_peaks(v, height=2500)

                    peak_sum = sum(v[peaks])
                    log_sum = np.log(peak_sum) if peak_sum > 0 else 0
                    row_sum = sum(v)
                    log_row_sum = np.log(row_sum) if row_sum > 0 else 0

                    d = {
                        "ID": data["ID"], 
                        "diet_and_channel": (data["diet"] + f"_{i}"), 
                        "rep": data["rep"], 
                        "sect": str((k+1)), 
                        "vals": v, 
                        "row_sum": sum(v), 
                        "log_row_sum":log_row_sum,
                        "peak_sum": peak_sum,
                        "log_peak_sum": log_sum,
                        "avg_peak": np.mean(v[peaks]) if len(peaks) > 0 else 0, 
                        "peaks": len(peaks)
                    }
                    
                    rows.append(d)

    return pd.DataFrame(rows)


def plot_spatial(df, x, y, hue):
    sns.set_theme(style="white")
    fig, ax = plt.subplots(1)

    ax = sns.lineplot(x=x,
                y=y,
                hue=hue,
                data=df)

    sns.move_legend(ax, "upper left", 
                    labels=[name_map[n] for n in ax.get_legend_handles_labels()[1]], 
                    title=hue)

    ax.set(xlabel=x, 
        ylabel=y);

    return fig, ax