#!/usr/bin/env bash
. env/bin/activate
export ROOT=`pwd`
export MANAGE="python $ROOT/manage.py"
export PYTHONPATH="$ROOT"
export DATABASE_URL="postgres://postgres:1@localhost/outputwatcher"

export DEBUG="True"
alias m="$MANAGE"