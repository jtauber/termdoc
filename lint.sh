#!/bin/sh

isort *.py
black *.py
flake8 --max-line-length=88 *.py
