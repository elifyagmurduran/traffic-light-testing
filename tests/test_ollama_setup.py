import ollama

prompt = "What is the capital of France?"

response = ollama.chat(
    model="llama3:latest",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])