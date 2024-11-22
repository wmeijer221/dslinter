#!/bin/bash

pip install --upgrade pip
pip install poetry

poetry lock --no-update
poetry install

poetry build
pip install ./dist/dslinter-2.0.9.tar.gz

poetry run pytest .
