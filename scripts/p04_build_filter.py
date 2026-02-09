import argparse
from pathlib import Path
import sys
import pandas as pd
import subprocess

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
            
# Purpose: Update builds column with either true (pass) or false (fails), and update 
#          discard_reason column with 1 if build failed.
# Parameters: df (DataFrame), program_name (program), result (return value from subprocess)
# Return: none
def record_result(df, program_name, result):
    # Boolean value to be recorded
    builds_bool = (result.returncode == 0)
    df.loc[df["program_name"] == program_name, "builds"] = builds_bool

    if not builds_bool:
        df.loc[df["program_name"] == program_name, "discard_reason"] = 1
        print("BUILD FAILED ...")
    else:
        df.loc[df["program_name"] == program_name, "discard_reason"] = pd.NA
        print("BUILD SUCCESS ...")
    
            
# Apply Meta's TestGen-LLM's first filter, which is to check for build correctness.
def main():
    parser = argparse.ArgumentParser(description = "check if an LLM-generated test class is built correctly.")
    
    parser.add_argument(
        "-p", "--project",
        help="apply build filter to a single project."
    )
    
    # Check valid argument(s)
    args = parser.parse_args()
    validate_project(args.project)

    scripts_dir = Path(__file__).absolute().parent
    tmp_dir = scripts_dir / "tmp"
    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / "results.csv" # edit file name if needed
    
    # Read results.csv and iterate through 'usable' projects only (projects that have coverage_before)
    df = pd.read_csv(results_csv)
    df_usable = df[df["usable"] == True]
    
    # Select a single project only
    if args.project:
        df_usable = df_usable[df_usable["program_name"].str.startswith(args.project + "_")]
    
    for index, row in df_usable.iterrows():
        # Get the program names in selected project (e.g. ansible_1, ansible_2, ...)
        program_name = row["program_name"]
        project = program_name.split("_")[0]
        llm_test_file = row.get("llm_test_file")

        project_dir = tmp_dir / program_name
        original_test_file = project_dir / TEST_FILES[project]
        llm_test_path = original_test_file.with_name(str(llm_test_file))

        print(f"[{program_name}] BUILD FILTER (pytest --collect-only): {llm_test_file}")

        # Run pytest --collect-only to replicate build filter 
        result = subprocess.run(
            ["pytest", "--collect-only", str(llm_test_path.relative_to(project_dir))],
            cwd=str(project_dir)
        )

        # Record result to csv file
        record_result(df, program_name, result)
    
    df.to_csv(results_csv, index=False)
    
if __name__ == "__main__":
    main()