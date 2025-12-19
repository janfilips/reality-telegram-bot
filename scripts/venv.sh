
#!/bin/bash
# Ensure this script is sourced, not executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Please run this script with: source $0" >&2
  exit 1
fi

python3.13 -m venv .venv
source .venv/bin/activate

pip3 install poetry

# On Windows run:
# .venv\Scripts\Activate
# On macOS/Linux run:
export $(grep -v '^#' .env | xargs)

# Clean up old Python bytecode files
find . -type d -name "__pycache__" -exec rm -rf {} +

# Load environment variables from the .env.devel file
if [ -f .env.devel ]; then
  set -o allexport
  source .env.devel
  set +o allexport
fi

poetry install --no-root

export KMP_DUPLICATE_LIB_OK=TRUE

which python3
