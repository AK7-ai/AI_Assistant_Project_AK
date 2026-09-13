"""
config.py

Global configuration for the project.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent

# Path to the PMData dataset
DATA_DIR = PROJECT_ROOT / "PMData"

# Default participant for testing
DEFAULT_PARTICIPANT = "p01"

OLLAMA_BASE_URL = "http://ollama.lst:11434/v1"

MODEL_NAME = "gpt-oss:20b"

API_KEY = "ollama"
