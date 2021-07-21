#!/bin/sh

python3 -m doctest README.md

coverage run --branch --source=termdoc -m unittest
coverage xml
coverage report -m
