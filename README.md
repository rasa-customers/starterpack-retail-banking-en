# Rasa Starter Pack: Retail Banking in English

Rasa has created a new starter pack for building AI assistants in retail banking with the Rasa CALM framework.

Our Retail Banking Intelligent Assistant can transfer money, check balances, manage payees, and block cards. Check out the code here on GitHub.

You can use this demo assistant as a starting point for your own Retail Banking Intelligent Assistant, or get ideas for features you might want to implement. It's free for you to copy and use locally with the Rasa Pro Developer Edition.

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

Navigate to the ​​starterpack-retail-banking-en directory where the zip file was uncompressed, and run the following commands in your terminal to set up your environment:

1. **Install Homebrew**:
    - Run `make install-homebrew`.
    - Note: You may need to run the following commands if prompted:
        - `echo >> $HOME/.zprofile`
        - `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> $HOME/.zprofile`
        - `eval "$(/opt/homebrew/bin/brew shellenv)"`
2. **Install Pyenv**:
    - Run `make install-pyenv`.
3. **Install uv**:
    - Run `make install-uv`.
4. **Setup Pyenv virtualenv**:
    - Run `make setup-pyenv-virtualenv`.
    - Run `source ~/.zshrc`
    - Run `pyenv activate <your-pyenv-virtualenv>`: e.g. pyenv activate rasa3.11.3-py3.11.11
5. **Install Python packages**:
    - Run `make install-packages`.
    - Run `source deactivate`
6. **Update Makefile File**:
    - Once the installation is complete, update the placeholders in the Makefile file with your actual values (Note: remove the # and <, > characters too), and save the file.
    - ```bash
      #RASA_PRO_LICENSE=<your-rasa-pro-license-key>
      #OPENAI_API_KEY=sk-<your-openai-api-key>
      ```
   - For example, after updating, it would look similar to this:
   - ```bash
     RASA_PRO_LICENSE=etou948949theu
     OPENAI_API_KEY=sk-proj-ntehoitnhtnoe
     ```
7. **Set environment variables**:
    - Run `make set-env`
    - Run `source ~/.zshrc`

> [!NOTE]
> Use `make help` for a description of all commands available.

> [!NOTE]
> Use `make set-env` to load these environment variables into your current terminal session.  
> For VScode to recognize the new environment variables, you may need to switch to a different VScode Python:Select Interpreter and then back to the one you just created- in a new terminal. In some cases you may need to restart VScode completely.

## Usage

Ensure you've activated your pyenv virtualenv:  
`pyenv activate <your-pyenv-virtualenv>`: e.g. pyenv activate rasa3.11.3-py3.11.11

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
