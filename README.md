# Automated-Test-Generation-Using-LLM

This repository contains scripts for a replication study of [Meta’s TestGen-LLM](https://arxiv.org/abs/2402.09171), implemented using Python and pytest. The goal is to evaluate whether applying the TestGen-LLM method to the [Tests4Py benchmark](https://arxiv.org/abs/2307.05147) produces similar overall and filter success rates as those reported in Meta’s study.

## Experiment

For each trial (a buggy project version from Tests4Py):

1. Baseline coverage is measured using the original test suite.
2. The LLM generates extended tests using multiple prompt styles.
3. Generated tests are filtered through:
   - Build filter (test must run without errors using pytest --collect-only)
   - Pass filter (run 5 times with pytest to detect flakiness)
   - Coverage improvement filter (must increase statement coverage)
4. Results are recorded in a CSV file, including coverage before/after and filter success outcomes.
5. Final analysis computes overall and filter success rates.

## Installation

The `requirements.txt` file lists all Python libraries required for this project.
Install them using:

```bash
pip install -r requirements.txt
```

### Ollama

This project uses [Ollama](https://ollama.com/) to run large language models locally for automated test generation. Install the model(s):
- [llama3.2:3b](https://ollama.com/library/llama3.2:3b)
- [deepseek-coder:6.7b](https://ollama.com/library/deepseek-coder:6.7b)

## Running 
To use the [Tests4Py](https://github.com/smythi93/Tests4Py?tab=readme-ov-file) CLI (`t4p`) and run this project, activate the virtual environment using:

```bash
source .venv/Scripts/activate
```

To automate running all filter files for one or more projects (e.g. ./run_filters.sh calculator ansible):

```bash
./run_filters.sh <project1> <project2> <project3> ...
```

## Scripts

[p01_setup.py](scripts/p01_setup.py)
```bash
usage: p01_setup.py [-h] [-p PROJECT]

set up the experiment by installing all Tests4Py projects and their corresponding versions.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   checkout a single project.
```
  
[p02_baseline_coverage.py](scripts/p02_baseline_coverage.py)
```bash
usage: p02_baseline_coverage.py [-h] [-p PROJECT]

get baseline statement coverage of a test class from each Tests4Py project.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   get statement coverage for a single project.
```

[p03_generate_llm_tests.py](scripts/p03_generate_llm_tests.py)
```bash
usage: p03_generate_llm_tests.py [-h] [-m MODEL] [-p PROJECT] [-n NUMBER] [-f FILE]

generate an LLM extended test class using the selected model and prompt, and save it to the same path as the original test class.

options:
  -h, --help              show this help message and exit
  -m, --model MODEL       select an LLM to generate extended test file(s).
  -p, --project PROJECT   generate extended test file for a single project.
  -n, --number NUMBER     prompts: 1 = extend_test, 2 = extend_coverage, 3 = corner_cases, 4 = statement_to_complete
  -f, --file FILE         CSV filename in results directory that records the data.
```

[p04_build_filter.py](scripts/p04_build_filter.py)
```bash
usage: p04_build_filter.py [-h] [-p PROJECT] [-f FILE]

check if an LLM-generated test class is built correctly.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   apply build filter to a single project.
  -f, --file FILE         CSV filename in results directory that records the data.
```

[p05_pass_filter.py](scripts/p05_pass_filter.py)
```bash
usage: p05_pass_filter.py [-h] [-p PROJECT] [-f FILE]

check for any flaky behavior by executing the LLM-generated test five times.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   apply build filter to a single project.
  -f, --file FILE         CSV filename in results directory that records the data.
```

[p06_llm_coverage.py](p06_llm_coverage.py)
```bash
usage: p06_llm_coverage.py [-h] [-p PROJECT] [-f FILE]

get statement coverage of a LLM-generated test class from each Tests4Py project.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   get statement coverage for a single project.
  -f, --file FILE         CSV filename in results directory that records the data.
```

[p07_coverage_improvement_filter.py](p07_coverage_improvement_filter.py)
```bash
usage: p07_coverage_improvement_filter.py [-h] [-p PROJECT] [-f FILE]

check for if coverage improvement has occurred on LLM-generated tests.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   run coverage improvement filter for a single project.
  -f, --file FILE         CSV filename in results directory that records the data.
```

[p08_analysis.py](p08_analysis.py)
```bash
usage: p08_analysis.py [-h] [-f FILE]

create tables to display the results (overall success rate and each filter success rates).

options:
  -h, --help              show this help message and exit
  -f FILE, --file FILE    CSV filename in results directory that records the data.
```

## License 
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
