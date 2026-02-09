"""
Configuration settings for the AI Project Generator
"""

# Groq Model Configuration
# Available models:
# - "llama-3.1-70b-versatile" (Recommended - Best for structured outputs)
# - "llama-3.3-70b-versatile" (Fast and reliable)
# - "mixtral-8x7b-32768" (Good for complex tasks)
# - "gemma2-9b-it" (Lightweight option)

GROQ_MODEL = "moonshotai/kimi-k2-instruct-0905"

# Agent Configuration
DEFAULT_RECURSION_LIMIT = 100
MAX_RECURSION_LIMIT = 200
MIN_RECURSION_LIMIT = 50

# Project Configuration
PROJECT_OUTPUT_DIR = "generated_project"

# Debug Settings
ENABLE_DEBUG = True
ENABLE_VERBOSE = True
