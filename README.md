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
- `config.yml`: Contains multiple configuration files for the assistant (i.e. different language models and settings).
- `credentials.yml`: Contains credentials for various services used by the Rasa assistant (i.e. Chat Widget)
- `data`: Contains flow definitions for the assistant and an in-memory database for the Rasa assistant.
- `docs`: Contains sample documents for Enterprise Search.
- `domain`: Contains domain files for the assistant.
- `tests`: Contains end-to-end test scenarios for the assistant where each subdirectory reflects a suite of tests (i.e. happy path).
    - `conversation_repair`: Contains end-to-end scripts that demonstrate the assistant's automatic conversation repair ability.
    - `demo_scripts`: Contains an end-to-end script that demonstrates all the assistant's features.
    - `happy_paths`: Contains a variety of banking transactions and inquiries.
- `endpoints.yml`: Contains endpoint configurations for the Rasa assistant.
- `prompts`: Contains Jinja2 template files for generating prompts.
- `requirements.txt`: Contains a list of Python packages required for the project.

<br><br><br>
# Installation (Docker)
> **Note:** You can find alternative installation methods in the [Rasa documentation](https://rasa.com/docs/pro/installation/overview).
<br>

## Installation Steps
- Before You Begin
- Setting Environment Variables for Rasa
- Install Docker
- Download Rasa Retail Banking Starter Pack
- Starting the Demo Assistant
<br>

## Before You Begin
**To use this starter pack, you will need:**
1. A free [Rasa Developer Edition license](https://github.com/rasa-customers/starterpack-retail-banking-en/releases). To get the free license use the link and complete the form. You'll be emailed the license key. Store this somewhere safe as you'll need it a bit later in the instructions below. The actual installation of the Rasa Pro platform will be performed during the installation steps described below.
2. An API key from OpenAI (the default model provider for this starter pack, though CALM supports other LLMs, too).
    - If you haven't already, sign up for an account on the OpenAI platform.
    - Then, navigate to the [OpenAI Key Management](https://platform.openai.com/api-keys) (Dashboard > API keys) page and click on the "Create New Secret Key" button to initiate obtaining `<your-openai-api-key>`.
3. A computer. Instructions are available for MacOS, Linux & Windows.
> **Note for Windows users:**
> If you don’t already have `make`, you’ll need to install it:
>
> - **Option 1:** Install [Chocolatey](https://chocolatey.org/install).
>   👉 Open **PowerShell as Administrator** (Start → search "PowerShell" → right-click → *Run as Administrator*).
>   Then run:
>   ```powershell
>   choco install make -y
>   ```
>   Verify with:
>   ```powershell
>   make --version
>   ```
>
> - **Option 2:** Install [Git for Windows](https://git-scm.com/download/win), which includes Git Bash (and `make`).
>   Open **Git Bash** instead of PowerShell to run your commands.
<br>

## Setting Environment Variables for Rasa

You'll need to save your **Rasa Pro license key** and **OpenAI API key** as environment variables so they can be used by the application.

**MacOS, Linux**
1. Open your terminal, and edit your shell config
    - `nano ~/.zshrc` (or `~/.bashrc` if you’re using Linux bash)
2. At the bottom of the file, add lines like this (replace the values with your actual keys):
    - `export RASA_PRO_LICENSE=<your-rasa-pro-license-key>`
    - `export OPENAI_API_KEY=sk-<your-openai-api-key>`
    1. For example, it may look something like this:
        - `RASA_PRO_LICENSE=etou948949theu`
        - `OPENAI_API_KEY=sk-proj-ntehoitnhtnoe`
3. Save the file (`CTRL+O`, `Enter`, `CTRL+X` in nano), then reload it
    - `source ~/.zshrc`  (or `~/.bashrc` if you’re using Linux bash)
4. Check that the variables are set:
    - `echo $RASA_PRO_LICENSE`
    - `echo $OPENAI_API_KEY`

**Windows**
1. Press `Win + S` and type `Environment Variables`, then select `Edit the system environment variables`.
2. In the `System Properties` window, click `Environment Variables`.
3. Under `User variables` (applies only to your user), click `New`.
    1. For `Name`, enter: `RASA_PRO_LICENSE`
    2. For `Value`, enter: `<your-rasa-pro-license-key>`
4. Repeat for `OPENAI_API_KEY`.
5. Click `OK` → `OK` to save and close all windows.
6. Restart your terminal (PowerShell) so the new values load.
7. Verify the variables are set (PowerShell):
    1. `echo $env:RASA_PRO_LICENSE`
    2. `echo $env:OPENAI_API_KEY`
<br>

## Install Docker
1. Download & install docker:
    - MacOS:   https://docs.docker.com/desktop/setup/install/mac-install/
    - Linux:   https://docs.docker.com/engine/install/
    - Windows: https://docs.docker.com/desktop/setup/install/windows-install/
        - Use WSL 2 backend (not Hyper-V)
3. Start Docker Desktop. Make sure Docker Desktop (the Docker daemon) is running before you run any commands.
    - Windows: Follow prompted instructions for WSL (e.g. `wsl --update`)
4. Verify Installation. Open your terminal (Mac/Linux shell, or PowerShell on Windows) and run:
    1. `docker --version`
5. Download the Rasa Pro Docker image. Open your terminal and run:
    1. `docker pull rasa/rasa-pro:3.13.7`
<br>

## Download Rasa Retail Banking Starter Pack
1. Download the Source Code Assets for the [latest release from GitHub](https://github.com/rasa-customers/starterpack-retail-banking-en/releases)
2. Uncompress the assets in a local directory of your choice.
    1. The **starterpack-retail-banking-en** directory (created when uncompressed) contains a README file with additional instructions on installing dependencies, training the model, and running the assistant locally.
3. Open your terminal (or PowerShell on Windows) and navigate to the directory where you uncompressed the **starterpack-retail-banking-en** files.
Congratulations, you have successfully installed Rasa and are ready to use the Retail Banking Starter Pack as a demo or as a foundation for your custom flows.
<br>

## Starting the Demo Assistant
To start up the Retail Banking Demo Assistant, ensure you're in the **starterpack-retail-banking-en** directory.
1. **Train the Rasa model**
2. **Start the Rasa Inspector** or
3. **Start the Rasa Chat Widget**
<br>

## 1. Train the Rasa model
```bash
make model
```

You will find your trained model inside the `models/` directory.
You can now test your assistant using the Rasa Inspector or Rasa Chat Widget.
<br><br>

## 2. Start the Rasa Inspector
```bash
make inspect
```
1. Once you see the “Starting worker” message in your terminal, proceed to the next step.
2. In your browser go to: http://localhost:5005/webhooks/socketio/inspect.html
<br><br>

## 3. Start the Rasa Chat Widget
```bash
make run
```
1. Once you see the “Starting worker” message in your terminal, proceed to the next step.
2. Open Finder (Mac) or File Explorer (Windows).
3. Navigate to the chatwidget directory inside the **starterpack-retail-banking-en** folder you uncompressed earlier.
4. Double-click `chatwidget/index.html` to open the demo in your browser.
5. You can now interact with the Retail Banking Demo Assistant using Rasa’s chat widget.
<br><br>
> [!TIP]
> You can also edit chatwidget/index.html to customize the look and behavior of the demo.

> [!NOTE]
> For a full list of Rasa CLI commands refer to: https://rasa.com/docs/reference/api/command-line-interface/#cheat-sheet
<br>

## Stopping the Demo Assistant
1. To stop the Rasa server, return to the terminal window where it is running and press **Ctrl+C**.
2. That's it, you’ve successfully run your first Rasa Assistant! You can now close the terminal window if you wish.
<br>

## Restarting the Demo Assistant
1. Open your terminal and navigate to the **starterpack-retail-banking-en** directory.
2. Then, follow the same steps from **Starting the Demo Assistant** to run the assistant again.
<br>

# Contributing
Feel free to fork this repo and submit pull requests. Suggestions and improvements are always welcome!
<br><br>

# License
This project is licensed under the Apache 2.0 License, allowing modification, distribution, and usage with proper attribution.
