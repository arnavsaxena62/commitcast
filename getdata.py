import requests
from datetime import datetime
import pickle

url = 'https://api.github.com/users/arnavsaxena62/events'
headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version":"2026-03-10",
}
query = {"per_page":100}

response = requests.get(url, headers=headers, params=query)
data = response.json()

activity = []

for i in data:
    if i["type"] in ["PushEvent"]:
        before = i["payload"]["before"]
        head = i["payload"]["head"]
        repourl = i["repo"]["url"]
        dt = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%SZ")

        repoCommitData = requests.get(f"{repourl}/compare/{before}...{head}").json()
        commit_msg = repoCommitData["base_commit"]["commit"]["message"]
        patchData = requests.get(repoCommitData["patch_url"]).text
        repoData = requests.get(repourl).json()
        repoDescription = repoData["description"]
        repoName = repoData["name"]

        print(patchData, repoDescription, repoName, commit_msg)

        activity.append({
            "reponame" : repoName,
            "repoDescription" : repoDescription,
            "datetime": dt,
            "commitmsg" : commit_msg,
            "patch" : patchData
        })

with open("example.pkl", "wb") as file:
    pickle.dump(activity, file)
