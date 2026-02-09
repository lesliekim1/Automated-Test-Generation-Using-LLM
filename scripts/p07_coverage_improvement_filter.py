import argparse
from pathlib import Path
import sys
import pandas as pd

# A chosen test file from each Tests4Py project 
TEST_FILES = {
    "ansible": "test/units/errors/test_errors.py", #
    "black": "tests/test_black.py", 
    "calculator": "tests/test_calc.py", 
    "cookiecutter": "tests/test_generate_file.py", 
    "expression": "tests/test_expression.py", 
    "fastapi": "tests/test_jsonable_encoder.py", 
    "httpie": "tests/test_exit_status.py", 
    "keras": "tests/test_loss_masking.py", 
    "luigi": "test/factorial_test.py", 
    "markup": "tests/test_markup.py", 
    "matplotlib": "lib/matplotlib/tests/test_container.py", 
    "middle": "tests/test_middle.py", 
    "pandas": "pandas/tests/arithmetic/test_numeric.py", 
    "pysnooper": "tests/test_pysnooper.py", 
    "sanic": "tests/test_middleware.py", 
    "scrapy": "tests/test_command_fetch.py", 
    "spacy": "spacy/tests/tokenizer/test_tokenizer.py",
    "thefuck": "tests/test_logs.py", 
    "tornado": "tornado/test/escape_test.py", 
    "tqdm": "tqdm/tests/tests_tqdm.py",
    "youtubedl": "test/test_age_restriction.py"
}

# Purpose: Check if project input is valid.
# Parameters: project (project from argument)
# Return: end program if invalid
def validate_project(project):
    if project:
        if project not in TEST_FILES:
            sys.exit(
                f"Unknown project: {project}\n"
                "Available Tests4Py projects:\n" +
                "\n".join(sorted(TEST_FILES.keys()))
            ) 

# Purpose: Update kept column with either true (pass) or false (fails), and update 
#          discard_reason column with 3 if kept failed.
# Parameters: df (DataFrame), program_name (program), kept_bool (boolean value)
#             coverage_delta (difference between original test coverage and LLM test coverage)
# Return: none  
def record_result(df, program_name, kept_bool, coverage_delta):
    if not kept_bool:
        df.loc[df["program_name"] == program_name, "discard_reason"] = 3
        print(f"DISCARDED (coverage_delta={coverage_delta}): {program_name} ...")
        
    else:
        df.loc[df["program_name"] == program_name, "discard_reason"] = pd.NA
        print(f"IMPROVEMENT SUCCESS: {program_name} ...")
    
# Apply Meta's TestGen-LLM's third filter, which is to check for coverage improvement.
def main():
    parser = argparse.ArgumentParser(description = "check for if coverage improvement has occurred on LLM-generated tests.")
    
    parser.add_argument(
        "-p", "--project",
        help="run coverage improvement filter for a single project."
    )
    
    args = parser.parse_args()
    validate_project(args.project)
    
    scripts_dir = Path(__file__).absolute().parent
    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / "results.csv"
    
    # Read results.csv and iterate through any projects that have passed the build and pass filters
    df = pd.read_csv(results_csv)
    df_cov = df[(df["usable"] == True) & (df["builds"] == True) & (df["passes"] == True)]
    
    if args.project:
        df_cov = df_cov[df_cov["program_name"].str.startswith(args.project + "_")]
    
    for index, row in df_cov.iterrows():
        program_name = row["program_name"]
        
        # Calculate coverage_delta and record it
        coverage_delta = float(row["coverage_after"]) - float(row["coverage_before"])
        df.loc[df["program_name"] == program_name, "coverage_delta"] = coverage_delta

        # An extended test class is only "kept" when difference is greater than zero
        kept_bool = coverage_delta > 0
        df.loc[df["program_name"] == program_name, "kept"] = kept_bool
        
        record_result(df, program_name, kept_bool, coverage_delta)
        
    df.to_csv(results_csv, index=False)

if __name__ == "__main__":
    main()