import datetime
import json
import os
import sys
from typing import Dict, List, Tuple

import pytz
from github import Github

def post_comment_on_pr(github_token: str, pr_number: int, message: str, check_existing_comment: bool) -> None:
    gh = Github(github_token)
    repo = gh.get_repo(os.environ["GITHUB_REPOSITORY"])
    pr = repo.get_pull(pr_number)
    comments = pr.get_issue_comments()

    existing_comment_id = None
    if check_existing_comment:
        for comment in comments:
            if comment.body == message:
                existing_comment_id = comment.id
                break

    if not existing_comment_id:
        pr.create_issue_comment(message)

def validate_timezone(timezone: str) -> None:
    if timezone not in pytz.all_timezones:
        raise ValueError(f"Invalid timezone: {timezone}. Please provide a valid timezone.")

def validate_restricted_times(restricted_times: Dict[str, List[Tuple[float, float]]]) -> None:
    valid_days = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
    if not set(restricted_times.keys()).issubset(valid_days):
        raise ValueError("Invalid day keys in the restricted_times dictionary. Use 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'.")

    for day, intervals in restricted_times.items():
        if not isinstance(intervals, list):
            raise ValueError(f"Invalid value for '{day}' in restricted_times. It should be a list of tuples.")
        for interval in intervals:
            if not isinstance(interval, tuple) or len(interval) != 2 or not all(isinstance(n, (int, float)) for n in interval):
                raise ValueError(f"Invalid interval '{interval}' for '{day}' in restricted_times. It should be a tuple with two numbers.")

def validate_custom_message(custom_message: str) -> None:
    if not custom_message.strip():
        raise ValueError("Custom message cannot be an empty string.")

def check_restricted_time(timezone: str, restricted_times: Dict[str, List[Tuple[float, float]]]) -> bool:
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    weekday = now.strftime("%a").lower()
    hour = now.hour + (now.minute / 60)

    return any(start <= hour < end for start, end in restricted_times[weekday])

def main():
    # Get the inputs from the environment
    github_token = os.environ["GITHUB_TOKEN"]
    pr_title = os.environ["CI_PR_TITLE"]
    timezone = os.environ.get("TIMEZONE", "Australia/Sydney")
    restricted_times_json = os.environ.get("RESTRICTED_TIMES", None)
    custom_message = os.environ.get("CUSTOM_MESSAGE", "⚠️ **PR merging is not allowed outside business hours.** ⚠️")
    check_existing_comment = os.environ.get("CHECK_EXISTING_COMMENT", "true").lower() == "true"

    # Validate the inputs
    validate_timezone(timezone)
    if restricted_times_json:
        restricted_times = json.loads(restricted_times_json)
        validate_restricted_times(restricted_times)
    else:
        restricted_times = {
            "mon": [(0, 7), (16.5, 24)],
            "tue": [(0, 7), (16.5, 24)],
            "wed": [(0, 7), (16.5, 24)],
            "thu": [(0, 7), (16.5, 24)],
            "fri": [(0, 7), (16.5, 24)],
            "sat": [(0, 24)],
            "sun": [(0, 24)],
        }
    validate_custom_message(custom_message)

    if not check_restricted_time(timezone, restricted_times):
        print("✅ Merging is allowed at this time.")
        sys.exit(0)

    if "hotfix:" in pr_title.lower():
        print("✅ Hotfix PRs are allowed to merge outside business hours.")
        sys.exit(0)
    print("❌ Merging is not allowed during the specified time.")
    pr_number = int(os.environ["GITHUB_PR_NUMBER"])
    post_comment_on_pr(github_token, pr_number, custom_message, check_existing_comment)
    sys.exit(1)

if __name__ == "__main__":
    main()
