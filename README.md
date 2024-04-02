# ONISH-downstream

This repository provides a toolkit for the analysis of data produced by [wormimtools](https://github.com/moore-andrew05/worm-imtools). It includes utilities for data loading, cleaning, parameter generation, and visualization techniques including significance-annotated boxplots.

## Features

- **Data Preprocessing**: Functions to load and clean worm imaging datasets, preparing them for analysis.
- **Parameter Generation**: Tools to compute various parameters from the cleaned data, essential for in-depth analysis.
- **Visualization**: Advanced plotting utilities to visualize data distributions and statistical significance between groups.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. The toolkit requires the following Python libraries:

- pandas
- numpy
- scipy
- seaborn
- matplotlib
- [wormimtools](https://github.com/moore-andrew05/worm-imtools)
- [statannotations](https://github.com/trevismd/statannotations)

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/moore-andrew05/ONISH-downstream
cd ONISH-downstream
```

### Usage

The toolkit is organized into modules for each major functionality. Here's how to use them:

#### Data Loading and Cleaning

```python
from utils.utils import load_and_clean
df = load_and_clean(path_to_data)
```

#### Parameter Generation

```python
from utils.utils import generate_worm_params
df_abund = generate_worm_params(df)
```

#### Visualization

Plotting 1D and 2D barcodes:

```python
from utils.utils import plot_by_id_1d, plot_by_id_2d
plot_by_id_1d(df, id="sample_id")
plot_by_id_2d(df, id="sample_id")
```

Creating significance-annotated boxplots:

```python
from utils.statannotation_utils import significance_boxplot
order = ['Group1', 'Group2']
fig, ax = significance_boxplot(df=df_abund, y='parameter', x='group', order=order)
```
