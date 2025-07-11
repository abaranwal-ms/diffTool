#!/usr/bin/env python3
"""
CLI Diff Tool - Command-line only file comparison
"""

import sys
import os
from pathlib import Path

# Add src directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from cli import main as cli_main

def main():
    """Main entry point for cdiff command"""
    try:
        cli_main()
    except ImportError as e:
        print(f"Error: CLI dependencies not available: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
