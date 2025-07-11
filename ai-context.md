# AI Context - Windows Diff Tool Development

## Project Overview
This document contains the complete development context for the Windows Diff Tool project, created to provide a Linux-like diff command experience on Windows with enhanced side-by-side comparison and highlighting capabilities.

## User Requirements
- **Primary Need**: Missing the Linux diff command functionality on Windows
- **Specific Feature**: Side-by-side comparison with highlighting
- **Interface Preference**: Both CLI for quick comparisons and GUI for detailed analysis
- **Language Choice**: Python (selected for cross-platform compatibility, rich ecosystem, and ease of development)

## Architecture Decisions

### Language Selection: Python
**Reasons for choosing Python:**
- **Cross-platform compatibility** - works seamlessly on Windows
- **Built-in difflib module** for efficient text comparison algorithms
- **Rich ecosystem** for both CLI (colorama) and GUI (tkinter) development
- **Easy distribution** as standalone executables with PyInstaller
- **Excellent terminal color support** with Windows compatibility

### Core Components

#### 1. diff_engine.py - Core Logic
- **Purpose**: Handles the core file comparison logic
- **Key Classes**:
  - `DiffType`: Enum for different types of changes (EQUAL, DELETE, INSERT, REPLACE)
  - `DiffLine`: Represents a single line in the diff with metadata
  - `DiffEngine`: Main comparison engine with configurable options
- **Key Features**:
  - Uses `difflib.SequenceMatcher` for efficient comparison
  - Supports ignore whitespace option
  - Handles multiple file encodings (UTF-8, Latin-1)
  - Provides statistics calculation
  - Maintains line alignment for side-by-side display

#### 2. cli.py - Command Line Interface
- **Purpose**: Provides colored terminal output for quick comparisons
- **Key Classes**:
  - `ColoredFormatter`: Handles terminal color formatting
  - `SideBySideFormatter`: Manages side-by-side layout
- **Key Features**:
  - Windows-compatible colored output using colorama
  - Configurable output width
  - Statistics display option
  - Proper exit codes (0 for no differences, 1 for differences, 2 for errors)
  - Truncation handling for long lines

#### 3. gui.py - Graphical Interface
- **Purpose**: Provides windowed interface for detailed file analysis
- **Key Classes**:
  - `DiffGUI`: Main GUI application class
- **Key Features**:
  - File browser integration
  - Synchronized scrolling between panes
  - Real-time statistics in status bar
  - Color-coded diff highlighting
  - Resizable interface with proper scaling
  - Ignore whitespace checkbox

#### 4. main.py - Unified Entry Point
- **Purpose**: Single entry point that routes to CLI or GUI based on arguments
- **Key Features**:
  - Automatic interface selection (GUI if no files specified)
  - Argument parsing and forwarding
  - Error handling for missing dependencies
  - Help text with usage examples

### Technical Implementation Details

