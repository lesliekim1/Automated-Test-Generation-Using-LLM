import argparse
from pathlib import Path
import sys
import subprocess

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

# Purpose: Get all selected projects to be retrieved.
# Parameters: project (project from argument)
# Return: dict of projects
def select_projects(project):
    # Single project
    if project:
        if project not in PROJECTS:
            sys.exit(f"Unknown project: {project}\nTests4Py projects:\n" + "\n".join(PROJECTS.keys()))
        chosen_projects = {project: PROJECTS[project]} 
        
    # All projects
    else:
        chosen_projects = PROJECTS
    return chosen_projects

# Purpose: Retrieve all chosen project(s) by using t4p checkout.
# Parameters: chosen_projects (projects to be retrieved), t4p (t4p executable), 
#             tmp_dir (tmp folder), scripts_dir (scripts folder)
# Return: none
def t4p_checkout(chosen_projects, t4p, tmp_dir, scripts_dir):
    for project, num_bugs in chosen_projects.items():
        for bug_id in range(1, num_bugs+1):
            print(f"RUNNING: t4p checkout -p {project} -i {bug_id} -w scripts/tmp ... ")

            subprocess.run(
                [str(t4p), "checkout", "-p", project, "-i", str(bug_id), "-w", str(tmp_dir)],
                cwd=str(scripts_dir)
            )

# Retrieve and add Tests4Py project(s) into tmp folder using t4p checkout. 
def main():
    parser = argparse.ArgumentParser(description = "checkout all Tests4Py projects.")

    parser.add_argument(
        "-p", "--project",
        help="checkout a single project."
    )

    args = parser.parse_args()
    scripts_dir = Path(__file__).absolute().parent
    t4p = scripts_dir.parent /".venv" / "Scripts" / "t4p.exe"

    # Create tmp dir to store Tests4Py projects
    tmp_dir = scripts_dir / "tmp"
    tmp_dir.mkdir(exist_ok=True)
     
    chosen_projects = select_projects(args.project)
    
    # t4p checkout all chosen project(s)
    t4p_checkout(chosen_projects, t4p, tmp_dir, scripts_dir)

if __name__ == "__main__":
    main()