#!/bin/bash
echo "🧹 Cleaning up the environment and output files..."
rm -rf *.venv __pycache__ .pytest_cache *.log output/ temp/
echo "✅ Cleanup completed."
