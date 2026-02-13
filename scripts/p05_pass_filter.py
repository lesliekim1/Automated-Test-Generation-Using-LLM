import argparse
from pathlib import Path
import sys
import pandas as pd
import subprocess

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
          
# Purpose: Update pass column with either true (pass) or false (fails), and update 
#          discard_reason column with 2 if pass failed.
# Parameters: df (DataFrame), program_name (program), passes_bool (return value from subprocess 5x)
# Return: none  
def record_result(df, program_name, passes_bool):
    df.loc[df["program_name"] == program_name, "passes"] = passes_bool
        
    if not passes_bool:
        df.loc[df["program_name"] == program_name, "discard_reason"] = 2
        print("FAILED: FLAKY DETECTED ...")
    else:
        df.loc[df["program_name"] == program_name, "discard_reason"] = pd.NA
        print("SUCCESS: PASSED 5 TIMES ...")
            
# Apply Meta's TestGen-LLM's second filter, which is to check for flaky behavior in five executions.
def main():
    parser = argparse.ArgumentParser(description = "check for any flaky behavior by executing the LLM-generated test five times.")
    
    parser.add_argument(
        "-p", "--project",
        help="apply build filter to a single project."
    )
    
    parser.add_argument(
        "-f", "--file",
        default="results.csv",
        help="CSV filename in results directory that records the data."
    )
    
    # Check valid argument(s)
    args = parser.parse_args()
    validate_project(args.project)
    
    scripts_dir = Path(__file__).absolute().parent
    tmp_dir = scripts_dir / "tmp"
    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / args.file
    python = sys.executable
    
    # Read results.csv and iterate through any projects that have passed the first (build) filter
    df = pd.read_csv(results_csv)
    df_pass = df[(df["usable"] == True) & (df["builds"] == True) & df["passes"].isna()]
    
    # Select a single project only
    if args.project:
        df_pass = df_pass[df_pass["program_name"].str.startswith(args.project + "_")]
    
    print(f"CSV FILE: {args.file}")
    
    for index, row in df_pass.iterrows():
        # Get the program names in selected project (e.g. ansible_1, ansible_2, ...)
        program_name = row["program_name"]
        project = program_name.split("_")[0]
        llm_test_file = row.get("llm_test_file")
        
        project_dir = tmp_dir / program_name
        original_test_file = project_dir / TEST_FILES[project]
        llm_test_path = original_test_file.with_name(str(llm_test_file))
        
        print(f"[{program_name}] PASS FILTER: {llm_test_file}")
        
        # Run the pass filter 5 times to catch any flaky behavior
        codes = []
        passes_bool = True
        for i in range(5):
            result = subprocess.run(
                [python, "-m", "pytest", str(llm_test_path.relative_to(project_dir))],
                cwd=str(project_dir),
                stdout=subprocess.PIPE,
                text=True
            )
            
            print(f"RUN #{i+1} ...")
            print(result.stdout)
            codes.append(result.returncode)
            
        # If run is inconsistent (passing sometimes and failing sometimes), then it's flaky
        passes_bool = (len(set(codes)) == 1)
        
        record_result(df, program_name, passes_bool)
        
    df.to_csv(results_csv, index=False)
    
if __name__ == "__main__":
    main()