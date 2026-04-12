import pandas as pd

file_path = "results_LLAMA_CORNERCASES.csv"

df = pd.read_csv(file_path)

df["coverage_delta"] = df["coverage_after"] - df["coverage_before"]

eligible_mask = (
    (df["usable"] == True) &
    (df["builds"] == True) &
    (df["passes"] == True)
)

df.loc[eligible_mask, "kept"] = df.loc[eligible_mask, "coverage_delta"] > 0
df.loc[eligible_mask & (df["coverage_delta"] <= 0), "discard_reason"] = 3
df.loc[eligible_mask & (df["coverage_delta"] > 0), "discard_reason"] = pd.NA

df.to_csv(file_path, index=False)

print(f"Fixed kept/discard_reason for eligible rows only in: {file_path}")