import argparse
import sys
import os
from typing import List
from colorama import init, Fore, Back, Style
from diff_engine import DiffEngine, DiffLine, DiffType

# Initialize colorama for Windows support
init(autoreset=True)

class ColoredFormatter:
    """Handles colored terminal output for diffs"""
    
    def __init__(self, use_color: bool = True):
        self.use_color = use_color
        
    def format_line(self, line: DiffLine, side: str = "left") -> str:
        """Format a single line with appropriate coloring"""
        if not self.use_color:
            return self._format_plain_line(line)
        
        line_num_str = f"{line.line_num:4d}" if line.line_num else "    "
        content = line.content
        
        if line.diff_type == DiffType.EQUAL:
            return f"{Style.DIM}{line_num_str}{Style.RESET_ALL} {content}"
        elif line.diff_type == DiffType.DELETE:
            if line.line_num is not None:
                return f"{Fore.RED}{line_num_str}{Style.RESET_ALL} {Fore.RED}- {content}{Style.RESET_ALL}"
            else:
                return f"{Style.DIM}    {Style.RESET_ALL} "
        elif line.diff_type == DiffType.INSERT:
            if line.line_num is not None:
                return f"{Fore.GREEN}{line_num_str}{Style.RESET_ALL} {Fore.GREEN}+ {content}{Style.RESET_ALL}"
            else:
                return f"{Style.DIM}    {Style.RESET_ALL} "
        elif line.diff_type == DiffType.REPLACE:
            if line.line_num is not None:
                color = Fore.RED if side == "left" else Fore.GREEN
                symbol = "~" if side == "left" else "~"
                return f"{color}{line_num_str}{Style.RESET_ALL} {color}{symbol} {content}{Style.RESET_ALL}"
            else:
                return f"{Style.DIM}    {Style.RESET_ALL} "
        
        return f"{line_num_str} {content}"
    
    def _format_plain_line(self, line: DiffLine) -> str:
        """Format line without colors"""
        line_num_str = f"{line.line_num:4d}" if line.line_num else "    "
        content = line.content
        
        if line.diff_type == DiffType.DELETE and line.line_num is not None:
            return f"{line_num_str} - {content}"
        elif line.diff_type == DiffType.INSERT and line.line_num is not None:
            return f"{line_num_str} + {content}"
        elif line.diff_type == DiffType.REPLACE and line.line_num is not None:
            return f"{line_num_str} ~ {content}"
        else:
            return f"{line_num_str} {content}"

class SideBySideFormatter:
    """Formats diff output in side-by-side view"""
    
    def __init__(self, use_color: bool = True, width: int = 80):
        self.use_color = use_color
        self.width = width
        self.half_width = (width - 3) // 2  # Account for separator
        self.formatter = ColoredFormatter(use_color)
    
    def format_diff(self, left_diff: List[DiffLine], right_diff: List[DiffLine], 
                   file1: str, file2: str) -> str:
        """Format the entire diff in side-by-side view"""
        output = []
        
        # Header
        header = self._format_header(file1, file2)
        output.append(header)
        output.append("=" * self.width)
        
        # Content
        for i, (left_line, right_line) in enumerate(zip(left_diff, right_diff)):
            left_formatted = self.formatter.format_line(left_line, "left")
            right_formatted = self.formatter.format_line(right_line, "right")
            
            # Truncate lines if they're too long
            left_truncated = self._truncate_line(left_formatted, self.half_width)
            right_truncated = self._truncate_line(right_formatted, self.half_width)
            
            # Combine with separator
            line = f"{left_truncated:<{self.half_width}} | {right_truncated}"
            output.append(line)
        
        return "\n".join(output)
    
    def _format_header(self, file1: str, file2: str) -> str:
        """Format the header showing filenames"""
        left_header = f"< {os.path.basename(file1)}"
        right_header = f"> {os.path.basename(file2)}"
        
        left_padded = f"{left_header:<{self.half_width}}"
        right_padded = f"{right_header:<{self.half_width}}"
        
        if self.use_color:
            return f"{Style.BRIGHT}{left_padded}{Style.RESET_ALL} | {Style.BRIGHT}{right_padded}{Style.RESET_ALL}"
        else:
            return f"{left_padded} | {right_padded}"
    
    def _truncate_line(self, line: str, max_width: int) -> str:
        """Truncate line to fit within width, handling ANSI codes"""
        # Simple truncation for now - could be improved to handle ANSI codes better
        if len(line) <= max_width:
            return line
        return line[:max_width-3] + "..."

def print_stats(stats: dict):
    """Print diff statistics"""
    print(f"\n{Style.BRIGHT}Statistics:{Style.RESET_ALL}")
    print(f"  Lines added:   {Fore.GREEN}{stats['added_lines']}{Style.RESET_ALL}")
    print(f"  Lines deleted: {Fore.RED}{stats['deleted_lines']}{Style.RESET_ALL}")
    print(f"  Lines changed: {Fore.YELLOW}{stats['changed_lines']}{Style.RESET_ALL}")
    print(f"  Lines unchanged: {stats['unchanged_lines']}")

def main():
    parser = argparse.ArgumentParser(description="Windows Diff Tool - Side-by-side file comparison")
    parser.add_argument("file1", help="First file to compare")
    parser.add_argument("file2", help="Second file to compare")
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
    
    # Check if files exist
    if not os.path.exists(args.file1):
        print(f"Error: File '{args.file1}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.file2):
        print(f"Error: File '{args.file2}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Create diff engine
    engine = DiffEngine(
        ignore_whitespace=args.ignore_whitespace,
        context_lines=args.context
    )
    
    try:
        # Compare files
        left_diff, right_diff = engine.compare_files(args.file1, args.file2)
        
        # Format output
        formatter = SideBySideFormatter(
            use_color=not args.no_color,
            width=args.width
        )
        
        diff_output = formatter.format_diff(left_diff, right_diff, args.file1, args.file2)
        print(diff_output)
        
        # Show statistics if requested
        if args.stats:
            stats = engine.get_stats(left_diff, right_diff)
            print_stats(stats)
        
        # Exit with appropriate code
        has_differences = any(line.diff_type != DiffType.EQUAL for line in left_diff)
        sys.exit(1 if has_differences else 0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
