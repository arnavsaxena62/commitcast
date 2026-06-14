import pickle
import dotenv
from openai import OpenAI
import os
import time
import logging

dotenv.load_dotenv()
key = os.getenv('API_KEY')


client = OpenAI(
    api_key=key,
    base_url="https://openrouter.ai/api/v1"
)

def llm(system, user, model="openrouter/free"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    time.sleep(0.5)
    return response.choices[0].message.content

def diffSummary(diff):
    systemPrompt = "You are a technical summarizer. Given a git diff patch, write a single sentence describing what was actually changed and why, in plain English. Mention the specific file(s) changed. If the change is trivial (typo fix, minor style tweak, config value nudge), prefix with 'trivial:'. Be concise and literal. Do not editorialize."
    return llm(systemPrompt, diff)

with open("example.pkl", "rb") as file:
    activity = pickle.load(file)

print(diffSummary(activity[0]['patch']))

