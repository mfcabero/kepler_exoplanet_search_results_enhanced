"""
Generation of required datasets for Kepler Visualization
Author: mfcabero (2025)
"""

import pandas as pd
import numpy as np

# Paths
SRC_PATH = "../datasets/kepler_exoplanet_search_results_enhanced.csv"
OUT_HZ_BIN_COUNT = "../datasets/HZ_bin_count.csv"
OUT_HZ_BIN1 = "../datasets/kepler_hz_bin1.csv"
OUT_HZ_BIN1_HIST = "../datasets/kepler_hz_bin1_histogram.csv"

# Load original dataset
df = pd.read_csv(SRC_PATH)

# Count per HZ_bin
hz_bin_count = (
    df["HZ_bin"]
    .value_counts()
    .sort_index()
    .reset_index()
)
hz_bin_count.columns = ["HZ_bin", "count"]

hz_bin_count.to_csv(OUT_HZ_BIN_COUNT, index=False)
print(f"HZ_bin count saved to {OUT_HZ_BIN_COUNT}")


# Filter dataset for HZ_bin = 1
df_hz_bin1 = df[df["HZ_bin"] == 1]
print(f"Filtered {len(df_hz_bin1)} entries with HZ_bin = 1")
df_hz_bin1.to_csv(OUT_HZ_BIN1, index=False)

# Prepare histogram data
df_hz_bin1_hist = df_hz_bin1.dropna(subset=["koi_teq"])
values = df_hz_bin1_hist["koi_teq"].to_numpy()
bin_edges = np.histogram_bin_edges(values, bins="fd")

# Compute bins and counts
counts, edges = np.histogram(values, bins=bin_edges)
bin_left = edges[:-1].round(1)
bin_right = edges[1:].round(1)
bin_center = ((bin_left + bin_right) / 2).round(1)

# Create binned dataset
df_histogram = pd.DataFrame({
    "temp_bin_left": bin_left,
    "temp_bin_right": bin_right,
    "temp_bin_center": bin_center,
    "frequency": counts
})

df_histogram.to_csv(OUT_HZ_BIN1_HIST, index=False)
print(f"Binned data saved: {len(df_histogram)} bins")
