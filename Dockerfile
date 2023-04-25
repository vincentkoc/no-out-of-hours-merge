FROM python:3.9-slim

USER dummy

LABEL version="1.0.0"
LABEL repository="https://github.com/koconder/no-out-of-hours-merge"
LABEL maintainer="Vincent Koc"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gh \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
COPY check_merge_time.py /check_merge_time.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]