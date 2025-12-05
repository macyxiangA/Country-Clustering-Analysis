# Country Clustering Analysis

This project performs hierarchical agglomerative clustering (HAC) on country-level economic and demographic data and visualizes the results with both dendrograms and a world map.

## Overview

The code provides:

- Data loading from a CSV file
- Feature extraction for each country
- Feature normalization
- A custom implementation of hierarchical agglomerative clustering (single-link or complete-link)
- Dendrogram plotting using SciPy
- World map visualization of clusters using GeoPandas

## Requirements

- Python 3
- numpy
- scipy
- matplotlib
- geopandas

You can install the required packages with:

    pip install numpy scipy matplotlib geopandas

## Files

- clustering.py — main implementation file containing:
  - load_data
  - calc_features
  - normalize_features
  - hac
  - fig_hac
  - world_map
- countries.csv — input data file (not included)
- README.md

## Data Format

The input CSV is expected to have at least the following columns:

- country
- child_mort
- exports
- health
- imports
- income
- inflation
- life_expec
- total_fer
- gdpp

Each row corresponds to one country and its numeric attributes.

## Usage

### 1. Load and normalize data

Example for reading the CSV and building the feature matrix:

    from clustering import load_data, calc_features, normalize_features

    rows = load_data("countries.csv")
    features = [calc_features(r) for r in rows]
    features_norm = normalize_features(features)

    names = [r["country"] for r in rows]

### 2. Run hierarchical agglomerative clustering

You can choose either "single" or "complete" linkage:

    from clustering import hac

    Z = hac(features_norm, linkage_type="single")
    # or:
    # Z = hac(features_norm, linkage_type="complete")

The function returns a linkage matrix Z of shape (n-1, 4), following the SciPy convention.

### 3. Plot the dendrogram

    from clustering import fig_hac
    import matplotlib.pyplot as plt

    fig = fig_hac(Z, names)
    plt.show()

This will display a dendrogram with country names on the x-axis.

### 4. Visualize clusters on a world map

To display the clusters geographically, choose a target number of clusters K and call:

    from clustering import world_map

    K_clusters = 5
    world_map(Z, names, K_clusters)

This will:

- Build cluster assignments from the linkage matrix Z
- Map cluster labels to country names
- Plot a world map where each clustered country is colored according to its cluster
- Countries that are not in the dataset appear in a default color

## Notes

- Hierarchical clustering is implemented manually based on pairwise distances between feature vectors.
- Feature normalization is performed using z-score (subtract mean and divide by standard deviation).
- GeoPandas uses the Natural Earth low-resolution dataset to draw the base world map.
- The project is intended as a simple, self-contained example of clustering and geospatial visualization.
