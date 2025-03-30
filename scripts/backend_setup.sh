#!/bin/bash

# Exit if any command fails
set -e

# Get Python 3 version (major.minor)
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
VENV_PACKAGE="python${PYTHON_VERSION}-venv"

echo "🔍 Detected Python version: $PYTHON_VERSION"

# Check if venv module is available
if ! python3 -m venv --help > /dev/null 2>&1; then
  echo "⚠️  python3-venv is not installed for Python $PYTHON_VERSION"
  echo "➡️  Installing: $VENV_PACKAGE"
  sudo apt update
  sudo apt install -y "$VENV_PACKAGE"
fi

# Variables
BACKEND_DIR="backend"

# Create backend directory and enter it
mkdir -p "$BACKEND_DIR"
cd "$BACKEND_DIR"

# Create virtual environment
python3 -m venv venv

# Activate venv just for pip install step
source venv/bin/activate

# Create requirements.txt
cat <<EOF > requirements.txt
flask
flask_cors
python-dotenv
flask-pymongo
EOF

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat <<EOL > .env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_RUN_PORT=8000
SECRET_KEY=mysecretkey
MONGO_URI=#<My MongoDB Cluster Link>
EOL

# Create app.py
cat <<'EOF' > app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo_client = PyMongo(app)

if __name__ == '__main__':
    app.run(debug=True)
EOF

# Create .gitignore
cat <<EOF > .gitignore
# Python virtual environment
venv/

# Python cache
__pycache__/
*.py[cod]

# Environment variables
.env

# Editor and system files
.vscode/
.idea/
.DS_Store
Thumbs.db

# Logs
*.log
EOF


echo ""
echo "✅ Backend environment setup complete!"
echo ""
echo "👉 To start developing, run:"
echo "cd $BACKEND_DIR"
echo "source venv/bin/activate"
echo "flask run"
