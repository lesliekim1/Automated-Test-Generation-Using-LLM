#!/bin/bash
# Automate running p03_generate_llm_tests.py
# run: ./run_llm.sh

echo "---- CORNERCASES ----"
python p03_generate_llm_tests.py -f results_DEEPSEEK_CORNERCASES.py -n 3
echo "---- EXTENDCOV ----"
python p03_generate_llm_tests.py -f results_DEEPSEEK_EXTENDCOV.py -n 2
echo "---- EXTENDTEST ----"
python p03_generate_llm_tests.py -f results_DEEPSEEK_EXTENDTEST.py -n 1
echo "---- STATEMENTCOMPLETE ----"
python p03_generate_llm_tests.py -f results_DEEPSEEK_STATEMENTCOMPLETE.py -n 4