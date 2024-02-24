# Specify the required Python version.
ARG PYTHON_IMAGE=python:3.12-alpine
FROM ${PYTHON_IMAGE}
# Required dependencies for compiling project's packages
RUN apk --no-cache add gcc libffi-dev musl-dev yaml-dev
# Create the working directory.
WORKDIR /usr/Shinshi/Alterstein/
# Project files copy
COPY .. .
# Install the project's dependencies.
RUN pip install --no-cache-dir --quiet -U poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --quiet --no-interaction --no-root --no-dev
# Start
STOPSIGNAL SIGINT
ENV SHINSHI_PYTHON_EXECUTABLE=python3.12
ENTRYPOINT ["/bin/sh", "-c", "poetry run ${SHINSHI_PYTHON_EXECUTABLE} -OOm shinshi_main"]
