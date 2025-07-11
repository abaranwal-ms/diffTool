import difflib
import re
from typing import List, Tuple, Optional
from enum import Enum


class DiffType(Enum):
    EQUAL = "equal"
    DELETE = "delete"
    INSERT = "insert"
    REPLACE = "replace"


class DiffLine:
    def __init__(self, line_num: Optional[int], content: str, diff_type: DiffType):
        self.line_num = line_num
        self.content = content
        self.diff_type = diff_type

    def __repr__(self):
        return f"DiffLine({self.line_num}, {self.content[:20]}..., {self.diff_type})"


class DiffEngine:
    def __init__(self, ignore_whitespace: bool = False, context_lines: int = 3):
        self.ignore_whitespace = ignore_whitespace
        self.context_lines = context_lines

    def _preprocess_text(self, text: str) -> str:
        """Preprocess text based on settings"""
        if self.ignore_whitespace:
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
        return text

    def _read_file(self, filepath: str) -> List[str]:
        """Read file and return lines"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.rstrip('\n\r') for line in lines]
        except UnicodeDecodeError:
            # Try with different encoding
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
            return [line.rstrip('\n\r') for line in lines]

    def compare_files(self, file1: str, file2: str) -> Tuple[List[DiffLine], List[DiffLine]]:
        """Compare two files and return diff lines for each side"""
        lines1 = self._read_file(file1)
        lines2 = self._read_file(file2)
        
        return self.compare_lines(lines1, lines2)

    def compare_lines(self, lines1: List[str], lines2: List[str]) -> Tuple[List[DiffLine], List[DiffLine]]:
        """Compare two lists of lines and return diff lines for each side"""
        # Preprocess lines if needed
        if self.ignore_whitespace:
            lines1 = [self._preprocess_text(line) for line in lines1]
            lines2 = [self._preprocess_text(line) for line in lines2]

        # Use difflib to get opcodes
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        opcodes = matcher.get_opcodes()

        left_diff = []
        right_diff = []

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                # Lines are the same
                for i, line_idx in enumerate(range(i1, i2)):
                    left_diff.append(DiffLine(line_idx + 1, lines1[line_idx], DiffType.EQUAL))
                    right_diff.append(DiffLine(j1 + i + 1, lines2[j1 + i], DiffType.EQUAL))
            
            elif tag == 'delete':
                # Lines deleted from left
                for line_idx in range(i1, i2):
                    left_diff.append(DiffLine(line_idx + 1, lines1[line_idx], DiffType.DELETE))
                # Add empty lines to right to maintain alignment
                for _ in range(i2 - i1):
                    right_diff.append(DiffLine(None, "", DiffType.DELETE))
            
            elif tag == 'insert':
                # Lines inserted in right
                for line_idx in range(j1, j2):
                    right_diff.append(DiffLine(line_idx + 1, lines2[line_idx], DiffType.INSERT))
                # Add empty lines to left to maintain alignment
                for _ in range(j2 - j1):
                    left_diff.append(DiffLine(None, "", DiffType.INSERT))
            
            elif tag == 'replace':
                # Lines replaced
                max_lines = max(i2 - i1, j2 - j1)
                
                # Add replaced lines
                for i in range(max_lines):
                    if i < (i2 - i1):
                        left_diff.append(DiffLine(i1 + i + 1, lines1[i1 + i], DiffType.REPLACE))
                    else:
                        left_diff.append(DiffLine(None, "", DiffType.REPLACE))
                    
                    if i < (j2 - j1):
                        right_diff.append(DiffLine(j1 + i + 1, lines2[j1 + i], DiffType.REPLACE))
                    else:
                        right_diff.append(DiffLine(None, "", DiffType.REPLACE))

        return left_diff, right_diff

    def get_stats(self, left_diff: List[DiffLine], right_diff: List[DiffLine]) -> dict:
        """Get statistics about the diff"""
        stats = {
            'total_lines_left': len([line for line in left_diff if line.line_num is not None]),
            'total_lines_right': len([line for line in right_diff if line.line_num is not None]),
            'added_lines': len([line for line in right_diff if line.diff_type == DiffType.INSERT]),
            'deleted_lines': len([line for line in left_diff if line.diff_type == DiffType.DELETE]),
            'changed_lines': len([line for line in left_diff if line.diff_type == DiffType.REPLACE]),
            'unchanged_lines': len([line for line in left_diff if line.diff_type == DiffType.EQUAL]),
        }
        return stats
