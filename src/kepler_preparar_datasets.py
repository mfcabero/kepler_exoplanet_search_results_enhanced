import pandas as pd

# =========================
# 1. Cargar datos originales
# =========================
input_path = "datasets/kepler_exoplanet_search_results_enhanced.csv"
df = pd.read_csv(input_path)

# =========================
# 2. (1) Conteo por HZ_bin
# =========================
hz_bin_count = (
    df["HZ_bin"]
    .value_counts()
    .sort_index()
    .reset_index()
)

hz_bin_count.columns = ["HZ_bin", "count"]

hz_bin_count.to_csv("HZ_bin_count.csv", index=False)

# =========================
# 3. (2) Filtrar HZ_bin = 1
# =========================
df_hz_bin1 = df[df["HZ_bin"] == 1]

df_hz_bin1.to_csv("kepler_hz_bin1.csv", index=False)

# =========================
# 4. (3) Preparar datos para histograma
# =========================
df_hz_bin1_hist = df_hz_bin1.copy()

# Limpiar koi_teq (eliminar NaN)
df_hz_bin1_hist = df_hz_bin1_hist.dropna(subset=["koi_teq"])

# Guardar CSV listo para histograma
df_hz_bin1_hist.to_csv(
    "kepler_hz_bin1_histogram.csv",
    index=False
)

print("Archivos generados correctamente:")
print(" - HZ_bin_count.csv")
print(" - kepler_hz_bin1.csv")
print(" - kepler_hz_bin1_histogram.csv")