#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if input was passed
if [ -z "$1" ]; then
  echo "❌ Please provide an English sentence as the first argument."
  echo "Usage: ./run_embody.sh 'I'm angry because you lied to me.'"
  exit 1
fi

# Set defaults
DIALECT="egyptian"
EMOTION="angry"
STYLE="default"

# Call Python pipeline
python embody_pipeline.py --text "$1" --dialect "$DIALECT" --emotion "$EMOTION" --style "$STYLE"
