#!/bin/sh -l

set -e

export GITHUB_TOKEN="$1"
export CI_PR_TITLE="$2"

# Check current time and block merge during specified times
python3 /check_merge_time.py

echo "Done"
