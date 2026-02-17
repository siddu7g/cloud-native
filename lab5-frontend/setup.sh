#!/bin/bash
# Lab 5 Frontend Setup Script
# Run this after installing Node.js 18+ from https://nodejs.org

set -e

echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed."
    echo "Please install Node.js 18+ from https://nodejs.org (LTS version)"
    exit 1
fi

NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "ERROR: Node.js 18+ required. Found: $(node -v)"
    exit 1
fi

echo "Node $(node -v) OK"
echo "npm $(npm -v) OK"

echo ""
echo "Installing dependencies..."
npm install

echo ""
echo "Setup complete. Start the dev server with: npm run dev"
echo "Then open http://localhost:3000"
