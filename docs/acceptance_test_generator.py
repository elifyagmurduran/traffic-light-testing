import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # change if using mistral


TEMPLATE_PROMPT = """
You are a software requirements engineer.

Using the following template, create an Acceptance Test table
for EACH assertion found in the User Story.

Use EXACTLY this structure:

| AT name: <testName> | | |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Input | Description | Expected behavior |
| ... | ... | ... |
| ... | ... | ... |
| | | |
| Invalid condition description | Description | Expected behavior |
| US name: <UserStoryName> | | |

Rules:
- One Acceptance Test per assertion
- Include valid case
- Include invalid case
- Keep the format identical
- Do NOT explain anything
- Output only tables
"""


def generate_acceptance_tests(user_story_text):
    prompt = TEMPLATE_PROMPT + "\n\nUser Story:\n" + user_story_text

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


if __name__ == "__main__":

    with open("UserStories.txt", "r") as f:
        user_story = f.read()

        result = generate_acceptance_tests(user_story)

        print(result)

        # Optional: Save to file
        with open("acceptance_tests_output.md", "w") as f:
            f.write(result)