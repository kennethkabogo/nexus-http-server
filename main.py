#!/usr/bin/env python3
"""
Main entry point for the Gemini HTTP Server.
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_server.main import main

if __name__ == '__main__':
    main()