import ollama

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