#!/usr/bin/env python3
"""
GUI Diff Tool - Graphical file comparison with optional file arguments
"""

import sys
import argparse
import os
from pathlib import Path

# Add src directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for gdiff command"""
    parser = argparse.ArgumentParser(
        description="GUI Diff Tool - Graphical file comparison",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gdiff                               # Launch GUI with file browser
  gdiff file1.txt file2.txt          # Launch GUI with files pre-selected
        """
    )
    
    parser.add_argument("file1", nargs="?", help="First file to compare (optional)")
    parser.add_argument("file2", nargs="?", help="Second file to compare (optional)")
    parser.add_argument("-w", "--ignore-whitespace", action="store_true", 
                       help="Ignore whitespace differences (pre-set in GUI)")
    parser.add_argument("--user-dir", help="Original user working directory for relative path resolution")
    
    args = parser.parse_args()
    
    # Validate file arguments if provided
    if args.file1 and not args.file2:
        parser.error("If file1 is provided, file2 must also be provided")
    if args.file2 and not args.file1:
        parser.error("If file2 is provided, file1 must also be provided")
    
    # Convert relative paths to absolute paths
    # Use user directory if provided, otherwise use current directory
    base_dir = args.user_dir if args.user_dir else os.getcwd()
    
    file1 = None
    file2 = None
    
    if args.file1:
        if os.path.isabs(args.file1):
            file1 = args.file1
        else:
            file1 = os.path.join(base_dir, args.file1)
        file1 = os.path.abspath(file1)
    
    if args.file2:
        if os.path.isabs(args.file2):
            file2 = args.file2
        else:
            file2 = os.path.join(base_dir, args.file2)
        file2 = os.path.abspath(file2)
    
    # Check if files exist
    if file1 and not os.path.exists(file1):
        print(f"Error: File '{args.file1}' not found", file=sys.stderr)
        sys.exit(1)
    
    if file2 and not os.path.exists(file2):
        print(f"Error: File '{args.file2}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        from gui import DiffGUI
        import tkinter as tk
        
        # Create GUI
        root = tk.Tk()
        app = DiffGUI(root)
        
        # Pre-populate files if provided
        if file1 and file2:
            app.file1_var.set(file1)
            app.file2_var.set(file2)
            app.file1_path = file1
            app.file2_path = file2
            
            # Set ignore whitespace if specified
            if args.ignore_whitespace:
                app.ignore_whitespace_var.set(True)
            
            # Automatically compare files
            app.compare_files()
        
        # Start GUI event loop
        root.mainloop()
        
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}", file=sys.stderr)
        print("Install tkinter to use the GUI interface", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
