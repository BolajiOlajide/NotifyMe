#!/bin/bash

set -e

celery -A manage.celery worker & python manage.py
