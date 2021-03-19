#! /bin/bash

source /opt/python-venv/myfintnesspal/bin/activate
export FLASK_APP=/opt/myfitnesspal-api/flask_app.py

export PATH=$PATH:/opt/myfitnesspal-api/
flask run --host 0.0.0.0 --port=4080
