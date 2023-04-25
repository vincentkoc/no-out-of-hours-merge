#!/bin/sh -l

set -e

export GITHUB_TOKEN="$1"
export CI_PR_TITLE="$2"
export TIMEZONE="$3"
export RESTRICTED_TIMES="$4"
export CUSTOM_MESSAGE="$5"
export CHECK_EXISTING_COMMENT="$6"


python3 /check_merge_time.py

echo "Done"
