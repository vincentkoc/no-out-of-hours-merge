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
  no_weekend_merge:
    name: Out of Hours Check ⏰
    runs-on: ubuntu-latest
    timeout-minutes: 2
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9


      - name: Block merge during specified times
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CI_PR_TITLE: ${{ github.event.pull_request.title }}
          GITHUB_PR_NUMBER: ${{ github.event.pull_request.number }}
          TIMEZONE: "Australia/Sydney"
          RESTRICTED_TIMES: '{"mon": [[0, 7], [16.5, 24]], "tue": [[0, 7], [16.5, 24]], "wed": [[0, 7], [16.5, 24]], "thu": [[0, 7], [16.5, 24]], "fri": [[0, 7], [16.5, 24]], "sat": [[0, 24]], "sun": [[0, 24]]}'
          CUSTOM_MESSAGE: "⚠️ **PR merging is not allowed outside business hours.** ⚠️"
        run: no-weekend-merge

```

## Configuration

You can configure the action using the following environment variables:

- `TIMEZONE`: The timezone used for checking the current time (default: `"Australia/Sydney"`).
- `RESTRICTED_TIMES`: A JSON string containing the restricted times for each day of the week (default: the provided example in the Usage section).
- `CUSTOM_MESSAGE`: The custom message that will be posted as a comment on the pull request if merging is not allowed (default: `"⚠️ PR merging is not allowed outside business hours. ⚠️"`).

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt).
