#!/bin/sh
# Запуск всех тестов проекта.
set -e
cd "$(dirname "$0")"
PYTHONPATH=src python3 -m unittest discover -s tests -t . -v
