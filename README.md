# Automated-Test-Generation-Using-LLM

This repository contains scripts for a replication study of Meta’s LLM-based automated unit test generation method [1], evaluated on the Tests4Py benchmark [2] using Python and pytest.

The goal of this research project is to evaluate whether applying the same method described in Meta’s study results in success rate trends on the Tests4Py benchmark.

## Installation

The `requirements.txt` file lists all Python libraries required for this project.
Install them using:

```bash
pip install -r requirements.txt
```

To use the [Tests4Py](https://github.com/smythi93/Tests4Py?tab=readme-ov-file) CLI (`t4p`), activate the virtual environment using:

```bash
.\.venv\Scripts\Activate.ps1
```

## Scripts

- [p01_setup.py](scripts/p01_setup.py) Add all Tests4Py projects (or a single project using --project, -p) into tmp/.

- [p02_baseline_coverage.py](scripts/p02_baseline_coverage.py) Run a test class for each Tests4Py project (or a single project using --project, -p).

- p03_generate_llm_tests.py

- p04_llm_coverage.py

- p05_filters.py

- p06_analysis.py
  
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