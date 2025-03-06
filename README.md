# multimodal_legal_rag
Capstone project for comp.cs.530 (Fine-tuning LLMs)


## Depencies

Install docker and docker compose plugin, tutorial and commands:

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

After installation, You need to add permissions with
```bash
sudo usermod -aG docker $USER
newgrp docker
```


## Usage

Run using commands

```bash
docker compose build
docker compose up
```

*NOTE: if on MacOs, run `open -a Docker` to ensure that docker is running.*

## Project Architecture
[Architecture diagram](docs/project_architecture.png)
