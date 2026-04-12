import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Calculate precision score for a model and run a two-proportion z-test
def main():
    parser = argparse.ArgumentParser(
        description="calculate precision score for model and also run a two-proportion z-test."
    )

    parser.add_argument(
        "-f", "--file",
        help="CSV filename in results directory that records the data."
    )

    args = parser.parse_args()
    scripts_dir = Path(__file__).absolute().parent
    results_dir = scripts_dir.parent / "results"

    results_csv = results_dir / args.file
    df = pd.read_csv(results_csv)

    # Calculate precision score
    tp = (df["RELIABLE"] == True).sum()
    fp = (df["RELIABLE"] == False).sum()
    precision = tp / (tp + fp)

    print(f"\nTP (reliable): {tp}")
    print(f"FP (not reliable): {fp}")
    print(f"total passed tests: {tp+fp}")
    print(f"PRECISION SCORE: {precision:.4f}")

    # Two-proportion z-test (manually typed)
    count = np.array([92, 178])
    nobs = np.array([1312, 1312])

    z_stat, p_val = proportions_ztest(count, nobs, alternative='two-sided')

    print("\n\nTWO-PROPORTION Z-TEST")
    print(f"z-statistic: {z_stat:.4f}")
    print(f"p-value: {p_val:.4f}")

main()