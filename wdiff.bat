@echo off
REM Windows Diff Tool - Batch launcher
REM Usage: wdiff.bat [options] file1 file2
REM        wdiff.bat --gui

cd /d "%~dp0"
python src/main.py %*
