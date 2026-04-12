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
    
    # Replace old prompt names with actual prompt names from Meta's study
    df["prompt_mode"] = df["prompt_mode"].replace({
        "TESTONLY": "EXTENDTEST",
        "TESTCUT": "EXTENDCOV"
    })
    
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
    print()
    
    
    # Combined overall and filter tables (manually typed data)
    combined_success = 27 + 23 + 26 + 16
    combined_trials = 328 * 4
    combined_build = 60 + 69 + 97 + 42
    combined_pass = 60 + 69 + 97 + 42

    combined_overall_data = [
        ["Llama", combined_success, combined_trials, round(combined_success / combined_trials, 2)]
    ]

    combined_overall_table = pd.DataFrame(
        combined_overall_data,
        columns=["LLM", "Successful trials", "Total trials", "Success rate"]
    )

    combined_filter_data = [
        ["Llama", "Build", combined_build, combined_trials, round(combined_build / combined_trials, 2)],
        ["Llama", "Pass", combined_pass, combined_build, round(combined_pass / combined_build, 2)],
        ["Llama", "Add Coverage", combined_success, combined_pass, round(combined_success / combined_pass, 2)]
    ]

    combined_filter_table = pd.DataFrame(
        combined_filter_data,
        columns=["LLM", "Filter", "Successful trials", "Total trials", "Success rate"]
    )

    print("\n" + combined_overall_table.to_string(index=False))
    print("\n" + combined_filter_table.to_string(index=False) + "\n")

main()