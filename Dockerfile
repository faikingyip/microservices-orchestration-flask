from python:3.12.4-alpine3.20
LABEL maintainer="Fai"

# Logs will be outputted to the screen immediately
# when our application is running.
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

ARG DEFAULT_PORT=5000
ENV PORT $DEFAULT_PORT
EXPOSE $PORT

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp 

# These files may change frequently but we don't want
# the previous steps to rebuild, so we recopy these
# files at the end of the dockerfile.
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./stores.json /app/stores.json
COPY ./test_store_postcodes.json /app/test_store_postcodes.json

ENV PATH="/py/bin:$PATH"
