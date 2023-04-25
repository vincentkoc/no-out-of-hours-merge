FROM python:3.9-slim

LABEL version="1.0.0"
LABEL repository="https://github.com/koconder/no-out-of-hours-merge"
LABEL maintainer="Vincent Koc"

RUN useradd -u 8877 dummy
USER dummy

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gh \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
COPY src/main.py /src/main.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
