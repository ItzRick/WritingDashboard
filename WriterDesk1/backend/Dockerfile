# For more information, please refer to https://aka.ms/vscode-docker-python
FROM openjdk:11-slim-bullseye
COPY --from=python:3.10-slim-bullseye / /

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

#install additional requirements
RUN apt-get update
RUN apt-get install -y --no-install-recommends libreoffice 
RUN apt-get install -y --no-install-recommends libmagic1 
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD gunicorn -b 0.0.0.0:5000 wsgi:app
# CMD flask run --host=0.0.0.0
