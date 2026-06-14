from llm import llm
import json
from collections import defaultdict

SYSTEM_PROMPT = """You are a tweet writer for a CS student who builds real projects. Given a list of commit summaries from a single repository, decide if there is something genuinely interesting worth tweeting about.
If yes, write 1-3 tweet options. if no send "SKIP"
If there is anything even mildly interesting or relatable about the work done, write tweet options. Only respond with SKIP if the commits are purely trivial (single value tweaks, typo fixes, dependency bumps with no context). When in doubt, tweet.
Rules:
- Sound like a person, not a changelog
- No hashtags, no emojis, no hustle-bro energy
- Curiosity and dry wit over enthusiasm
- Talk about what you were actually trying to solve, not just what you changed
- Trivial commits (style tweaks, config nudges) are not worth a tweet unless there are many of them forming a pattern
- Short is better. One punchy sentence often beats three explanatory ones
- Do not mention the repo name or commit messages directly
Context: the person builds ML tools, systems projects, and full stack apps. They are interested in how things work at a fundamental level."""

def getTweet(activity):
    summaries = [i["llm_summary"] for i in activity if i["llm_summary"]]
    if not summaries:
        return None
    user_prompt = "\n".join(f"- {s}" for s in summaries)
    return llm(system=SYSTEM_PROMPT, user=user_prompt, model="qwen/qwen3.6-flash")

def getTweetsByRepo(activity):
    grouped = defaultdict(list)
    for item in activity:
        key = (item["reponame"], item["datetime"].date())
        grouped[key].append(item)
    
    results = {}
    for (repo, date), items in grouped.items():
        results[(repo, date)] = getTweet(items)
    
    return results
