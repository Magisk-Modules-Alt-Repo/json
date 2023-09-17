import sys
import json
import os
from github import Github
from datetime import datetime

# Configuration
REPO_NAME = "Magisk-Modules-Alt-Repo"
REPO_TITLE = "Magisk Modules Alt Repo"
REPO_SUBMIT = "https://github.com/Magisk-Modules-Alt-Repo/submission"

# Skeleton for the repository
meta = {
    "name": REPO_TITLE,
    "submitModule": REPO_SUBMIT,
    "last_update": "",
    "modules": []
}

# Initialize the GitHub objects
g = Github(os.environ['GIT_TOKEN'])
user = g.get_user(REPO_NAME)
repos = user.get_repos()

# Fetch the last repository update
meta["last_update"] = int(user.updated_at.timestamp() * 1000)

# Iterate over all public repositories
for repo in repos:
    # It is possible that module.prop does not exist (meta repo)
    try:
        # Parse module.prop into a python object
        moduleprop_raw = repo.get_contents("module.prop").decoded_content.decode("UTF-8")
        moduleprop = {}
        for line in moduleprop_raw.splitlines():
            if "=" not in line:
                continue
            lhs, rhs = line.split("=", 1)
            moduleprop[lhs] = rhs
        
        # Get the last update timestamp of the module.prop file
        last_update_timestamp = repo.get_contents("module.prop").last_modified

        # Convert the string to a datetime object
        last_update_datetime = datetime.strptime(last_update_timestamp, '%a, %d %b %Y %H:%M:%S %Z')

        # Get the timestamp of the last update
        last_update_timestamp = datetime.timestamp(last_update_datetime)

        # Create meta module information
        module = {
            "id": moduleprop["id"],
            "last_update": int(last_update_timestamp * 1000),
            "prop_url": f"https://raw.githubusercontent.com/{repo.full_name}/{repo.default_branch}/module.prop",
            "zip_url": f"https://github.com/{repo.full_name}/archive/{repo.default_branch}.zip",
            "notes_url": f"https://raw.githubusercontent.com/{repo.full_name}/{repo.default_branch}/README.md",
            "stars": int(repo.stargazers_count)
        }

        # Append to skeleton
        meta["modules"].append(module)
    except:
        continue

# Return our final skeleton
print(json.dumps(meta, indent=4, sort_keys=True))
