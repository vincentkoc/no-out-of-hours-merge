FROM python:3.9-slim

LABEL version="1.0.0"
LABEL repository="https://github.com/koconder/no-out-of-hours-merge"
LABEL maintainer="Vincent Koc"
ENV DOCKER_BUILDKIT=1

USER root

# RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
RUN apt-get update -yqq && \
    apt-get install -y --no-install-recommends && \
    apt-get clean && \
    rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/* \
    /usr/share/man \
    /usr/share/doc \
    /usr/share/doc-base

COPY entrypoint.sh /entrypoint.sh
COPY src/main.py /src/main.py
COPY requirements*.txt /

RUN useradd -u 8877 dummy
RUN chmod +x /entrypoint.sh
RUN chown -R dummy:dummy /entrypoint.sh && \
    chown -R dummy:dummy /src/

USER dummy

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
