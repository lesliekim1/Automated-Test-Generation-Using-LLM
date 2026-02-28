#!/usr/bin/env bash
# Automate running all filters py files (p04 - p07)
# run: ./run_filters.sh <project>

PROJECT="$1"

if [ -z "$PROJECT" ]; then
    echo "Usage: $0 <project>"
    exit 1
fi

echo "Running pipeline for project: $PROJECT"
echo

for f in results/results_LLAMA_*.csv; do
    name=$(basename "$f")

    echo "===================================="
    echo "Processing: $name"
    echo "===================================="

    echo "---- BUILD FILTER ----"
    python3 p04_build_filter.py -p "$PROJECT" -f "$name"
    echo "---- PASS FILTER ----"
    python3 p05_pass_filter.py -p "$PROJECT" -f "$name"
    echo "---- LLM COVERAGE ----"
    python3 p06_llm_coverage.py -p "$PROJECT" -f "$name"
    echo "---- COVERAGE IMPROVEMENT FILTER ----"
    python3 p07_coverage_improvement_filter.py -p "$PROJECT" -f "$name"
done

echo "all filters done"