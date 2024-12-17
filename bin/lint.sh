#!/usr/bin/env bash

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ "$1" == "--fix" ]; then
  ruff check . --fix && black ./flood_aid && toml-sort pyproject.toml --all --in-place
else
  ruff check . && black ./flood_aid --check && toml-sort pyproject.toml --all --in-place --check
fi
