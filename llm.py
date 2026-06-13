import pickle
import dotenv
from openai import OpenAI
import os

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
    return response.choices[0].message.content

print(llm("hey", "hello"))
