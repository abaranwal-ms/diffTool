# Windows Diff Tool

A powerful side-by-side file comparison tool for Windows, inspired by the Linux `diff` command but with enhanced visual features and separate CLI and GUI interfaces.

## Features

- **Side-by-side comparison** with syntax highlighting
- **Separate CLI and GUI** commands for specific use cases
- **Colored terminal output** with Windows support
- **Ignore whitespace** option
- **Statistics** showing added, deleted, and changed lines
- **Cross-platform** Python implementation
- **Easy to use** with simple command-line interface

## Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Interface (Recommended)

Launch the graphical interface:
```bash
python src/gdiff.py
```

**Or use the batch file:**
```bash
gdiff.bat
```

**Launch GUI with files pre-selected:**
```bash
python src/gdiff.py file1.txt file2.txt
```

**Or use the batch file:**
```bash
gdiff.bat file1.txt file2.txt
```

### Command Line Interface

Compare two files:
```bash
python src/cdiff.py file1.txt file2.txt
```

**Or use the batch file:**
```bash
cdiff.bat file1.txt file2.txt
```

#### CLI Options

```bash
python src/cdiff.py [options] file1 file2

Options:
  -h, --help            Show help message
  -w, --ignore-whitespace
                        Ignore whitespace differences
  -c CONTEXT, --context CONTEXT
                        Number of context lines to show (default: 3)
  --no-color            Disable colored output
  --width WIDTH         Output width (default: 120)
  -s, --stats           Show statistics
```

#### GUI Options

```bash
python src/gdiff.py [options] [file1] [file2]

Options:
  -h, --help            Show help message
  -w, --ignore-whitespace
                        Ignore whitespace differences (pre-set in GUI)
  file1                 First file to compare (optional)
  file2                 Second file to compare (optional)
```

### Examples

1. **Basic CLI comparison:**
   ```bash
   cdiff.bat file1.txt file2.txt
   ```

2. **CLI with ignore whitespace:**
   ```bash
   cdiff.bat -w file1.txt file2.txt
   ```

3. **CLI with statistics:**
   ```bash
   cdiff.bat -s file1.txt file2.txt
   ```

4. **CLI with custom width:**
   ```bash
   cdiff.bat --width 100 file1.txt file2.txt
   ```

5. **Launch GUI:**
   ```bash
   gdiff.bat
   ```

6. **Launch GUI with files pre-selected:**
   ```bash
   gdiff.bat file1.txt file2.txt
   ```

## Features in Detail

### Side-by-Side View
- Files are displayed side-by-side for easy comparison
- Line numbers are shown for both files
- Changes are aligned properly for visual clarity

### Color Coding
- **Red**: Deleted lines (only in left file)
- **Green**: Added lines (only in right file)
- **Yellow**: Changed lines (different in both files)
- **Gray**: Unchanged lines

### GUI Features
- **File browser** for easy file selection
- **Synchronized scrolling** between panes
- **Real-time statistics** in status bar
- **Ignore whitespace** checkbox
- **Resizable interface** with proper scaling

### CLI Features
- **Colored terminal output** (works on Windows)
- **Configurable output width**
- **Context line control**
- **Statistics display**
- **Proper exit codes** (0 for no differences, 1 for differences, 2 for errors)

## Technical Details

### Architecture
- **diff_engine.py**: Core comparison logic using Python's difflib
- **cli.py**: Command-line interface with colored output
- **gui.py**: Tkinter-based graphical interface
- **main.py**: Unified entry point for both interfaces

### Dependencies
- **colorama**: Windows-compatible colored terminal output
- **tkinter**: GUI framework (usually included with Python)
- **Python 3.7+**: Required for type hints and modern features

### File Support
- **Text files**: UTF-8 and Latin-1 encoding support
- **Any file type**: Basic text comparison works with any file
- **Large files**: Efficient memory usage with line-by-line processing

## Adding to PATH (Optional)

To use `cdiff` and `gdiff` from anywhere on your system:

1. Add the diffTool directory to your Windows PATH environment variable
2. Or create `.cmd` files in a directory that's in your PATH:
   ```batch
   # cdiff.cmd
   @echo off
   "C:\path\to\diffTool\cdiff.bat" %*
   
   # gdiff.cmd
   @echo off
   "C:\path\to\diffTool\gdiff.bat" %*
   ```

Then you can use:
```bash
cdiff file1.txt file2.txt
gdiff file1.txt file2.txt
gdiff
```

## Building Executable (Optional)

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create executable:
   ```bash
   pyinstaller --onefile --windowed src/main.py
   ```

## Troubleshooting

### Python not found
- Ensure Python is installed and in your PATH
- Try `python3` instead of `python` on some systems

### Tkinter not available
- On Linux: `sudo apt-get install python3-tk`
- On Windows: Tkinter is usually included with Python

### Colors not working
- Ensure colorama is installed: `pip install colorama`
- Use `--no-color` flag to disable colors

## License

This project is open source and available under the MIT License.

## Development & AI Context

For detailed development information, architecture decisions, and AI-assisted development context, see [ai-context.md](ai-context.md). This document contains:

- Complete development process and decisions
- Technical implementation details
- Testing results and known issues
- Future enhancement roadmap
- Code quality standards and deployment options

## Contributing

Contributions are welcome! Please feel free to submit pull requests or report issues. Before contributing, please review the [ai-context.md](ai-context.md) file for detailed technical context and development standards.

## Future Enhancements

Based on the development roadmap in [ai-context.md](ai-context.md):

### High Priority
- **Syntax Highlighting**: Add pygments integration for code files
- **Word-level Differences**: Highlight specific changed words within lines
- **Directory Comparison**: Compare entire directory structures
- **Binary File Support**: Handle binary files with hex comparison

### Medium Priority
- **Export Functionality**: Save results to HTML/PDF
- **Configuration Files**: User-customizable settings
- **Plugin System**: Allow custom comparison algorithms
- **Performance Optimization**: Handle very large files more efficiently

### Low Priority
- **Integration with VCS**: Git/SVN integration
- **Network File Support**: Compare files over network
- **Backup/Restore**: Integrated backup functionality
- **Themes**: Multiple color schemes
