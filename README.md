# Rasa Starter Pack: Financial Services in English

Rasa has created a new starter pack for building AI assistants in financial services or banking with the Rasa CALM framework.
Our Banking Intelligent Assistant can transfer money, check balances, manage payees, and block cards. Check out the code here on GitHub.

You can use this demo assistant as a starting point for your own Banking Intelligent Assistant, or get ideas for features you might want to implement. It's free for you to copy and use locally with the Rasa Pro Developer Edition.

The Rasa Pro Developer Edition is free and allows you to run Rasa Pro (with CALM) locally on your laptop, your desktop or your integrated development environment. The detailed information for the Developer Edition can be found here: https://rasa.com/docs/rasa-pro/developer-edition/.



## Project Structure

Here's a brief description of the directories and files in the project root:

- `Makefile`: Contains a set of directives used by the `make` build automation tool to streamline running repetitive commands.
- `README.md`: The file you're currently reading!
- `actions`: Contains Python scripts defining custom actions for the Rasa assistant.
- `configs`: Contains multiple configuration files for the assistant (i.e. different language models and settings).
- `credentials.yml`: Contains credentials for various services used by the Rasa assistant (i.e. Chat Widget)
- `data`: Contains flow definitions for the assistant and an in-memory database for the Rasa assistant.
- `docs`: Contains sample documents for Enterprise Search.
- `domain`: Contains domain files for the assistant.
- `e2e_tests`: Contains end-to-end test scenarios for the assistant where each subdirectory reflects a suite of tests (i.e. happy path).
    - `conversation_repair`: Contains end-to-end scripts that demonstrate the assistant's automatic conversation repair ability.
    - `demo_scripts`: Contains an end-to-end script that demonstrates all the assistant's features.
    - `happy_paths`: Contains a variety of banking transactions and inquiries.
- `endpoints.yml`: Contains endpoint configurations for the Rasa assistant.
- `prompts`: Contains Jinja2 template files for generating prompts.
- `requirements.txt`: Contains a list of Python packages required for the project.

## Setup

1. **Install Homebrew**: Run `make install-homebrew`.
2. **Install Pyenv**: Run `make install-pyenv`.
3. **Install uv**: Run `make install-uv`.
4. **Setup Pyenv virtualenv**: Run `make setup-pyenv-virtualenv`.
5. **Install Python packages**: Run `make install-packages`.
6. **Set environment variables**: Run `make set-env`.

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

### Rasa Inspector

The Rasa Inspector is a debugging tool that offers developers an in-depth look into the conversational mechanics of their Rasa assistant. It allows for real-time prototyping of conversation flows, slot values, and tracker states to ensure smooth and accurate dialogue management.

1. **Clean Rasa files**: Run `make clean`
2. **Train / validate Rasa model**: Run `make model`
3. **Start Rasa Inspector**: Run `make inspect`. This will trigger a new browser tab open request.

### Rasa Chat Widget

The Rasa Chat widget is pop-up box that appears on the lower right corner of a website, inviting users to chat.

1. **Clean Rasa files**: Run `make clean`
2. **Train / validate Rasa model**: Run `make model`
3. **Start Rasa Chat Widget (backend)**: Run `make run`
4. **Start Rasa Chat Widget (frontend)**: MacOS
    - Run `open -a "Google Chrome" chatwidget/index.html` or
    - Locate the chatwidget/index.html file in your Finder and open it with your browser of choice
