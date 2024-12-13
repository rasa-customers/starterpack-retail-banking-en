# Rasa Starter Pack: Financial Services in English

Rasa has created a new starter pack for building AI assistants in financial services or banking with the Rasa CALM framework. 
Our Banking Intelligent Assistant can transfer money, check balances, manage payees, and block cards. Check out the code her on GitHub.

You can use this demo assistant as a starting point for your own Banking Intelligent Assistant, or get ideas for features you might want to implement. It's free for you to copy and use locally with the Rasa Pro Developer Edition. 

The Rasa Pro Developer Edition is free and allows you to run Rasa Pro (with CALM) locally on your laptop, your desktop or your integrated development environment. The detailed information for the Developer Edition can be found here: https://rasa.com/docs/rasa-pro/developer-edition/.



## Project Structure

Here's a brief description of the directories and files in the project root:

- `Makefile`: Contains a set of directives used by the `make` build automation tool to streamline running repetitive commands.
- `README.md`: The file you're currently reading!
- `actions`: Contains Python scripts defining custom actions for the Rasa assistant.
- `configs`: Contains multiple configuration files for the assistant (i.e. different language models and settings).
- `credentials.yml`: Contains credentials for various services used by the Rasa assistant.
- `data`: Contains flow definitions for the assistant and an in-memory database for the Rasa assistant.
- `docs`: Contains sample documents for Enterprise Search.
- `domain`: Contains domain files for the assistant.
- `e2e_tests`: Contains end-to-end test scenarios for the assistant where each subdirectory reflects a suite of tests (i.e. happy path).
    - `demo_scripts`: Contains an end-to end-script that demonstrates all the assistant's features.
- `endpoints.yml`: Contains endpoint configurations for the Rasa assistant.
- `prompts`: Contains Jinja2 template files for generating prompts.
- `pyproject.toml`: Contains metadata and dependencies for the Python project.
- `requirements.txt`: Contains a list of Python packages required for the project.

## Prerequisites

You'll need to create an ngrok account and connect your ngrok agent to this account by following [this](https://ngrok.com/docs/getting-started/#step-2-connect-your-account) step. This will enable you to connect Studio to your local action server for custom action development and testing.

## Setup

1. **Install Homebrew**: Run `make install-homebrew`.
2. **Install Pyenv**: Run `make install-pyenv`.
3. **Install uv**: Run `make install-uv`.
4. **Install ngrok**: Run `make install-ngrok`.
5. **Setup Pyenv virtualenv**: Run `make setup-pyenv-virtualenv`.
6. **Install Python packages**: Run `make install-packages`.
7. **Set environment variables**: Run `make set-env`.

> [!NOTE]
> Use `make help` for a description of all commands available.

## Update .env File

Update the placeholders in the `.env` file with your actual values:

```bash
# Rasa Pro
RASA_PRO_LICENSE=<your-rasa-pro-license-key>
RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS=999

# OpenAI
OPENAI_API_KEY=sk-<your-openai-api-key>
OPENAI_ORGANISATION_ID=org-<your-openai-organisation-id>
```
> [!NOTE]
> Use `make set-env` to load these environment variables into your current terminal session.

## Usage

### Rasa Pro Workflow

1. **Clean Rasa files**: Run `make clean`.
2. **Train / validate Rasa model**: Run `make model CONFIG=<your-config-file>`. Replace `<your-config-file>` with the name of your configuration file in the `configs` directory.
3. **Start Rasa action server**: Run `make action`.
4. **Start Rasa Inspector**: Run `make inspect` (or a Rasa Server or Rasa Shell using `make run` and `make shell` respectively)
5. **Test Rasa model**: Run `make test TESTS=<your-test-subdirectory>`. Replace `<your-test-subdirectory>` with the name of your subdirectory under the `e2e_tests` directory.

### Rasa Studio Workflow

This workflow assumes you have bootstraped a set of flows using the Studio visual flow builder and would like to continue custom action development using Rasa Pro locally.

1. **Run ngrok server**: Run `make start-ngrok`.
2. **Update Action Server URL**: Add a static forwarding address + `/webhook` (i.e. https://word1-word2-word3.ngrok-free.app/webhook) under **Assistant settings** > **Configuration** > **endpoints.yml** > **action_endpoint:** in Studio.
2. **Setup Rasa Studio config**: Run `make config-studio`.
3. **Log into Rasa Studio**: Run `make login-studio`.
4. **Download `domain.yml` and `studio_flows.yml` from Rasa Studio**: Run `make download-studio`.
