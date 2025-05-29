# Directories
LOG_DIR := logs
MODEL_DIR := models
RASA_DIR := .rasa

# Files
ZSHRC := $(HOME)/.zshrc

# Default values
CONFIG ?= nlu_logreg_llm_openai
TESTS ?= demo_scripts
#TESTS ?= happy_paths
#TESTS ?= conversation_repair

# Variables
HOMEBREW_INSTALL_SCRIPT := https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
PYTHON_VERSION := 3.11.11
RASA_VERSION := 3.12.13
RASA_STUDIO_URL := <URL>
RASA_STUDIO_ASSISTANT_NAME := banking-assistant
RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS := 999
#RASA_PRO_LICENSE := <your-rasa-pro-license-key>
#OPENAI_API_KEY := sk-<your-openai-api-key>

# Commands
ECHO := @echo
SED_INPLACE := $(shell sed --version >/dev/null 2>&1 && echo "-i" || echo "-i ''")

.PHONY: help $(shell grep -E '^[a-zA-Z_-]+:' $(MAKEFILE_LIST) | sed 's/://')

#####
# Documentation

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-variables: ## Print all Makefile variables
	$(ECHO) "Makefile Variables:"
	$(ECHO) "LOG_DIR: $(LOG_DIR)"
	$(ECHO) "MODEL_DIR: $(MODEL_DIR)"
	$(ECHO) "RASA_DIR: $(RASA_DIR)"
	$(ECHO) "PYTHON_VERSION: $(PYTHON_VERSION)"
	$(ECHO) "RASA_VERSION: $(RASA_VERSION)"
	$(ECHO) "RASA_STUDIO_URL: $(RASA_STUDIO_URL)"
	$(ECHO) "RASA_STUDIO_ASSISTANT_NAME: $(RASA_STUDIO_ASSISTANT_NAME)"
	$(ECHO) "RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS: $(RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS)"
	$(ECHO) "RASA_PRO_LICENSE: $(RASA_PRO_LICENSE)"
	$(ECHO) "OPENAI_API_KEY: $(OPENAI_API_KEY)"
	
#####
# Rasa Pro related targets

install-homebrew: ## Install the Homebrew package manager
	$(ECHO) "Installing Homebrew..."
	/bin/bash -c "$$(curl -fsSL $(HOMEBREW_INSTALL_SCRIPT))"

