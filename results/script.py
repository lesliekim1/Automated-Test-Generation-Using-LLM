import pandas as pd

file_path = "LLAMA_combined_results.csv"

# Load CSV
df = pd.read_csv(file_path)

# Recompute coverage_delta just to be safe
df["coverage_delta"] = df["coverage_after"] - df["coverage_before"]

# Remove rows where coverage_delta == 0
df_clean = df[df["coverage_delta"] != 0]

# Overwrite the same file
df_clean.to_csv(file_path, index=False)

print(f"Removed rows with coverage_delta = 0. Remaining rows: {len(df_clean)}")