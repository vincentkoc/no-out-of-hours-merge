# ⏰ No Out of Hours Merge (Github Action)

A GitHub Action that prevents merging pull requests outside of specified business hours or on weekends. This action can be configured with custom time zones, restricted times, and custom messages.

## Features

- Customizable time zone and restricted hours
- Optional custom message for pull request comments
- Allows hotfixes to bypass the time restrictions
- Provides informative error messages and input validation
- Allows for rules on specific days
- Support for holidays (thanks to holidays pip package)

## Requirements

- Python 3.9 or higher
- [PyGithub](https://pypi.org/project/PyGithub/)
- [pytz](https://pypi.org/project/pytz/)
- [holidays](https://pypi.org/project/holidays/)

## Usage

To use the No Out of Hours Merge GitHub Action, add the following workflow to your GitHub repository:

```yaml
name: No Out of Hours Merge

on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened

jobs:
  no_out_of_hours_merge:
    name: Out of Hours Check ⏰
    runs-on: ubuntu-latest
    timeout-minutes: 2
    permissions:
      contents: read
      issues: write
      pull-requests: write
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Block merge during specified times
        uses: vincentkoc/no-out-of-hours-merge@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_TITLE: ${{ github.event.pull_request.title }}
          TIMEZONE: "Australia/Sydney"
          RESTRICTED_TIMES: >
            {
              "weekly": [
                {
                  "days": ["mon", "tue", "wed", "thu", "fri"],
                  "intervals": [[0, 7], [16.5, 24]]
                }
              ],
              "dates": [
                {
                  "date": "2023-12-25",
                  "intervals": [[0, 24]]
                }
              ],
              "holidays": {
                "country": "GB",
                "state": "UK",
                "intervals": [[0, 24]]
              }
            }
          CUSTOM_MESSAGE: "⚠️ **PR merging is not allowed outside business hours. Let's not be a cowboy!** ⚠️"

```

## Configuration

You can configure the action using the following inputs:

- `GITHUB_TOKEN`: Required to post a message back to the PR.
- `PR_TITLE`: Pull request title used to allow `hotfix:` bypasses.
- `CUSTOM_MESSAGE`: The custom message that will be posted as a comment on the pull request if merging is not allowed (default: `"⚠️ PR merging is not allowed outside business hours. ⚠️"`).
- `CHECK_EXISTING_COMMENT`: Don't post the same message twice (default: enabled).
- `TIMEZONE`: The timezone used for checking the current time (default: `"Europe/London"`).
- `RESTRICTED_TIMES`: A JSON string containing the restricted times for each day of the week (default: the provided example in the Usage section).

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt).
