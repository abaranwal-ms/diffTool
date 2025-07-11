@echo off
set "USER_DIR=%CD%"
cd /d "%~dp0"
python src/gdiff.py --user-dir "%USER_DIR%" %*