#### Color Scheme
- **Red (#f8d7da, #721c24)**: Deleted lines
- **Green (#d4edda, #155724)**: Added lines  
- **Yellow (#fff3cd, #856404)**: Changed lines
- **Gray (#f8f9fa, #6c757d)**: Unchanged lines

#### File Handling
- **Encoding Support**: UTF-8 primary, Latin-1 fallback
- **Line Processing**: Strips line endings, handles empty files
- **Error Handling**: Graceful handling of file not found, permission errors

#### Diff Algorithm
- **Primary**: Python's `difflib.SequenceMatcher`
- **Alignment**: Maintains line-by-line alignment for side-by-side display
- **Optimization**: Efficient memory usage with line-by-line processing

## Development Process

### Phase 1: Core Engine (Completed)
- Implemented `DiffEngine` class with basic comparison logic
- Added support for ignore whitespace option
- Implemented proper line alignment for side-by-side display
- Created `DiffLine` and `DiffType` data structures

### Phase 2: CLI Interface (Completed)
- Implemented colored terminal output using colorama
- Created side-by-side formatting with configurable width
- Added statistics display and proper exit codes
- Implemented argument parsing with comprehensive options

### Phase 3: GUI Interface (Completed)
- Created tkinter-based GUI with file browser integration
- Implemented synchronized scrolling between text panes
- Added real-time statistics display
- Created color-coded diff highlighting
- Fixed initialization order issue with colors

### Phase 4: Integration and Testing (Completed)
- Created unified entry point with automatic interface selection
- Added Windows batch file launcher
- Created comprehensive test files
- Verified functionality on Windows with PowerShell

### Phase 5: Documentation and Distribution (Completed)
- Created comprehensive README with usage examples
- Added setup.py for proper Python package installation
- Created requirements.txt for dependency management
- Added troubleshooting guide

## Testing Results

### CLI Testing
```bash
# Basic test with statistics
python src/main.py test_files/file1.txt test_files/file2.txt -s

# Results showed:
# - Proper side-by-side alignment
# - Colored output working on Windows
# - Accurate statistics (1 added, 0 deleted, 2 changed, 8 unchanged)
# - Correct line numbering and formatting
```

### GUI Testing
- Successfully launched with `python src/main.py --gui`
- File browser integration working
- Color highlighting applied correctly
- Synchronized scrolling functional

### Batch File Testing
- `.\wdiff.bat` command worked correctly
- Arguments passed through properly
- Output formatting maintained

## Known Issues and Solutions

### Issue 1: GUI Colors Initialization
**Problem**: `AttributeError: 'DiffGUI' object has no attribute 'colors'`
**Solution**: Moved color configuration before GUI setup in `__init__` method
**Status**: Fixed

### Issue 2: PowerShell Batch File Execution
**Problem**: `wdiff.bat` not recognized without explicit path
**Solution**: Use `.\wdiff.bat` syntax in PowerShell
**Status**: Documented in README

### Issue 3: Long Line Truncation
**Problem**: Very long lines can break terminal formatting
**Solution**: Implemented truncation with "..." indicator
**Status**: Implemented

## Future Enhancement Opportunities

### High Priority
1. **Syntax Highlighting**: Add pygments integration for code files
2. **Word-level Differences**: Highlight specific changed words within lines
3. **Directory Comparison**: Compare entire directory structures
4. **Binary File Support**: Handle binary files with hex comparison

### Medium Priority
1. **Export Functionality**: Save results to HTML/PDF
2. **Configuration Files**: User-customizable settings
3. **Plugin System**: Allow custom comparison algorithms
4. **Performance Optimization**: Handle very large files more efficiently

### Low Priority
1. **Integration with VCS**: Git/SVN integration
2. **Network File Support**: Compare files over network
3. **Backup/Restore**: Integrated backup functionality
4. **Themes**: Multiple color schemes

## Development Environment

### Requirements
- Python 3.7+
- colorama>=0.4.6
- pygments>=2.17.2 (for future syntax highlighting)
- tkinter (usually included with Python)

### File Structure
```
diffTool/
├── src/
│   ├── diff_engine.py    # Core comparison logic
│   ├── cli.py           # Command-line interface
│   ├── gui.py           # GUI interface
│   └── main.py          # Unified entry point
├── test_files/          # Sample files for testing
│   ├── file1.txt
│   └── file2.txt
├── requirements.txt     # Dependencies
├── setup.py            # Installation script
├── wdiff.bat           # Windows batch launcher
├── README.md           # Complete documentation
└── ai-context.md       # This file
```

## Code Quality Standards

### Python Standards
- Type hints used throughout for better IDE support
- Docstrings for all public methods
- Error handling with specific exception types
- Following PEP 8 style guidelines

### Testing Standards
- Manual testing with sample files
- CLI and GUI functionality verified
- Windows compatibility confirmed
- Cross-platform considerations addressed

## Deployment Options

### Option 1: Direct Python Execution
```bash
pip install -r requirements.txt
python src/main.py [options] file1 file2
```

### Option 2: Package Installation
```bash
pip install -e .
wdiff [options] file1 file2
```

### Option 3: Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/main.py
```

## Integration Points

### Command Line Integration
- Can be added to Windows PATH for system-wide access
- Supports piping and redirection
- Proper exit codes for scripting

### IDE Integration
- Can be configured as external tool in IDEs
- Supports file comparison from file managers
- GUI can be launched from command line

## Performance Characteristics

### Memory Usage
- Line-by-line processing for large files
- Efficient diff algorithm from Python standard library
- GUI uses scrolled text widgets for large content

### Speed
- Fast comparison using optimized difflib algorithms
- Minimal startup time for CLI interface
- GUI responsive for files up to several thousand lines

## Maintenance Considerations

### Dependencies
- Minimal external dependencies (only colorama required)
- tkinter usually included with Python
- Easy to update and maintain

### Code Organization
- Modular design allows easy extension
- Clear separation of concerns
- Well-documented interfaces

This context document provides complete information for future development, maintenance, and enhancement of the Windows Diff Tool project.
