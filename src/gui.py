import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import List, Optional
from diff_engine import DiffEngine, DiffLine, DiffType

class DiffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Diff Tool")
        self.root.geometry("1200x800")
        
        # Initialize diff engine
        self.engine = DiffEngine()
        
        # Current file paths
        self.file1_path = ""
        self.file2_path = ""
        
        # Configure colors
        self.colors = {
            DiffType.EQUAL: {"bg": "#f8f9fa", "fg": "#6c757d"},
            DiffType.DELETE: {"bg": "#f8d7da", "fg": "#721c24"},
            DiffType.INSERT: {"bg": "#d4edda", "fg": "#155724"},
            DiffType.REPLACE: {"bg": "#fff3cd", "fg": "#856404"}
        }
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # File 1 selection
        ttk.Label(file_frame, text="File 1:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file1_var = tk.StringVar()
        self.file1_entry = ttk.Entry(file_frame, textvariable=self.file1_var, width=50)
        self.file1_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_file1).grid(row=0, column=2)
        
        # File 2 selection
        ttk.Label(file_frame, text="File 2:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.file2_var = tk.StringVar()
        self.file2_entry = ttk.Entry(file_frame, textvariable=self.file2_var, width=50)
        self.file2_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        ttk.Button(file_frame, text="Browse", command=self.browse_file2).grid(row=1, column=2, pady=(5, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.ignore_whitespace_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Ignore whitespace", 
                       variable=self.ignore_whitespace_var).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(options_frame, text="Compare Files", 
                  command=self.compare_files).grid(row=0, column=1, padx=(20, 0))
        
        # Main comparison frame
        comparison_frame = ttk.Frame(main_frame)
        comparison_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        comparison_frame.columnconfigure(0, weight=1)
        comparison_frame.columnconfigure(1, weight=1)
        comparison_frame.rowconfigure(1, weight=1)
        
        # File labels
        self.file1_label = ttk.Label(comparison_frame, text="File 1", font=("Arial", 10, "bold"))
        self.file1_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.file2_label = ttk.Label(comparison_frame, text="File 2", font=("Arial", 10, "bold"))
        self.file2_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Text widgets with scrollbars
        self.text1 = scrolledtext.ScrolledText(comparison_frame, wrap=tk.NONE, width=50, height=30)
        self.text1.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.text2 = scrolledtext.ScrolledText(comparison_frame, wrap=tk.NONE, width=50, height=30)
        self.text2.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Synchronize scrolling
        self.text1.config(yscrollcommand=self.sync_scroll)
        self.text2.config(yscrollcommand=self.sync_scroll)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure text widget tags for coloring
        self.configure_text_tags()
    
    def configure_text_tags(self):
        """Configure text widget tags for different diff types"""
        for text_widget in [self.text1, self.text2]:
            for diff_type, colors in self.colors.items():
                text_widget.tag_config(diff_type.value, 
                                     background=colors["bg"], 
                                     foreground=colors["fg"])
    
    def sync_scroll(self, *args):
        """Synchronize scrolling between text widgets"""
        if args[0] == 'moveto':
            self.text1.yview_moveto(args[1])
            self.text2.yview_moveto(args[1])
    
    def browse_file1(self):
        """Browse for first file"""
        filename = filedialog.askopenfilename(
            title="Select first file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file1_var.set(filename)
            self.file1_path = filename
    
    def browse_file2(self):
        """Browse for second file"""
        filename = filedialog.askopenfilename(
            title="Select second file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file2_var.set(filename)
            self.file2_path = filename
    
    def compare_files(self):
        """Compare the selected files"""
        file1 = self.file1_var.get().strip()
        file2 = self.file2_var.get().strip()
        
        if not file1 or not file2:
            messagebox.showerror("Error", "Please select both files")
            return
        
        if not os.path.exists(file1):
            messagebox.showerror("Error", f"File not found: {file1}")
            return
        
        if not os.path.exists(file2):
            messagebox.showerror("Error", f"File not found: {file2}")
            return
        
        try:
            # Update status
            self.status_var.set("Comparing files...")
            self.root.update()
            
            # Configure engine
            self.engine.ignore_whitespace = self.ignore_whitespace_var.get()
            
            # Compare files
            left_diff, right_diff = self.engine.compare_files(file1, file2)
            
            # Display results
            self.display_diff(left_diff, right_diff, file1, file2)
            
            # Update status with statistics
            stats = self.engine.get_stats(left_diff, right_diff)
            status_text = f"Added: {stats['added_lines']}, Deleted: {stats['deleted_lines']}, Changed: {stats['changed_lines']}, Unchanged: {stats['unchanged_lines']}"
            self.status_var.set(status_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare files: {str(e)}")
            self.status_var.set("Error occurred")
    
    def display_diff(self, left_diff: List[DiffLine], right_diff: List[DiffLine], 
                    file1: str, file2: str):
        """Display the diff results in the text widgets"""
        # Clear existing content
        self.text1.delete(1.0, tk.END)
        self.text2.delete(1.0, tk.END)
        
        # Update file labels
        self.file1_label.config(text=f"File 1: {os.path.basename(file1)}")
        self.file2_label.config(text=f"File 2: {os.path.basename(file2)}")
        
        # Display diff lines
        for left_line, right_line in zip(left_diff, right_diff):
            # Format left line
            left_text = self.format_line(left_line)
            left_start = self.text1.index(tk.INSERT)
            self.text1.insert(tk.END, left_text + "\n")
            left_end = self.text1.index(tk.INSERT + "-1c")
            self.text1.tag_add(left_line.diff_type.value, left_start, left_end)
            
            # Format right line
            right_text = self.format_line(right_line)
            right_start = self.text2.index(tk.INSERT)
            self.text2.insert(tk.END, right_text + "\n")
            right_end = self.text2.index(tk.INSERT + "-1c")
            self.text2.tag_add(right_line.diff_type.value, right_start, right_end)
        
        # Scroll to top
        self.text1.see(1.0)
        self.text2.see(1.0)
    
    def format_line(self, line: DiffLine) -> str:
        """Format a diff line for display"""
        line_num = f"{line.line_num:4d}" if line.line_num else "    "
        
        if line.diff_type == DiffType.DELETE and line.line_num is not None:
            return f"{line_num} - {line.content}"
        elif line.diff_type == DiffType.INSERT and line.line_num is not None:
            return f"{line_num} + {line.content}"
        elif line.diff_type == DiffType.REPLACE and line.line_num is not None:
            return f"{line_num} ~ {line.content}"
        else:
            return f"{line_num}   {line.content}"

def main():
    root = tk.Tk()
    app = DiffGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
