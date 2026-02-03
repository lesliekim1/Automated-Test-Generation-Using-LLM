import argparse
from pathlib import Path
import sys
import subprocess
import pandas as pd

PROJECTS = {
    "ansible": 18,
    "black": 23,
    "calculator": 1,
    "cookiecutter": 4,
    "expression": 1,
    "fastapi": 16,
    "httpie": 5,
    "keras": 45,
    "luigi": 33,
    "markup": 2,
    "matplotlib": 30,
    "middle": 2,
    "pandas": 169,
    "pysnooper": 3,
    "sanic": 5,
    "scrapy": 40,
    "spacy": 10,
    "thefuck": 32,
    "tornado": 16,
    "tqdm": 9,
    "youtubedl": 43,
}

# A chosen test file from each Tests4Py project 
TEST_FILES = {
    "ansible": "test/units/errors/test_errors.py", #
    "black": "tests/test_black.py", #
    "calculator": "tests/test_calc.py", #
    "cookiecutter": "tests/test_generate_file.py", #
    "expression": "tests/test_expression.py", # 
    "fastapi": "tests/test_jsonable_encoder.py", #
    "httpie": "tests/test_exit_status.py", #
    "keras": "tests/test_loss_masking.py", #
    "luigi": "test/factorial_test.py", #
    "markup": "tests/test_markup.py", #
    "matplotlib": "lib/matplotlib/tests/test_container.py", #
    "middle": "tests/test_middle.py", #
    "pandas": "pandas/tests/arithmetic/test_numeric.py", ##
    "pysnooper": "tests/test_pysnooper.py", #
    "sanic": "tests/test_middleware.py", #
    "scrapy": "tests/test_mail.py",
    "spacy": "spacy/tests/test_displacy.py",
    "thefuck": "tests/test_logs.py",
    "tornado": "tornado/test/options_test.py",
    "tqdm": "tqdm/tests/tests_version.py",
    "youtubedl": "test/test_age_restriction.py"
}

# Purpose: Create CSV file if it doesn't exist, or read results.csv.
# Parameters: file_path (path to results/results.csv)
# Return: results.csv
def read_csv(file_path):
    if not file_path.exists():
        df = pd.DataFrame(columns=[
            "program_name",
            "test_file",
            "usable",
            "llm_test_file",
            "builds",
            "passes",
            "coverage_before",
            "coverage_after",
            "coverage_delta",
            "kept",
            "discard_reason"
        ])
        df.to_csv(file_path, index=False)
    return pd.read_csv(file_path)

# Purpose: Get all selected projects to be retrieved.
# Parameters: project (project from argument)
# Return: dict of projects
def select_projects(project):
    # Use one project
    if project:
        if project not in PROJECTS:
            sys.exit(f"Unknown project: {project}\nTests4Py projects:\n" + "\n".join(PROJECTS.keys()))
        chosen_projects = {project: PROJECTS[project]} 
        
    # Use all projects
    else:
        chosen_projects = PROJECTS
    return chosen_projects

# Purpose: Parse the coverage report output to get the coverage number only.
# Parameters: result2 (process' object that captured coverage report output)
# Return: a number
def get_coverage_number(result2):
    for line in result2.stdout.splitlines():
        line = line.strip()

        # The last substring of the line with TOTAL is coverage number
        if line.startswith("TOTAL"):
            return line.split()[-1].replace("%", "")

# Run a test file with pytest from Tests4Py project(s) to record statement coverage.
def main():
    parser = argparse.ArgumentParser(description = "get statement coverage of a test class from " \
    "each Tests4Py project.")

    parser.add_argument(
        "-p", "--project",
        help="get statment coverage for a single project."
    )

    args = parser.parse_args()
    scripts_dir = Path(__file__).absolute().parent
    tmp_dir = scripts_dir / "tmp"
    #pytest = scripts_dir.parent /".venv" / "Scripts" / "pytest.exe" #hard coded for windows
    #pip = scripts_dir.parent /".venv" / "Scripts" / "pip.exe" #hard coded for windows
    python = sys.executable # for WSL terminal

    # Create results dir in scripts dir to store CSV file
    results_dir = scripts_dir.parent / "results"
    results_dir.mkdir(exist_ok=True)

    # Read results.csv and get selected projects
    file_path = results_dir / "results.csv" 
    df = read_csv(file_path)
    chosen_projects = select_projects(args.project)
    
    # Run pytest --cov on all chosen projects to get and record coverage to results.csv
    for project, num_bugs in chosen_projects.items():
        for bug_id in range(1, num_bugs + 1):
            program_name = f"{project}_{bug_id}"
            project_dir = tmp_dir / f"{project}_{bug_id}"

            # Attempt to install the project's packages to ensure that environment is compatible
            print(f"CHECKING IF {project}_{bug_id} IS USABLE ... ")

            if bug_id == 1:
                # Skip pip install to avoid getting pip errors to get coverage
                if project == "ansible" or project == "keras" or project == "sanic":
                    result = subprocess.CompletedProcess(args=[], returncode=0)

                else:
                    result = subprocess.run(
                        # str(pip)
                        [python, "-m", "pip", "install", "-e", "."],
                        cwd=str(project_dir)
                    )

            # If environment is compatible after installing project's packages
            if result.returncode == 0:
                print("SUCCESS: ENVIRONMENT COMPATIBLE! ATTEMPTING TO GET COVERAGE ...")
                test_file = project_dir / TEST_FILES[project]
                
                # Attempt to run pytest --cov to get statement coverage and record it 
                result2 = subprocess.run(
                    # str(pytest)
                    [python, "-m", "pytest", str(test_file), "--cov", "--cov-report=term"],
                    cwd=str(project_dir),
                    stdout=subprocess.PIPE,
                    text=True
                )

                print("PRINTING STATEMENT COVERAGE ...")
                print(result2.stdout)
                coverage_before = get_coverage_number(result2)
                    
                # If pytest or other errors has occurred, then project isn't usable for experiment
                if coverage_before is None:
                    new_row = {
                        "program_name": program_name,
                        "test_file": Path(TEST_FILES[project]).name,
                        "usable": False,
                        "llm_test_file": "",
                        "builds": "",
                        "passes": "",
                        "coverage_before": "",
                        "coverage_after": "",
                        "coverage_delta": "",
                        "kept": "",
                        "discard_reason": ""
                    }
                    print("ERROR: CANNOT COLLECT COVERAGE ...")

                # If pytest --cov ran successfully, then project can be used for experiment
                else:
                    new_row = {
                        "program_name": program_name,
                        "test_file": Path(TEST_FILES[project]).name,
                        "usable": True,
                        "llm_test_file": "",
                        "builds": "",
                        "passes": "",
                        "coverage_before": int(coverage_before),
                        "coverage_after": "",
                        "coverage_delta": "",
                        "kept": "",
                        "discard_reason": ""
                    }
                    print("SUCCESS: COVERAGE COLLECTED ...")

            # If pip install -e fails when installing packages because of incompatible environment
            else:
                new_row = {
                    "program_name": program_name,
                    "test_file": Path(TEST_FILES[project]).name,
                    "usable": False,
                    "llm_test_file": "",
                    "builds": "",
                    "passes": "",
                    "coverage_before": "",
                    "coverage_after": "",
                    "coverage_delta": "",
                    "kept": "",
                    "discard_reason": ""
                }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    main()