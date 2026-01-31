import argparse
from pathlib import Path
import sys
import subprocess
import pandas as pd
import os

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

def main():
    parser = argparse.ArgumentParser(description = "get statement coverage of a test class from " \
    "each Tests4Py project.")

    parser.add_argument(
        "-p", "--project",
        help="get coverage for a single project."
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
            "included",
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
    
    # Use one project and its buggy versions
    if args.project:
        if args.project not in PROJECTS:
            sys.exit(f"Unknown project: '{args.project}'.\nTests4Py projects: {"\n".join((PROJECTS.keys()))}")
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
                # Check if there's no compatibility issues first to decide to include project for experiment
                result = subprocess.run(
                    [str(pip), "install", "-e", "."],
                    cwd=str(project_dir)
                    )

            if result.returncode == 0:
                print("init")
            else:
                new_row = {
                    "program_name": program_name,
                    "included": False,
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