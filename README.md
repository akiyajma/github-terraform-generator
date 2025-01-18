# Terraform Generator for GitHub

This project provides a tool to generate Terraform files for provisioning GitHub resources. It uses Jinja2 templates to create Terraform configuration files based on the provided input data.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Documentation](#documentation)

## Features

- Generate Terraform files for various resources.
- Calculate differences between existing and requested resources.
- Process additions, updates, and deletions of resources.
- Configurable through a YAML configuration file.
- Logging support for better traceability.

## Requirements

- Python 3.12 or higher
- pip

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/terraform-generator.git
    cd terraform-generator
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. (Optional) Install development dependencies:

    ```sh
    pip install -r dev-requirements.txt
    ```

## Usage

1. Set up the configuration file [`config/config.yaml`](config/config.yaml ):

    ```yaml
    template_dir: "templates"
    output_dir: "terraform"
    tfstate_file: "terraform.tfstate"
    state_file: "existing_resources.json"
    default_repository:
      visibility: "public"
    default_team:
      privacy: "closed"
      role: "member"
    ```

2. Set environment variables for resources:

    ```sh
    export REPOSITORIES='[
      {
        "repository_name": "repo1",
        "description": "This is repo1",
        "visibility": "public",
        "gitignore_template": "Python"
      }
    ]'
    export TEAMS='[
      {
        "team_name": "team1",
        "description": "This is team1",
        "privacy": "closed",
        "members": [
          {"username": "user1", "role": "maintainer"}
        ]
      }
    ]'
    ```

3. Run the main script:

    ```sh
    python main.py
    ```

4. The generated Terraform files will be saved in the [`output_dir`](generator/repository_generator.py ) specified in the configuration file.

## Configuration

The configuration file [`config/config.yaml`](config/config.yaml ) contains the following settings:

- [`template_dir`](generator/repository_generator.py ): Directory containing the Jinja2 templates.
- [`output_dir`](generator/repository_generator.py ): Directory where the generated Terraform files will be saved.
- [`tfstate_file`](main.py ): Path to the Terraform state file.
- [`state_file`](main.py ): Path to the file where the existing state will be saved.
- `default_repository`: Default settings for repositories.
- `default_team`: Default settings for teams.

## Logging

Logging is configured using the [`logging_config.py`](logging_config.py ) file. The log messages are output to the console with different levels (INFO, WARNING, ERROR).

## Testing

To run the tests, use the following command:

```sh
pytest tests/
```
The tests cover various aspects of the project, including model validation, resource generation, and difference calculation.

## Project Structure
```
terraform-generator/
├── config/
│   ├── __init__.py
│   ├── config_loader.py
│   └── config.yaml
├── docs/
│   ├── generator/
│   │   ├── index.md
│   │   ├── repository_generator.md
│   │   └── team_generator.md
│   ├── main.md
│   └── utils/
│       ├── diff_calculator.md
│       ├── index.md
│       ├── process_resources.md
│       ├── resource_changes.md
│       └── tfstate_loader.md
├── generator/
│   ├── __init__.py
│   ├── repository_generator.py
│   ├── team_generator.py
│   └── terraform_generator.py
├── models/
│   ├── __init__.py
│   ├── repository.py
│   └── team.py
├── templates/
│   ├── repository.tf.j2
│   └── team.tf.j2
├── tests/
│   ├── __init__.py
│   ├── test_config_loader.py
│   ├── test_diff_calculator.py
│   ├── test_generator.py
│   ├── test_main.py
│   ├── test_models.py
│   └── test_tfstate_loader.py
├── utils/
│   ├── __init__.py
│   ├── diff_calculator.py
│   ├── process_resources.py
│   ├── resource_changes.py
│   └── tfstate_loader.py
├── .devcontainer/
│   └── devcontainer.json
├── .gitignore
├── dev-requirements.in
├── dev-requirements.txt
├── logging_config.py
├── main.py
├── pyproject.toml
├── README.md
├── requirements.in
└── requirements.txt
```

## Documentation
Documentation is generated and available in the docs/ directory. It includes detailed information about the modules and functions in the project.

To generate the documentation in Markdown format, run the following command:
```python
python -m pdoc --output-dir docs --force config generator models tests utils main logging_config
```
