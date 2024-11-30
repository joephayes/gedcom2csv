#!/bin/bash

set -e

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo "Usage: $(basename $0) path/to/gedcom.ged path/to/output.csv
fi

export LOG_LEVEL=${LOG_LEVEL:-DEBUG}

TMPDIR=$(dirname $2)

if [ ! -d "$TMPDIR" ]; then
    mkdir -p $TMPDIR
fi

if [ ! -d venv ]; then
    python -m venv --prompt gedcomcsv venv
    pip install -e .
fi

venv/bin/gedcom2csv convert $1 > $2

echo "$2 is ready"
exit 0
