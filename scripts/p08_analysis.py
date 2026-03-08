import argparse
from pathlib import Path
import pandas as pd

# Output tables to display the results (overall success rate and each filter success rates)
def main():
    parser = argparse.ArgumentParser(
        description="create tables to display the results (overall success rate and each filter success rates)."
    )

    parser.add_argument(
        "-f", "--file",
        default="results.csv",
        help="CSV filename in results directory that records the data."
    )

    args = parser.parse_args()
    scripts_dir = Path(__file__).absolute().parent
    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / args.file

    df = pd.read_csv(results_csv)
    df = df[df["usable"] == True]
    
    prompt_mode = df["prompt_mode"].iloc[0]
    total_usable = len(df)
    build_count = df["builds"].sum()
    pass_count = df["passes"].sum()
    coverage_improvement_count = df["kept"].sum()

    # Success rates
    build_rate = round(build_count / total_usable, 2)
    pass_rate = round(pass_count / build_count, 2)
    coverage_improvement_rate = round(coverage_improvement_count / pass_count, 2)
    overall_success_rate = round(coverage_improvement_count / total_usable, 2)

    # Tables
    overall_data = [
        [prompt_mode, coverage_improvement_count, total_usable, overall_success_rate]
    ]
    overall_table = pd.DataFrame(
        overall_data,
        columns=["Prompt", "Successful trials", "Total trials", "Success rate"]
    )

    filter_data = [
        [prompt_mode, "Build", build_count, total_usable, build_rate],
        [prompt_mode, "Pass", pass_count, build_count, pass_rate],
        [prompt_mode, "Add Coverage", coverage_improvement_count, pass_count, coverage_improvement_rate],
    ]

    filter_table = pd.DataFrame(
        filter_data,
        columns=["Prompt", "Filter", "Successful trials", "Total trials", "Success rate"]
    )

    print("\n" + overall_table.to_string(index=False))
    print("\n" + filter_table.to_string(index=False))

if __name__ == "__main__":
    main()