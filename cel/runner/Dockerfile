FROM python:3-alpine

# Correct directories
RUN mkdir /runner /app /venv && touch /app/__init__.py

# # Install dependencies
RUN python3 -m venv /venv
# ADD requirements /app/requirements
# RUN /venv/bin/pip install -r /app/requirements/base.txt

# Copy across the runner code
COPY bootstrap.py /runner

# This is the command we want to run by default when a container is created
CMD /venv/bin/python /runner/bootstrap.py
