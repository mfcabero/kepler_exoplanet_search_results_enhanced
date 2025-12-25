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

# Prepare histogram data (convert to Celcius)
df_hz_bin1_hist = df_hz_bin1.dropna(subset=["koi_teq"])
values_C = df_hz_bin1_hist["koi_teq"] - 273.15
# Compute optimal bin edges in C
bin_edges_C = np.histogram_bin_edges(values_C, bins="fd")

# Compute bins and counts
counts_C, edges_C = np.histogram(values_C, bins=bin_edges_C)
bin_left_C = edges_C[:-1].round(1)
bin_right_C = edges_C[1:].round(1)
bin_center_C = ((bin_left_C + bin_right_C) / 2).round(1)

# Create binned dataset in C
df_histogram_C = pd.DataFrame({
    "temp_C_bin_left": bin_left_C,
    "temp_C_bin_right": bin_right_C,
    "temp_C_bin_center": bin_center_C,
    "frequency": counts_C
})

df_histogram_C.to_csv(OUT_HZ_BIN1_HIST, index=False)
print(f"Binned Celsius data saved: {len(df_histogram_C)} bins")
