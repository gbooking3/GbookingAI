#!/bin/bash

# Exit on error
set -e

# Project name
PROJECT_NAME="frontend"

echo "🚀 Creating Vite React project: $PROJECT_NAME..."

# Create Vite React project
npm create vite@latest $PROJECT_NAME -- --template react --force

# Navigate into the project directory
cd $PROJECT_NAME

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install Tailwind CSS
echo "🎨 Installing Tailwind CSS..."
npm install tailwindcss @tailwindcss/vite


# Configure tailwind.config.js
echo "⚙️ Updating Tailwind configuration..."
cat > vite.config.js <<EOF
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
})
EOF

rm -rf src/{App,index}.css
sed -i '4d' src/App.jsx
sed -i '3d' src/main.jsx

cat > init_project.sh <<EOF
# Start the development server
echo "🚀 Starting Vite development server..."
npm run dev
EOF