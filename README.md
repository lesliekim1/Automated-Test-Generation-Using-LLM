# Automated-Test-Generation-Using-LLM

This repository contains scripts for a replication study of [Meta’s TestGen-LLM](https://arxiv.org/abs/2402.09171), using Python and pytest. Its purpose is to evaluate whether applying Meta's TestGen-LLM method on the [Tests4Py benchmark](https://arxiv.org/abs/2307.05147) results in similar overall and filter success rates on the Tests4Py benchmark to those reported in Meta's study.

## Installation

The `requirements.txt` file lists all Python libraries required for this project.
Install them using:

```bash
pip install -r requirements.txt
```

### Ollama

This project uses [Ollama](https://ollama.com/) to run large language models locally for automated test generation. Install the model(s):
- [llama3.2:3b](https://ollama.com/library/llama3.2:3b)

## Running 
To use the [Tests4Py](https://github.com/smythi93/Tests4Py?tab=readme-ov-file) CLI (`t4p`) and run this project, activate the virtual environment using:

```bash
source .venv/Scripts/activate
```

To run all filters for a project (e.g. ./run_filters.sh calculator ansible):

```bash
cd scripts
./run_filters.sh <project1> <project2> <project3> ...
```

## Scripts

[p01_setup.py](scripts/p01_setup.py)
```bash
usage: p01_setup.py [-h] [-p PROJECT]

checkout all Tests4Py projects.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   checkout a single project.
```
  
[p02_baseline_coverage.py](scripts/p02_baseline_coverage.py)
```bash
usage: p02_baseline_coverage.py [-h] [-p PROJECT]

get statement coverage of a test class from each Tests4Py project.

options:
  -h, --help              show this help message and exit
  -p, --project PROJECT   get statment coverage for a single project.
```

[p03_generate_llm_tests.py](scripts/p03_generate_llm_tests.py)
```bash
usage: p03_generate_llm_tests.py [-h] [-m MODEL] [-p PROJECT] [-n NUMBER] [-f FILE]

generate and save extended test class to same path as original test class.

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

p08_analysis.py

## License 
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
