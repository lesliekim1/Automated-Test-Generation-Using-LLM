import argparse
from pathlib import Path
import pandas as pd

# Calculate average coverage delta (increase) per prompt
def main():
    parser = argparse.ArgumentParser(
        description="calculate average coverage delta (increase) per prompt."
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

    # Group by prompt and calculate average coverage delta (increase)
    avg_delta = df.groupby("prompt_mode")["coverage_delta"].mean()

    print("AVERAGE COVERAGE DELTA PER PROMPT:")
    for prompt, avg in avg_delta.items():
        print(f"{prompt}: {avg:.4f}")
    print()
    
main()