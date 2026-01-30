import argparse
from pathlib import Path
import sys
import subprocess

# project: num bugs
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
    parser = argparse.ArgumentParser(description = "checkout all Tests4Py programs.")

    parser.add_argument(
        "-p", "--project",
        help="checkout only one project."
    )

    args = parser.parse_args()
    root_dir = Path(__file__).absolute().parent
    t4p = root_dir /".venv" / "Scripts" / "t4p.exe"

    # Ensure that tmp folder exists
    tmp_dir = root_dir / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    # Use a single project
    if args.project and args.project not in PROJECTS:
        sys.exit(f"Unknown project: '{args.project}'.\nTests4Py projects: {"\n".join((PROJECTS.keys()))}")
        t4p_projects = {args.project: PROJECTS[args.project]} 
    
    # Use all projects
    else:
        t4p_projects = PROJECTS
    
    for project, num_bugs in t4p_projects.items():
        for bug_id in range(num_bugs):
            print(f"checkout {project} #{bug_id}... ")
            
            result = subprocess.run(
                [t4p, "checkout", "-p", project, "-i", str(bug_id), "-w", str(tmp_dir)],
                cwd=str(root)
            )

    print("\ndone")

if __name__ == "__main__":
    main()