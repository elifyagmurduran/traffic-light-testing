import requests

r = requests.post("http://localhost:11434/api/generate",
                  json={"model": "llama3", "prompt": "Say hello in 3 words.", "stream": False})
print(r.json()["response"])