#!/bin/bash

# Install uv if not present
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install project with dev dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install