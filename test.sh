#!/bin/sh

coverage run --branch --source=termdoc -m unittest
coverage xml
coverage report -m
