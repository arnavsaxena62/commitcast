import pickle
import dotenv
from openai import OpenAI
import os
import time
import logging

logger = logging.getLogger(__name__)

dotenv.load_dotenv()
key = os.getenv('API_KEY')

if not key:
    raise ValueError("API_KEY not found in environment")

client = OpenAI(
    api_key=key,
    base_url="https://openrouter.ai/api/v1"
)

def llm(system, user, model="openrouter/free"):
    logger.info(f"calling model {model}")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        time.sleep(0.5)
        result = response.choices[0].message.content
        logger.debug(f"response: {result}")
        return result
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return None

def diffSummary(diff):
    logger.info("summarising diff")
    systemPrompt = "You are a technical summarizer. Given a git diff patch, write a single sentence describing what was actually changed and why, in plain English. Mention the specific file(s) changed. If the change is trivial (typo fix, minor style tweak, config value nudge), prefix with 'trivial:'. Be concise and literal. Do not editorialize."
    result = llm(systemPrompt, diff)
    if result is None:
        logger.warning("diffSummary returned None")
    return result

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler("commitcast.log"),
            logging.StreamHandler()
        ]
    )
    try:
        with open("example.pkl", "rb") as file:
            activity = pickle.load(file)
        logger.info(f"loaded {len(activity)} events")
        print(diffSummary(activity[0]['patch']))
    except FileNotFoundError:
        logger.error("example.pkl not found — run github.py first")
    except Exception as e:
        logger.error(f"unexpected error: {e}")
