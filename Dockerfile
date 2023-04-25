FROM python:3.9-slim

LABEL version="1.0.0"
LABEL repository="https://github.com/koconder/no-out-of-hours-merge"
LABEL maintainer="Vincent Koc"

USER root

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update -yqq && \
    apt-get install -y --no-install-recommends && \
    apt-get clean && \
    rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/* \
    /usr/share/man \
    /usr/share/doc \
    /usr/share/doc-base

RUN useradd -u 8877 dummy
USER dummy

COPY entrypoint.sh /entrypoint.sh
COPY src/main.py /src/main.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
