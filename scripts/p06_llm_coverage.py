import argparse
from pathlib import Path
import sys
import subprocess
import pandas as pd

# A chosen test file from each Tests4Py project 
TEST_FILES = {
    "ansible": "test/units/errors/test_errors.py", 
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
            
# Purpose: Parse the coverage report output to get the coverage number only.
# Parameters: result2 (process' object that captured coverage report output)
# Return: a number
def get_coverage_number(result2):
    for line in result2.stdout.splitlines():
        line = line.strip()

        # The last substring of the line with TOTAL is coverage number
        if line.startswith("TOTAL"):
            return line.split()[-1].replace("%", "")

# Run a LLM-generated test file with pytest from Tests4Py project(s) to record statement coverage.
def main():
    parser = argparse.ArgumentParser(description = "get statement coverage of a LLM-generated test class from " \
    "each Tests4Py project.")

    parser.add_argument(
        "-p", "--project",
        help="get statement coverage for a single project."
    )
    
    parser.add_argument(
        "-f", "--file",
        default="results.csv",
        help="CSV filename in results directory that records the data."
    )

    args = parser.parse_args()
    validate_project(args.project)
    
    scripts_dir = Path(__file__).absolute().parent
    tmp_dir = scripts_dir / "tmp"
    python = sys.executable

    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / args.file

    # Read results.csv and iterate through any projects that have passed the previous two filters
    df = pd.read_csv(results_csv)
    df_cov = df[(df["usable"] == True) & (df["builds"] == True) & (df["passes"] == True) & df["kept"].isna()]
    
    # Select a single project only
    if args.project:
        df_cov = df_cov[df_cov["program_name"].str.startswith(args.project + "_")]
        
    print(f"CSV FILE: {args.file}")
    
    # Run pytest --cov on all chosen projects to get and record coverage to results.csv
    for index, row in df_cov.iterrows():
        # Get the program names in selected project (e.g. ansible_1, ansible_2, ...)
        program_name = row["program_name"]
        project = program_name.split("_")[0]
        llm_test_file = row.get("llm_test_file")
        
        project_dir = tmp_dir / program_name
        original_test_file = project_dir / TEST_FILES[project]
        llm_test_path = original_test_file.with_name(str(llm_test_file))
        
        print(f"[{program_name}] LLM COVERAGE: {llm_test_file}")
        
        # Run pytest --cov on the LLM-generated test file only
        result2 = subprocess.run(
            [python, "-m", "pytest", str(llm_test_path.relative_to(project_dir)), "--cov", "--cov-report=term"],
            cwd=str(project_dir),
            stdout=subprocess.PIPE,
            text=True
        )
        
        print("PRINTING STATEMENT COVERAGE ...")
        print(result2.stdout)
        coverage_after = get_coverage_number(result2)
        
        # If pytest or other errors has occurred, then program failed the third filter
        if coverage_after is None:
            df.loc[df["program_name"] == program_name, "coverage_after"] = pd.NA
            print("ERROR: CANNOT COLLECT COVERAGE ...")
            
        else:
            df.loc[df["program_name"] == program_name, "coverage_after"] = int(coverage_after)
            print("SUCCESS: COVERAGE COLLECTED ...")
            
        df.to_csv(results_csv, index=False)
            
if __name__ == "__main__":
    main()