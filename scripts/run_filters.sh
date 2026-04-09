#!/bin/bash
# Automate running all filters py files (p04 - p07)
# run: ./run_filters.sh <project1> <project2> <project3> ...
# example: ./run_filters.sh calculator

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <project1> <project2> <project3> ..."
    exit 1
fi

FILES=(
  results_DEEPSEEK_CORNERCASES.csv
  results_DEEPSEEK_EXTENDCOV.csv
  results_DEEPSEEK_EXTENDTEST.csv
  results_DEEPSEEK_STATEMENTCOMPLETE.csv
)

for PROJECT in "$@"; do
    echo
    echo "PROJECT: $PROJECT"

    for name in "${FILES[@]}"; do
        echo
        echo "RUNNING FILTERS FOR: $name"

        echo "---- BUILD FILTER ----"
        python3 p04_build_filter.py -p "$PROJECT" -f "$name"
        echo "---- PASS FILTER ----"
        python3 p05_pass_filter.py -p "$PROJECT" -f "$name"
        echo "---- GETTING COVERAGE FROM LLM-GENERATED EXTENDED TEST ----"
        python3 p06_llm_coverage.py -p "$PROJECT" -f "$name"
        echo "---- COVERAGE IMPROVEMENT FILTER ----"
        python3 p07_coverage_improvement_filter.py -p "$PROJECT" -f "$name"
    done
done