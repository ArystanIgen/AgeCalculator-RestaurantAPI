#!/bin/bash

alembic -x data=true upgrade head
uvicorn app.main:main_app --reload --host 0.0.0.0 --port 8000
