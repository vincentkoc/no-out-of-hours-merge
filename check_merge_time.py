import datetime
import json
import os
import sys
from typing import Dict, List, Tuple

import pytz
from github import Github

def post_comment_on_pr(github_token: str, pr_number: int, message: str) -> None:
    gh = Github(github_token)
    repo = gh.get_repo(os.environ["GITHUB_REPOSITORY"])
    pr = repo.get_pull(pr_number)
    comments = pr.get_issue_comments()

    existing_comment_id = None
    for comment in comments:
        if comment.body == message:
            existing_comment_id = comment.id
            break

    if not existing_comment_id:
        pr.create_issue_comment(message)

def main():
    # Get the inputs from the environment
    github_token = os.environ["GITHUB_TOKEN"]
    pr_title = os.environ["CI_PR_TITLE"]
    timezone = os.environ.get("TIMEZONE", "Australia/Sydney")
    restricted_times_json = os.environ.get("RESTRICTED_TIMES", None)
    custom_message = os.environ.get("CUSTOM_MESSAGE", "⚠️ **PR merging is not allowed outside business hours.** ⚠️")

    if restricted_times_json:
        restricted_times = json.loads(restricted_times_json)
    else:
        restricted_times = {
            "mon": [(0, 7), (16.5, 24)],
            "tue": [(0, 7),
        "wed": [(0, 7), (16.5, 24)],
        "thu": [(0, 7), (16.5, 24)],
        "fri": [(0, 7), (16.5, 24)],
        "sat": [(0, 24)],
        "sun": [(0, 24)],
    }

tz = pytz.timezone(timezone)

now = datetime.datetime.now(tz)
weekday = now.strftime("%a").lower()
hour = now.hour + (now.minute / 60)

if any(start <= hour < end for start, end in restricted_times[weekday]):
    print("❌ Merging is not allowed during the specified time.")
    pr_number = int(os.environ["GITHUB_PR_NUMBER"])
    post_comment_on_pr(github_token, pr_number, custom_message)
    sys.exit(1)
else:
    print("✅ Merging is allowed at this time.")
    sys.exit(0)

if name == "main":
main()

