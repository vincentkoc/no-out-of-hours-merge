import datetime
import json
import os
import re
import sys
from typing import Any, Dict

import holidays
import pytz
from dateutil import parser
from dateutil.rrule import FR, MO, SA, SU, TH, TU, WE
from github import Github


def post_comment_on_pr(
    github_token: str, pr_number: int, message: str, check_existing_comment: bool
) -> None:
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
        raise ValueError(
            f"Invalid timezone: {timezone}. Please provide a valid timezone."
        )


def is_holiday(now, holidays_config):
    if not holidays_config:
        return False

    country_holidays = holidays.CountryHoliday(
        holidays_config["country"],
        prov=holidays_config.get("state", None),
        state=holidays_config.get("state", None),
    )

    return now.date() in country_holidays


def validate_restricted_times(restricted_times: Dict[str, Any]) -> None:
    valid_days = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}

    if "weekly" not in restricted_times:
        raise ValueError("Missing 'weekly' key in restricted_times dictionary.")

    for rule in restricted_times["weekly"]:
        if not set(rule["days"]).issubset(valid_days):
            raise ValueError(
                "Invalid day keys in the restricted_times dictionary. Use "
                + "'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'."
            )

        if not isinstance(rule["intervals"], list):
            raise ValueError(
                f"Invalid value for '{rule['days']}' in restricted_times. "
                + " It should be a list of tuples."
            )
        for interval in rule["intervals"]:
            if (
                not isinstance(interval, tuple)
                or len(interval) != 2
                or not all(isinstance(n, (int, float)) for n in interval)
            ):
                raise ValueError(
                    f"Invalid interval '{interval}' for '{rule['days']}'"
                    + " in restricted_times."
                    + " It should be a tuple with two numbers."
                )


def validate_custom_message(custom_message: str) -> None:
    if not custom_message.strip():
        raise ValueError("Custom message cannot be an empty string.")


def is_restricted_time(timezone, restricted_times):
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    now = now.astimezone(tz)

    for rule in restricted_times["weekly"]:
        day_map = {
            "mon": MO,
            "tue": TU,
            "wed": WE,
            "thu": TH,
            "fri": FR,
            "sat": SA,
            "sun": SU,
        }
        mapped_days = [day_map[d] for d in rule["days"]]
        if now.weekday() in [d.weekday for d in mapped_days] and any(
            start <= now.hour + now.minute / 60 < end
            for start, end in rule["intervals"]
        ):
            return True

    for rule in restricted_times["dates"]:
        date = parser.parse(rule["date"]).date()
        if now.date() == date and any(
            start <= now.hour + now.minute / 60 < end
            for start, end in rule["intervals"]
        ):
            return True

    holiday_intervals = restricted_times.get("holidays", {}).get("intervals", [])
    if is_holiday(now, restricted_times.get("holidays")) and any(
        start <= now.hour + now.minute / 60 < end for start, end in holiday_intervals
    ):
        return True

    return False


def main():
    # Set Defaults
    restricted_times_default = {
        "weekly": [
            {"days": [MO, TU, WE, TH, FR], "intervals": [(0, 7), (16.5, 24)]},
            {"days": [SA, SU], "intervals": [(0, 24)]},
        ],
        "dates": [
            {"date": "2023-12-25", "intervals": [(0, 24)]},
            {"date": "2023-12-26", "intervals": [(0, 24)]},
        ],
        "holidays": {"country": "US", "state": "CA", "intervals": [(0, 24)]},
    }

    # Get the inputs from the environment
    github_token = os.environ["INPUT_GITHUB_TOKEN"]
    pr_title = os.environ["INPUT_PR_TITLE"]
    timezone = os.environ.get("INPUT_TIMEZONE", "Australia/Sydney")
    restricted_times_json = os.environ.get(
        "INPUT_RESTRICTED_TIMES", json.dumps(restricted_times_default)
    )
    custom_message = os.environ.get(
        "INPUT_CUSTOM_MESSAGE",
        "⚠️ **PR merging is not allowed outside business hours.** ⚠️",
    )
    check_existing_comment = (
        os.environ.get("INPUT_CHECK_EXISTING_COMMENT", "true").lower() == "true"
    )

    # Validate the inputs
    validate_timezone(timezone)
    try:
        restricted_times = json.loads(restricted_times_json)
        validate_restricted_times(restricted_times)
    except ValueError as e:
        raise ValueError(
            f"❌ Error parsing RESTRICTED_TIMES {restricted_times_json}"
        ) from e
    validate_custom_message(custom_message)

    if not is_restricted_time(timezone, restricted_times):
        print("✅ Merging is allowed at this time.")
        sys.exit(0)

    if re.search(r"(?i)hotfix\s*:", pr_title):
        print("✅ Hotfix PRs are allowed to merge outside business hours.")
        sys.exit(0)

    print("❌ Merging is not allowed during the specified time.")
    pr_number = int(os.environ["GITHUB_PR_NUMBER"])
    post_comment_on_pr(github_token, pr_number, custom_message, check_existing_comment)
    sys.exit(1)


if __name__ == "__main__":
    main()
