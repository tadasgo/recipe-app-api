FROM python:3.9-alpine3.13
LABEL maintainer="https://github.com/tadasgo"

# stdout and stderr sent directly to terminal
ENV PYTHONUNBUFFERED 1

# copy from source to container image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# updated by docker-compose
ARG DEV=false

# creates a new image layer for each command
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# python commands can be run from the virtualenv
ENV PATH="/py/bin:$PATH"

# container will run with the last user swithed into
# no root user privileges 🔒
USER django-user