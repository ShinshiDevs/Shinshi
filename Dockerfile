# Python.
ARG PYTHON_IMAGE=python:3.12-alpine
FROM ${PYTHON_IMAGE}

ARG PYTHON_EXECUTABLE=python3.12
ARG WORKING_DIRECTORY=/usr/shinshi
ARG VENV_DIRECTORY=${WORKING_DIRECTORY}/.venv

# Create the working directory.
RUN mkdir -p ${WORKING_DIRECTORY}
WORKDIR ${WORKING_DIRECTORY}

# Make and activate a virtual environment for the dependencies.
RUN mkdir ${VENV_DIRECTORY}
RUN ${PYTHON_EXECUTABLE} -m venv ${VENV_DIRECTORY}
RUN . ${VENV_DIRECTORY}/bin/activate

# Install the bot's dependencies.
RUN apk add --no-cache --virtual gcc libffi-dev musl-dev yaml-dev
COPY requirements.txt ${WORKING_DIRECTORY}
RUN ${PYTHON_EXECUTABLE} -m pip install -r requirements.txt

# Copy the source code.
COPY . .

# Yuri Gagarin: "Let’s go!"
ENV SHINSHI_PYTHON_EXECUTABLE ${PYTHON_EXECUTABLE}
STOPSIGNAL SIGINT
ENTRYPOINT ["/bin/sh", "-c", "poetry run ${SHINSHI_PYTHON_EXECUTABLE} -OOm shinshi"]
