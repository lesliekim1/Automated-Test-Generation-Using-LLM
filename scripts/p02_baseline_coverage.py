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

TEST_FILES = {
    "ansible": "test/ansible_test/unit/test_diff.py",
    "black": "tests/test_black.py", 
    "calculator": "tests/test_calc.py", 
    "cookiecutter": "tests/test_generate_file.py", 
    "expression": "tests/test_expression.py",
    "fastapi": "tests/test_additional_properties.py",
    "httpie": "tests/test_binary.py",
    "keras": "tests/test_loss_masking.py", 
    "luigi": "test/factorial_test.py",
    "markup": "tests/test_markup.py",
    "matplotlib": "tests.py",
    "middle": "tests/test_middle.py",
    "pandas": "pandas/tests/arithmetic/test_numeric.py",
    "pysnooper": "tests/test_pysnooper.py", 
    "sanic": "tests/test_app.py",
    "scrapy": "tests/test_mail.py",
    "spacy": "spacy/tests/test_displacy.py",
    "thefuck": "tests/test_logs.py",
    "tornado": "tornado/test/options_test.py",
    "tqdm": "tqdm/tests/tests_version.py",
    "youtubedl": "test/test_age_restriction.py"
}

# Record the statement of a test class from each Tests4Py programs that is compatible to environment. 
def main():
    parser = argparse.ArgumentParser(description = "get statement coverage of a test class from " \
    "each Tests4Py project.")

    parser.add_argument(
        "-p", "--project",
        help="get statment coverage for a single project."
    )

    args = parser.parse_args()
    root_dir = Path(__file__).absolute().parent
    tmp_dir = root_dir / "tmp"
    pytest = root_dir.parent /".venv" / "Scripts" / "pytest.exe"
    pip = root_dir.parent /".venv" / "Scripts" / "pip.exe"
    
    results_dir = root_dir.parent / "results"
    results_dir.mkdir(exist_ok=True)

    file_path = results_dir / "results.csv" 

    # Create CSV file if it doesn't exist
    if not file_path.exists():
        df = pd.DataFrame(columns=[
            "program_name",
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

    df = pd.read_csv(file_path)
    
    # Use one project
    if args.project:
        if args.project not in PROJECTS:
            sys.exit(f"Unknown project: {args.project}\nTests4Py projects:\n" + "\n".join(PROJECTS.keys()))
        t4p_projects = {args.project: PROJECTS[args.project]} 
        
    # Use all projects
    else:
        t4p_projects = PROJECTS

    for project, num_bugs in t4p_projects.items():
        for bug_id in range(1, num_bugs+1):
            program_name = f"{project}_{bug_id}"
            project_dir = tmp_dir / f"{project}_{bug_id}"

            print(f"BASELINE COVERAGE {project}_{bug_id}... ")
            
            if bug_id == 1:
                # Run 'pip install -e .' on each project_1 to make sure that it's compatible
                result = subprocess.run(
                    [str(pip), "install", "-e", "."],
                    cwd=str(project_dir)
                    )

            if result.returncode == 0:
                test_file = project_dir / TEST_FILES[project]
                
                # Run pytest [test file] --cov to get statement coverage and record it 
                result2 = subprocess.run(
                    [str(pytest), str(test_file), "--cov", "--cov-report=term"],
                    cwd=str(project_dir),
                    stdout=subprocess.PIPE,
                    text=True
                )

                print("--STATEMENT COVERAGE--")
                print(result2.stdout)

                coverage_before = ""
                # Split coverage report into list of lines
                for line in result2.stdout.splitlines():
                    line = line.strip()

                    # Last substring is coverage number
                    if line.startswith("TOTAL"):
                        coverage_before = line.split()[-1].replace("%", "")
                        break
                    
                # If pytest or import error has occurred, then program isn't usable for experiment
                if coverage_before == "":
                    new_row = {
                        "program_name": program_name,
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
                    print("ERROR: CANNOT COLLECT COVERAGE...")
                else:
        
                    new_row = {
                        "program_name": program_name,
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
                    print("SUCCESS: COVERAGE COLLECTED...")

            # Fails to do pip install -e . for installing packages
            else:
                new_row = {
                    "program_name": program_name,
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