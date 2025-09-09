# Your Rasa version
RASA_VERSION := 3.13.9

#####
# Utility targets for help and variable inspection
ECHO := @echo

# List phony targets
.PHONY: print-variables clean model inspect run test help $(HELP_CMDS)

# Help (cross-platform)
HELP_CMDS := help model inspect run clean test print-variables
HELP_help    := Show available targets
HELP_model   := Train and validate the Rasa model
HELP_inspect := Inspect the Rasa model (debug/logging)
HELP_run     := Start Rasa server (API enabled)
HELP_clean   := Remove build artifacts
HELP_test    := Run end-to-end tests on the Rasa model
HELP_print-variables := Print all Makefile variables
# Print help text at parse time when `make help` is called
ifeq ($(filter help,$(MAKECMDGOALS)),help)
  $(info Available targets:)
  $(foreach t,$(HELP_CMDS),$(info   $(t) -  $(HELP_$(t))))
endif
help: ; @

print-variables: ## Print all Makefile variables
	$(ECHO) "Makefile Variables:"
	$(ECHO) "RASA_VERSION: $(RASA_VERSION)"
	$(ECHO) "RASA_PRO_LICENSE: $(RASA_PRO_LICENSE)"
	$(ECHO) "OPENAI_API_KEY: $(OPENAI_API_KEY)"

#####
# OS-specific settings

# Windows
ifeq ($(OS), Windows_NT)
  SHELL := powershell.exe
  .SHELLFLAGS := -NoProfile -Command
  MKDIR_LOG = powershell -NoProfile -Command "New-Item -ItemType Directory -Force logs | Out-Null"
  CLEAN_LOGS = powershell -NoProfile -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .rasa\*, models\*, logs\*; Get-ChildItem -Recurse -Include *.pyc,*.pyo -Force | Remove-Item -Force -ErrorAction SilentlyContinue; Get-ChildItem -Recurse -Filter '*~' -Force | Remove-Item -Force -ErrorAction SilentlyContinue"
  define RASA_DOCKER_MODEL
    docker run --rm -v "$${PWD}:/app" \
      -e RASA_PRO_LICENSE=$$env:RASA_PRO_LICENSE \
      -e OPENAI_API_KEY=$$env:OPENAI_API_KEY \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  define RASA_DOCKER
    docker run -v "$${PWD}:/app" -p 5005:5005 \
      -e RASA_PRO_LICENSE=$$env:RASA_PRO_LICENSE \
      -e OPENAI_API_KEY=$$env:OPENAI_API_KEY \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
# MacOS and Linux
else
  SHELL := /bin/bash
  .SHELLFLAGS := -eu -o pipefail -c
  MKDIR_LOG = mkdir -p logs
  CLEAN_LOGS = rm -rf .rasa/* models/* logs/* || true; find . -type f \( -name '*.py[co]' -o -name '*~' \) -delete
  define RASA_DOCKER_MODEL
    docker run --rm -v "$$PWD:/app" \
      -e RASA_PRO_LICENSE="$$RASA_PRO_LICENSE" \
      -e OPENAI_API_KEY="$$OPENAI_API_KEY" \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  define RASA_DOCKER
    docker run -v "$$PWD:/app" -p 5005:5005 \
      -e RASA_PRO_LICENSE="$$RASA_PRO_LICENSE" \
      -e OPENAI_API_KEY="$$OPENAI_API_KEY" \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
endif

#####
# Remove Rasa model, and log files, and clean up Python cache files
clean:
	$(ECHO) "Cleaning files..."
	$(CLEAN_LOGS)

# Train and validate the Rasa model
model:
	$(ECHO) "Training Rasa model..."
	$(call RASA_DOCKER_MODEL, train)

# Start Rasa Inspector with logging enabled
inspect:
	$(ECHO) "Starting Rasa Inspector with logging..."
	@$(MKDIR_LOG)
	$(call RASA_DOCKER, inspect --debug --log-file logs/logs.out)

# Start the Rasa server with logging enabled
run:
	$(ECHO) "Starting Rasa Server with logging..."
	@$(MKDIR_LOG)
	$(call RASA_DOCKER, run --debug --log-file logs/logs.out --enable-api --cors "*")

# Run end-to-end tests on the Rasa model
test:
	$(ECHO) "Testing Rasa model..."
	$(call RASA_DOCKER, test e2e tests/)