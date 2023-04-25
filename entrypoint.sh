#!/bin/sh -l

set -e

export GITHUB_TOKEN="$1"
export CI_PR_TITLE="$2"
export TIMEZONE="$3"
export RESTRICTED_TIMES="$4"
export CUSTOM_MESSAGE="$5"
export CHECK_EXISTING_COMMENT="$6"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "GITHUB_TOKEN environment variable is not set"
    exit 1
fi

python3 /src/main.py

echo "Done"
