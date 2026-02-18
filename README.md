# Automated-Test-Generation-Using-LLM

This repository contains scripts for a replication study of Meta’s TestGen-LLM method [1], using Python and pytest. Its purpose is to evaluate whether applying Meta's TestGen-LLM method on the Tests4Py benchmark [2] results in similar overall and filter success rates on the Tests4Py benchmark to those reported in Meta's study.

## Installation

The `requirements.txt` file lists all Python libraries required for this project.
Install them using:

```bash
pip install -r requirements.txt
```

To use the [Tests4Py](https://github.com/smythi93/Tests4Py?tab=readme-ov-file) CLI (`t4p`), activate the virtual environment using:

```bash
.venv\Scripts\activate
```

### Ollama

This project uses [Ollama](https://ollama.com/) to run large language models locally for automated test generation. Install the models:
- [llama3.2:3b](https://ollama.com/library/llama3.2:3b)

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
  -n, --number NUMBER     1 = extend_test, 2 = extend_coverage, 3 = corner_cases, 4 = statement_to_complete
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

- p08_analysis.py
  
## References

[1] N. Alshahwan, J. Chheda, A. Finogenova, B. Gokkaya, M. Harman,
I. Harper, A. Marginean, S. Sengupta, and E. Wang. Automated unit
test improvement using large language models at meta. In 32nd ACM
International Conference on the Foundations of Software Engineering,
FSE 2024, page 185–196, New York, NY, USA, 2024. Association for
Computing Machinery.

[2] M. Smytzek, M. Eberlein, B. Serc¸e, L. Grunske, and A. Zeller. Tests4py:
A benchmark for system testing. In 32nd ACM International Conference
on the Foundations of Software Engineering (FSE), FSE 2024,
page 557–561, New York, NY, USA, 2024. Association for Computing
Machinery.

## License 
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
