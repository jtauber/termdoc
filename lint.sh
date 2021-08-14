#!/bin/sh

isort .
black .
flake8 --max-line-length=88 --ignore=E203 .
