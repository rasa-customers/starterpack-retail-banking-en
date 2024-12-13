# Codespaces Documentation
This documentation outlines how the Codespaces setup works for this repository.

## Setup
The `.devcontainer.json` file in this directory defines how the Github Codespace starts up and is documented with comments. It's configured to use the Docker image defined in `Dockerfile` as a base for the Codespace. When a user creates a new Codespace, Github builds a container from the Dockerfile and lets a user access it via a web-based VS Code UI. The `Dockerfile` also has inline comments explaining what each line does.

## Hardware
By default, the Codespace that is created has 2 vCPUs, 8GB of RAM and 32GB of storage. This should be enough for most tasks, but it can be increased on a per-codespace basis as documented [here](https://docs.github.com/en/codespaces/customizing-your-codespace/changing-the-machine-type-for-your-codespace). Please note that each increment of hardware will double the cost for us to run the Codespace. For now, we only permit the creation of 2 vCPU/8GB RAM or 4 vCPU/16GB RAM Codespaces to keep costs under control.

## Rasa Pro Licensing
You can provide a licence for all Codespaces environments for a given repo to make things easier for users. To do this, add a Codespaces Secret called `RASA_PRO_LICENSE` with the value being the licence key, and it will be injected as an environment variable into every codespace created for that repo. To do this, go to your repo's **Settings** page and create a secret under **Secrets and variables > Codespaces > New Repository Secret**

![image](https://github.com/rasa-customers/rasa-pro-workshop-template/assets/88323896/a4fe1a66-b271-4d5b-926c-849fecd74886)
