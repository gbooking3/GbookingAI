#!/bin/bash

# Exit on any error
set -e

# Get the absolute path of the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Move to the parent directory of the script (optional if scripts are relative)
cd "$SCRIPT_DIR/.."

# Run backend setup
echo "🚀 Running backend_setup.sh..."
bash "$SCRIPT_DIR/backend_setup.sh"

# Run frontend setup
echo "🚀 Running frontend_setup.sh..."
bash "$SCRIPT_DIR/frontend_setup.sh"

echo "✅ Fullstack setup complete!"
