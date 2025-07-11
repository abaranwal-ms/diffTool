# Issue #001: gdiff.bat Relative Path Resolution Problem

**Status:** 🔴 Open  
**Priority:** High  
**Category:** Bug  
**Created:** 2025-01-11  
**Assigned:** TBD  

## Issue Summary
**Problem:** `gdiff.bat` fails to find files when using relative paths from directories other than the tool's installation directory.

**Error Message:** `Error: File 'file1.txt' not found`

**Severity:** High - Breaks expected user workflow

## Reproduction Steps

1. Navigate to the test_files directory:
   ```cmd
   cd C:\poc\diffTool\test_files\
   ```

2. Run gdiff with relative paths:
   ```cmd
   gdiff .\file1.txt .\file2.txt
   ```

3. Observe the error:
   ```
   Error: File '.\file1.txt' not found
   ```

## Root Cause Analysis

### The Problem Chain

1. **User's Expectation:** When running `gdiff .\file1.txt .\file2.txt` from `C:\poc\diffTool\test_files\`, the user expects the tool to resolve paths relative to their current working directory.

2. **Batch File Behavior:** `gdiff.bat` contains:
   ```batch
   @echo off
   cd /d "%~dp0"
   python src/gdiff.py %*
   ```

3. **Working Directory Change:** The `cd /d "%~dp0"` command changes the working directory from the user's location (`C:\poc\diffTool\test_files\`) to the batch file's location (`C:\poc\diffTool\`).

4. **Path Resolution Failure:** When `gdiff.py` tries to resolve `.\file1.txt`, it now looks in `C:\poc\diffTool\file1.txt` instead of `C:\poc\diffTool\test_files\file1.txt`.

### Technical Details

- **gdiff.py** uses `os.path.abspath(args.file1)` to convert relative paths to absolute paths
- This conversion happens AFTER the batch file has already changed the working directory
- The Python script has no knowledge of the user's original working directory

## Impact Assessment

### Affected Use Cases
- ✅ **Works:** Running from tool directory: `gdiff test_files\file1.txt test_files\file2.txt`
- ✅ **Works:** Using absolute paths: `gdiff C:\full\path\to\file1.txt C:\full\path\to\file2.txt`
- ❌ **Fails:** Running from any subdirectory with relative paths: `gdiff .\file1.txt .\file2.txt`
- ❌ **Fails:** Running from any other directory with relative paths: `gdiff file1.txt file2.txt`

### User Experience Impact
- **Breaks intuitive workflow:** Users expect to navigate to their files' directory and use relative paths
- **Forces workarounds:** Users must use absolute paths or run from tool directory
- **Inconsistent with standard tools:** Most CLI tools resolve paths relative to the user's current directory

## Test Results

### Environment
- **OS:** Windows 11
- **Tool Location:** `C:\poc\diffTool\`
- **Test Files:** `C:\poc\diffTool\test_files\file1.txt`, `C:\poc\diffTool\test_files\file2.txt`

### Test Cases

| Test Case | Command | Working Directory | Result | Expected |
|-----------|---------|------------------|---------|----------|
| 1 | `gdiff .\file1.txt .\file2.txt` | `C:\poc\diffTool\test_files\` | ❌ File not found | ✅ Should work |
| 2 | `gdiff file1.txt file2.txt` | `C:\poc\diffTool\test_files\` | ❌ File not found | ✅ Should work |
| 3 | `gdiff test_files\file1.txt test_files\file2.txt` | `C:\poc\diffTool\` | ✅ Works | ✅ Works |
| 4 | `gdiff C:\poc\diffTool\test_files\file1.txt C:\poc\diffTool\test_files\file2.txt` | Any directory | ✅ Works | ✅ Works |

## Proposed Solutions

### Option 1: Preserve User's Working Directory (Recommended)
Modify `gdiff.bat` to capture the user's working directory before changing it:

```batch
@echo off
set "USER_DIR=%CD%"
cd /d "%~dp0"
python src/gdiff.py --user-dir "%USER_DIR%" %*
```

Then modify `gdiff.py` to use the user's directory for relative path resolution.

### Option 2: Use Pushd/Popd
```batch
@echo off
pushd "%~dp0"
python src/gdiff.py %*
popd
```

### Option 3: No Directory Change
```batch
@echo off
python "%~dp0src/gdiff.py" %*
```

This requires ensuring Python can find the modules, possibly by modifying `sys.path` in the Python script.

## Implementation Considerations

### For Option 1 (Recommended)
- **Pros:** Maintains user expectations, preserves current tool architecture
- **Cons:** Requires changes to both batch file and Python script
- **Complexity:** Medium

### For Option 2
- **Pros:** Simple batch file change, preserves user's directory after execution
- **Cons:** Still changes directory during execution, may have side effects
- **Complexity:** Low

### For Option 3
- **Pros:** Simplest solution, no directory changes
- **Cons:** May break Python module imports, requires path adjustments
- **Complexity:** Low to Medium

## Workarounds (Current)

Until the issue is fixed, users can:

1. **Use absolute paths:**
   ```cmd
   gdiff C:\full\path\to\file1.txt C:\full\path\to\file2.txt
   ```

2. **Run from tool directory:**
   ```cmd
   cd C:\poc\diffTool
   gdiff test_files\file1.txt test_files\file2.txt
   ```

3. **Use relative paths from tool directory:**
   ```cmd
   cd C:\poc\diffTool
   gdiff .\test_files\file1.txt .\test_files\file2.txt
   ```

## Related Issues

- This issue likely affects `cdiff.bat` as well if it has the same structure
- Any other batch files in the project may have similar problems
- The issue is specific to Windows batch file implementation

## Fix Priority

**High Priority** - This breaks basic user expectations and common workflows. The fix should be implemented to ensure proper relative path handling consistent with standard CLI tool behavior.

## Testing Requirements

After implementing a fix, verify:
1. Relative paths work from any directory
2. Absolute paths continue to work
3. Running from tool directory still works
4. No regression in GUI functionality
5. Cross-platform compatibility (if applicable)

## Resolution Criteria

This issue can be closed when:
- [ ] Relative paths work correctly from any directory
- [ ] All existing functionality continues to work
- [ ] Tests pass for all scenarios in the test table above
- [ ] Documentation is updated to reflect the fix
- [ ] No regressions are introduced

---

**Report Generated:** 2025-01-11 15:18:24 IST  
**Tested Environment:** Windows 11, Python 3.x  
**Tool Version:** Current development version  

## Issue Lifecycle

- **2025-01-11 15:18:24** - Issue created and documented
- **Next:** Issue will be addressed in next iteration
