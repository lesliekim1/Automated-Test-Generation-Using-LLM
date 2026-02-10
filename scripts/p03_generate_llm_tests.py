import argparse
from pathlib import Path
import sys
import pandas as pd
import ollama

# A chosen test file from each Tests4Py project 
TEST_FILES = {
    "ansible": "test/units/errors/test_errors.py", #
    "black": "tests/test_black.py", #
    "calculator": "tests/test_calc.py", 
    "cookiecutter": "tests/test_generate_file.py", 
    "expression": "tests/test_expression.py", 
    "fastapi": "tests/test_jsonable_encoder.py", 
    "httpie": "tests/test_exit_status.py", 
    "keras": "tests/test_loss_masking.py", 
    "luigi": "test/factorial_test.py", 
    "markup": "tests/test_markup.py", 
    "matplotlib": "lib/matplotlib/tests/test_container.py", 
    "middle": "tests/test_middle.py", 
    "pandas": "pandas/tests/arithmetic/test_numeric.py", 
    "pysnooper": "tests/test_pysnooper.py", 
    "sanic": "tests/test_middleware.py", 
    "scrapy": "tests/test_command_fetch.py", 
    "spacy": "spacy/tests/tokenizer/test_tokenizer.py",
    "thefuck": "tests/test_logs.py", 
    "tornado": "tornado/test/escape_test.py", 
    "tqdm": "tqdm/tests/tests_tqdm.py",
    "youtubedl": "test/test_age_restriction.py"
}

# A chosen "class under test" (CUT) file to give the LLM an example reference
CUT_FILES = {
    "ansible": "build/lib/ansible/errors/__init__.py", 
    "black": "black.py", 
    "calculator": "src/calc/__init__.py", 
    "cookiecutter": "cookiecutter/generate.py", 
    "expression": "src/expression/expr/arithmetic.py", 
    "fastapi": "fastapi/encoders.py", 
    "httpie": "httpie/cli.py", 
    "keras": "keras/losses.py", 
    "luigi": "luigi/interface.py", 
    "markup": "src/markup/__init__.py", 
    "matplotlib": "lib/matplotlib/container.py", 
    "middle": "src/middle/__init__.py", 
    "pandas": "pandas/core/indexes/numeric.py", 
    "pysnooper": "pysnooper/tracer.py", 
    "sanic": "sanic/app.py", 
    "scrapy": "scrapy/commands/fetch.py", 
    "spacy": "spacy/util.py", 
    "thefuck": "thefuck/logs.py", 
    "tornado": "tornado/escape.py", 
    "tqdm": "tqdm/std.py",
    "youtubedl": "youtube_dl/YoutubeDL.py"
}

# LLMs options
LLMS = {
    "llama": "llama3.2:3b"
    #deepseek-coder:1.3b
}

# Purpose: Check if project input is valid.
# Parameters: project (project from argument)
# Return: end program if invalid
def validate_project(project):
    if project:
        if project not in TEST_FILES:
            sys.exit(
                f"Unknown project: {project}\n"
                "Available Tests4Py projects:\n" +
                "\n".join(sorted(TEST_FILES.keys()))
            )  

# Purpose: Check if LLM model is valid.
# Parameters: model (model from argument)
# Return: end program if invalid
def validate_model(model):
    if model not in LLMS:
        sys.exit(
            f"Available LLMs:\n" +
            "\n".join(sorted(LLMS.keys()))
        )   

# Prompt an LLM to generate an extended test class file and output it to same path as the original test class
def main():
    parser = argparse.ArgumentParser(description = "generate and save extended test class to same path as original test class.")
    
    parser.add_argument(
        "-m", "--model",
        default="llama",
        help="select an LLM to generate extended test file(s).",
    )
    
    parser.add_argument(
        "-p", "--project",
        help="generate extended test file for a single project."
    )
    
    parser.add_argument(
        "-n", "--number",
        default="1",
        help="1 = test only, any other value = test and class under test."
    )
    
    # Check valid argument(s)
    args = parser.parse_args()
    validate_project(args.project)
    validate_model(args.model)
    
    scripts_dir = Path(__file__).absolute().parent
    tmp_dir = scripts_dir / "tmp"
    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / "results.csv"
    
    # Read results.csv and iterate through 'usable' projects only (projects that have coverage_before)
    df = pd.read_csv(results_csv)
    
    df["llm_test_file"] = df["llm_test_file"].astype("string")
    df_usable = df[(df["usable"] == True) & df["llm_test_file"].isna()]
    df["prompt_mode"] = df["prompt_mode"].astype("string")

    # Select a single project only
    if args.project:
        df_usable = df_usable[df_usable["program_name"].str.startswith(args.project + "_")]
    
    print(f"MODEL: {LLMS[args.model]}")
    
    # TESTONLY = test class only file used, TESTCUT = test class and class under test files used
    prompt_mode = str(args.number)
    if prompt_mode == "1":
        mode = "TESTONLY"
    else:
        mode = "TESTCUT"
    print(f"PROMPT MODE: {mode}")

    for index, row in df_usable.iterrows():
        # Get the program names in selected project (e.g. ansible_1, ansible_2, ...)
        program_name = row["program_name"]
        project = program_name.split("_")[0]
        
        project_dir = tmp_dir / program_name
        original_test_file = project_dir / TEST_FILES[project]
        existing_test_class = original_test_file.read_text(encoding="utf-8")
        
        # Test only mode
        if (prompt_mode == "1"):
            df.loc[df["program_name"] == program_name, "prompt_mode"] = mode
            
            # Prompt is the same as from Meta's study (output format is instructions for LLM)
            prompt = f"""
            Here is a Python unit test class:

            {existing_test_class}

            Write an extended version of the test class that includes additional tests to cover some extra corner cases.

            OUTPUT FORMAT (required):
            - OUTPUT ONLY PYTHON CODE.
            - Do NOT include explanations or comments outside the code.
            - Do NOT wrap the code in backticks (```).
            """
    
        # Test and class under test mode
        else:
            class_under_test_file = project_dir / CUT_FILES[project]
            class_under_test = class_under_test_file.read_text(encoding="utf-8")
            df.loc[df["program_name"] == program_name, "prompt_mode"] = mode
            
            # Prompt is the same as from Meta's study (output format is instructions for LLM)
            prompt = f"""
            Here is a Python unit test class and the class that it tests:

            {existing_test_class}
            
            {class_under_test}

            Write an extended version of the test class that includes additional unit tests that will increase the test coverage of the class under test.

            OUTPUT FORMAT (required):
            - OUTPUT ONLY PYTHON CODE.
            - Do NOT include explanations or comments outside the code.
            - Do NOT wrap the code in backticks (```).
            """
        
        print(f"GENERATING EXTENDED TEST FOR {program_name} ...")
        output_file = original_test_file.with_name(original_test_file.stem + "_" + args.model.upper() + "_" + mode + ".py")
         
        # Prompt an LLM (default: Llama) to generate an extended test suite
        try:
            response = ollama.chat(model=LLMS[args.model], messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ])
                
            llm_response = response["message"]["content"]               
            print(f"SUCCESS: GENERATED TEST FOR {program_name} ...\n\t--> {output_file}\n")
            
        except Exception as e:
            print(f"**ERROR: FAILED TO GENERATE FOR {program_name}: {e} ...\n")
            continue
            
        # Output to file in same path as the original test class
        with open(output_file, "w", encoding="utf-8") as py_file:
            py_file.write(llm_response)
            
        df.loc[df["program_name"] == program_name, "llm_test_file"] = output_file.name  
        df.to_csv(results_csv, index=False)
    
if __name__ == "__main__":
    main()