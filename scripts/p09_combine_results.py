import argparse
from pathlib import Path
import pandas as pd

# Combine results CSV files and extract rows (trials) that passed TestGen-LLM only
def main():
    parser = argparse.ArgumentParser(
        description="combine specified CSV files and extract trials that passed TestGen-LLM only."
    )

    parser.add_argument(
        "-f", "--files",
        nargs="+",
        required=True,
        help="List of CSV files in the results directory to combine"
    )

    args = parser.parse_args()

    scripts_dir = Path(__file__).absolute().parent
    results_dir = scripts_dir.parent / "results"

    df_list = []

    # Read each file
    for file_name in args.files:
        results_csv = results_dir / file_name
        df = pd.read_csv(results_csv)

        df = df[df["usable"] == True]
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)

    # Keep trials that passed the third filter
    df_kept = combined_df[combined_df["kept"] == True].copy()

    # Add new columns for manually review
    df_kept["RELIABLE"] = "" # True or False
    df_kept["REASON"] = "" # brief description on why the passed test isn't reliable

    output_file = results_dir / "combined_tests.csv"
    df_kept.to_csv(output_file, index=False)

    print(f"\nTOTAL TESTS: {len(df_kept)}")
    print(f"SAVED TO: {output_file}\n")

main()