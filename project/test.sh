#!/bin/bash

pytest -v --cov . --cov-report term-missing --cov-fail-under=100
