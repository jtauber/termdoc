#!/bin/sh

coverage run --branch --source=termdoc -m unittest
coverage report
