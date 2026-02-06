import argparse
from pathlib import Path
import sys
import pandas as pd
import ollama

# A chosen test file from each Tests4Py project 
TEST_FILES = {
    "ansible": "test/units/errors/test_errors.py", 
    "black": "tests/test_black.py", 
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
    "pandas": "pandas/tests/arithmetic/test_numeric.py", ##
    "pysnooper": "tests/test_pysnooper.py", 
    "sanic": "tests/test_middleware.py", 
    "scrapy": "tests/test_command_fetch.py", 
    "spacy": "spacy/tests/tokenizer/test_tokenizer.py", ##
    "thefuck": "tests/test_logs.py", 
    "tornado": "tornado/test/escape_test.py", 
    "tqdm": "tqdm/tests/tests_tqdm.py",
    "youtubedl": "test/test_age_restriction.py"
}

# Large Language Models (LLMs) options
LLAMA = "llama3.1:8b"


# OLD PRACTICE CODE: (to be removed later)
'''
desired_model = "llama3.1:8b"
prompt = "What is one plus two?" # this is a test, not to be used for final code!

response = ollama.chat(model=desired_model, messages=[
    {
        "role": "user",
        "content": prompt,
    },
])

ollama_response = response["message"]["content"]
print(ollama_response)

with open("C:/CAPSTONE/Automated-Test-Generation-Using-LLM/tmp_practice/OUTPUT/OutputOllama.txt", "w", encoding="utf-8") as text_file:
    text_file.write(ollama_response)
'''


# Prompt an LLM to generate an extended test class file and output it to same path as the original test class
def main():
    parser = argparse.ArgumentParser(description = "generate and output extended test file")
    
    '''
    parser.add_argument(
        "-m", "--model",
        default="llama",
        help="select an LLM to generate extended test file(s).",
    )
    '''
    
    parser.add_argument(
        "-p", "--project",
        help="generate extended test file for a single project."
    )
    
    # Directory paths
    args = parser.parse_args()
    scripts_dir = Path(__file__).absolute().parent
    tmp_dir = scripts_dir / "tmp"
    results_dir = scripts_dir.parent / "results"
    results_csv = results_dir / "results.csv"
    
    df_tmp = pd.read_csv(results_csv)
    df = df_tmp[df_tmp["usable"] == True]

    # Select a single project only
    if args.project:
        df = df[df["program_name"].str.startswith(args.project + "_")]
    
    print(f"MODEL: {args.model}")

    for index, row in df.iterrows():
        # Get the program names in selected project (e.g. ansible_1, ansible_2, ...)
        program_name = row["program_name"]
        project = program_name.split("_")[0]
        
        project_dir = tmp_dir / program_name
        original_test_file = project_dir / TEST_FILES[project]
        existing_test_class = original_test_file.read_text(encoding="utf-8")
        
        prompt = f"""
        Here is a Python unit test class:

        {existing_test_class}

        Write an extended version of the test class that includes additional tests to cover some extra corner cases.

        OUTPUT FORMAT (required):
        - OUTPUT ONLY PYTHON CODE.
        - Do NOT include explanations or comments outside the code.
        - Do NOT wrap the code in backticks (```).
        - The output must be runnable with pytest.
        """
        
        print(f"GENERATING EXTENDED TEST FOR {program_name} ...")
        
        if (args.model == "llama"):
            # Prompt Llama to generate an extended test suite
            try:
                response = ollama.chat(model=LLAMA, messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ])
                
                ollama_response = response["message"]["content"]
                print(ollama_response)
                
                # write to file
                
                print(f"SUCCESS: GENERATED TEST FOR {program_name} ...\n")
            
            except Exception as e:
                print(f"**ERROR: FAILED TO GENERATE FOR {program_name} ...\n")
                continue
            
    # df.to_csv(file_path, index=False)

if __name__ == "__main__":
    main()