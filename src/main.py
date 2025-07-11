#!/usr/bin/env python3
"""
Windows Diff Tool - Main entry point
Provides both CLI and GUI interfaces for file comparison
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

def main():
    parser = argparse.ArgumentParser(
        description="Windows Diff Tool - Side-by-side file comparison",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py file1.txt file2.txt           # CLI comparison
  python main.py --gui                         # Launch GUI
  python main.py -w file1.txt file2.txt       # Ignore whitespace
  python main.py -s file1.txt file2.txt       # Show statistics
        """
    )
    
    parser.add_argument("file1", nargs="?", help="First file to compare")
    parser.add_argument("file2", nargs="?", help="Second file to compare")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument("-w", "--ignore-whitespace", action="store_true", 
                       help="Ignore whitespace differences")
    parser.add_argument("-c", "--context", type=int, default=3,
                       help="Number of context lines to show")
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colored output")
    parser.add_argument("--width", type=int, default=120,
                       help="Output width (default: 120)")
    parser.add_argument("-s", "--stats", action="store_true",
                       help="Show statistics")
    
    args = parser.parse_args()
    
    # If GUI is requested or no files provided, launch GUI
    if args.gui or (not args.file1 and not args.file2):
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error: GUI dependencies not available: {e}", file=sys.stderr)
            print("Install tkinter to use the GUI interface", file=sys.stderr)
            sys.exit(1)
    else:
        # Use CLI interface
        if not args.file1 or not args.file2:
            parser.error("Both file1 and file2 are required for CLI mode")
        
        try:
            from cli import main as cli_main
            # Set up sys.argv for CLI module
            cli_args = [sys.argv[0]]  # Script name
            cli_args.extend([args.file1, args.file2])
            
            if args.ignore_whitespace:
                cli_args.append("--ignore-whitespace")
            if args.context != 3:
                cli_args.extend(["--context", str(args.context)])
            if args.no_color:
                cli_args.append("--no-color")
            if args.width != 120:
                cli_args.extend(["--width", str(args.width)])
            if args.stats:
                cli_args.append("--stats")
            
            # Replace sys.argv temporarily
            original_argv = sys.argv
            sys.argv = cli_args
            
            try:
                cli_main()
            finally:
                sys.argv = original_argv
                
        except ImportError as e:
            print(f"Error: CLI dependencies not available: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
