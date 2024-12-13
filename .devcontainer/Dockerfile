# Use a Microsoft Python base image that includes Python dev tools and the dependencies required for Codespaces
FROM mcr.microsoft.com/devcontainers/python:1-3.10-bookworm

# Install UV as it's significantly faster than pip to install Rasa Pro
RUN pip install uv

# Use UV to install Rasa Pro into the system Python install (ie not a virtual environment)
# Change the version number at the end to update what version of Rasa Pro gets installed
RUN uv pip install --system --extra-index-url https://europe-west3-python.pkg.dev/rasa-releases/rasa-pro-python/simple rasa-pro==3.10.5
