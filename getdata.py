import requests
from datetime import datetime, timedelta, timezone
import pickle
from llm import diffSummary
import logging

logger = logging.getLogger(__name__)

GITHUB_URL = 'https://api.github.com/users/arnavsaxena62/events'
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
}
LOOKBACK_DAYS = 3

def fetch_activity():
    response = requests.get(GITHUB_URL, headers=HEADERS, params={"per_page": 100})
    data = response.json()

    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    activity = []

    for i in data:
        if i["type"] != "PushEvent":
            continue

        dt = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

        if dt < cutoff:
            logger.info(f"skipping old event from {dt} (cutoff: {cutoff})")
            continue

        before = i["payload"]["before"]
        head = i["payload"]["head"]
        repourl = i["repo"]["url"]
        logger.info(f"processing push event for {i['repo']['name']} at {dt}")

        repoCommitData = requests.get(f"{repourl}/compare/{before}...{head}").json()
        patchData = requests.get(repoCommitData["patch_url"]).text
        repoData = requests.get(repourl).json()

        commit_msg = repoCommitData["base_commit"]["commit"]["message"]
        repoDescription = repoData["description"]
        repoName = repoData["name"]

        logger.info(f"summarising patch for {repoName}: {commit_msg}")
        patchdescription = diffSummary(patchData)
        logger.debug(f"summary: {patchdescription}")

        activity.append({
            "reponame": repoName,
            "repoDescription": repoDescription,
            "datetime": dt,
            "commitmsg": commit_msg,
            "patch": patchData,
            "llm_summary": patchdescription
        })
        logger.info(f"added {repoName} to activity")

    return activity

def save_activity(activity, path="example.pkl"):
    with open(path, "wb") as f:
        pickle.dump(activity, f)
    logger.info(f"saved {len(activity)} events to {path}")

if __name__ == "__main__":
    activity = fetch_activity()
    save_activity(activity)
