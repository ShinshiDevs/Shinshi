# Specify the required Python version.
ARG PYTHON_IMAGE=python:3.12-alpine
FROM ${PYTHON_IMAGE}
ENV SHINSHI_PYTHON_EXECUTABLE=python3.12
# Required dependencies for compiling project's packages
RUN apk add --no-cache --virtual .build libffi-dev musl-dev yaml-dev && \
    pip install --upgrade pip && \
    pip install setuptools poetry && \
    apk del .build
# Create the working directory.
WORKDIR /usr/Shinshi/Alterstein/
# Project files copy
COPY .. .
# Install the project's dependencies.
RUN poetry config virtualenvs.in-project true && \
    poetry install --quiet --no-interaction --no-root --no-dev
# Start
STOPSIGNAL SIGINT
ENTRYPOINT ["/bin/sh", "-c", "poetry run ${SHINSHI_PYTHON_EXECUTABLE} -OOm shinshi"]
