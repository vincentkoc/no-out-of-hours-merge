#!/bin/sh -l

set -e

export GITHUB_TOKEN="$INPUT_GITHUB_TOKEN"
export CI_PR_TITLE="$INPUT_CI_PR_TITLE"
export TIMEZONE="$INPUT_TIMEZONE"
export RESTRICTED_TIMES="$INPUT_RESTRICTED_TIMES"
export CUSTOM_MESSAGE="$INPUT_CUSTOM_MESSAGE"
export CHECK_EXISTING_COMMENT="$INPUT_CHECK_EXISTING_COMMENT"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "GITHUB_TOKEN environment variable is not set"
    exit 1
fi

python3 /src/main.py

echo "Done"