install-pyenv: ## Install pyenv and pyenv-virtualenv
	$(ECHO) "Installing pyenv and pyenv-virtualenv..."
	brew install pyenv pyenv-virtualenv
	@{ \
		echo 'export PYENV_ROOT="$$(pyenv root)"'; \
		echo 'export PATH="$$PYENV_ROOT/bin:$$PATH"'; \
		echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$$(pyenv init -)"; fi'; \
		echo 'if command -v pyenv-virtualenv-init 1>/dev/null 2>&1; then eval "$$(pyenv virtualenv-init -)"; fi'; \
		echo 'export PYENV_VIRTUALENV_DISABLE_PROMPT=1'; \
	} >> $(ZSHRC)

install-uv: ## Install the uv tool using Homebrew
	$(ECHO) "Installing uv..."
	brew install uv

setup-pyenv-virtualenv: ## Setup a Python virtual environment using pyenv and virtualenv
	$(ECHO) "Setting up Pyenv virtual environment..."
	pyenv install $(PYTHON_VERSION)
	pyenv virtualenv $(PYTHON_VERSION) rasa$(RASA_VERSION)-py$(PYTHON_VERSION)
	$(ECHO) "Please run the following commands:"
	$(ECHO) "   source $(ZSHRC)"
	$(ECHO) "   pyenv activate rasa$(RASA_VERSION)-py$(PYTHON_VERSION)"

install-packages: ## Install Python packages from requirements.txt using uv
	$(ECHO) "Installing Python packages..."
	uv pip install -r requirements.txt

set-env: ## Set environment variables
	@echo "Setting environment variables in $(ZSHRC)"
	@sed $(SED_INPLACE) '/^export RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS=/d' $(ZSHRC)
	@sed $(SED_INPLACE) '/^export RASA_PRO_LICENSE=/d' $(ZSHRC)
	@sed $(SED_INPLACE) '/^export OPENAI_API_KEY=/d' $(ZSHRC)
	$(ECHO) 'export RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS="$(RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS)"' >> $(ZSHRC)
	$(ECHO) 'export RASA_PRO_LICENSE="$(RASA_PRO_LICENSE)"' >> $(ZSHRC)
	$(ECHO) 'export OPENAI_API_KEY="$(OPENAI_API_KEY)"' >> $(ZSHRC)
	$(ECHO) "Please run the following command:"
	$(ECHO) "   source $(ZSHRC)"

clean: ## Remove Rasa, model, and log files, and clean up Python cache files
	$(ECHO) "Cleaning files..."
	rm -rf $(RASA_DIR)/* $(MODEL_DIR)/* $(LOG_DIR)/*
	find . -name '*.py[co]' -o -name '*~' -exec rm -f {} +

model: ## Train and validate the Rasa model
	$(ECHO) "Training Rasa model..."
	rasa train -c configs/$(CONFIG).yml -d domain

action: ## Start the Rasa action server with debug mode and auto-reload
	$(ECHO) "Starting Rasa action server..."
	rasa run actions --debug --auto-reload

run: ## Start the Rasa server with logging enabled
	$(ECHO) "Starting Rasa Server with logging..."
	mkdir -p $(LOG_DIR)
	rasa run --debug --log-file $(LOG_DIR)/logs_$(shell date +%Y%m%d%H%M%S).out --enable-api --cors "*"

shell: ## Open the Rasa shell for interactive conversations
	$(ECHO) "Starting Rasa shell..."
	rasa shell --debug

inspect: ## Start Rasa Inspector with logging enabled
	$(ECHO) "Starting Rasa Inspector with logging..."
	mkdir -p $(LOG_DIR)
	rasa inspect --debug --log-file $(LOG_DIR)/logs_$(shell date +%Y%m%d%H%M%S).out

test: ## Run end-to-end tests on the Rasa model
	$(ECHO) "Testing Rasa model..."
	rasa test e2e -o e2e_tests/$(TESTS)

#####
# Rasa Studio related targets

install-ngrok: ## Install ngrok
	$(ECHO) "Installing ngrok..."
	brew install ngrok/ngrok/ngrok

start-ngrok: ## Start the ngrok service to tunnel requests to localhost
	$(ECHO) "Starting ngrok..."
	@if [ -n "$(SUBDOMAIN)" ]; then \
		$(ECHO) "Using custom subdomain: $(SUBDOMAIN)"; \
		ngrok http --domain=$(SUBDOMAIN).ngrok-free.app 5055; \
	else \
		$(ECHO) "Using default ngrok settings..."; \
		ngrok http 5055; \
	fi

config-studio: ## Configure Rasa Studio settings
	$(ECHO) "Setting up Rasa Studio config..."
	rasa studio config --advanced

login-studio: ## Log into Rasa Studio using provided credentials
	$(ECHO) "Logging into Rasa Studio..."
	rasa studio login

download-studio: ## Download domain and studio flow files from Rasa Studio
	$(ECHO) "Downloading from Rasa Studio..."
	@if [ -z "$(RASA_STUDIO_ASSISTANT_NAME)" ]; then \
		$(ECHO) "Error: RASA_STUDIO_ASSISTANT_NAME must be set"; \
		exit 1; \
	fi
	rasa studio download $(RASA_STUDIO_ASSISTANT_NAME) -d domain

upload-studio: ## Upload domain and other files to Rasa Studio
	$(ECHO) "Uploading to Rasa Studio..."
	@if [ -z "$(RASA_STUDIO_ASSISTANT_NAME)" ]; then \
		$(ECHO) "Error: RASA_STUDIO_ASSISTANT_NAME must be set"; \
		exit 1; \
	fi
	rasa studio upload -c configs/$(CONFIG).yml -d domain --calm
