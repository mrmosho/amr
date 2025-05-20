import sys
import os
from typing import Optional
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import queue
import importlib.util
import subprocess

# Function to check and install required packages
def check_and_install_dependencies():
    required_packages = ['spacy', 'pandas', 'numpy', 'scikit-learn', 'joblib']
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        msg = f"Missing required packages: {', '.join(missing_packages)}\n\nWould you like to install them now?"
        if messagebox.askyesno("Missing Dependencies", msg):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                
                # Special case for spacy - need to download the model
                if 'spacy' in missing_packages:
                    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
                
                messagebox.showinfo("Installation Complete", 
                                   "Dependencies installed successfully. Please restart the application.")
                return False
            except Exception as e:
                messagebox.showerror("Installation Error", 
                                    f"Failed to install dependencies: {str(e)}\n\nPlease install them manually.")
                return False
    return True

# Try to import the detector class, handle import errors
try:
    from detector import SensitiveDataDetector
    detector_import_success = True
except ImportError as e:
    detector_import_success = False
    import_error_message = str(e)
    
  

class SensitiveDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensitive Data Detection System")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set theme colors based on presentation
        self.colors = {
            "primary": "#9c27b0",  # Purple from presentation
            "secondary": "#e91e63",  # Pink from presentation
            "bg": "#f5f5f5",
            "text": "#333333",
            "success": "#4caf50",
            "warning": "#ff9800",
            "danger": "#f44336"
        }
        
        self.root.configure(bg=self.colors["bg"])
        
        # Queue for thread-safe communication
        self.queue = queue.Queue()
        
        # Check for detector import success
        if not detector_import_success:
            messagebox.showerror("Import Error", 
                               f"Failed to import detector module: {import_error_message}\n\n"
                               "This may be due to missing dependencies.")
            
            # Try to check and install dependencies
            if not check_and_install_dependencies():
                self.root.after(1000, self.root.destroy)
                return
            
        # Initialize detector (will load models)
        self.detector = None
        self.init_detector()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start periodic queue check
        self.check_queue()
    
    def init_detector(self):
        """Initialize the detector in a separate thread to avoid UI freezing"""
        # Skip if detector import failed
        if not detector_import_success:
            self.queue.put(("status", "Detector module not available - dependency issue"))
            return
            
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Find models directory - look in different potential locations
            model_locations = [
                os.path.join(current_dir, 'models'),
                os.path.join(current_dir, '..', 'models'),
                os.path.join(current_dir, '..', '..', 'models')
            ]
            
            models_dir = None
            for loc in model_locations:
                if os.path.exists(loc):
                    models_dir = loc
                    break
            
            if not models_dir:
                raise FileNotFoundError("Could not find models directory")
                
            # Paths to model files
            model_path = os.path.join(models_dir, 'sensitive_detector_model.joblib')
            vectorizer_path = os.path.join(models_dir, 'text_vectorizer.joblib')
            
            # Check if model files exist
            if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
                missing_files = []
                if not os.path.exists(model_path):
                    missing_files.append("sensitive_detector_model.joblib")
                if not os.path.exists(vectorizer_path):
                    missing_files.append("text_vectorizer.joblib")
                    
                raise FileNotFoundError(f"Model files not found: {', '.join(missing_files)}")
            
            # Initialize detector
            self.detector = SensitiveDataDetector(
                model_path=model_path,
                vectorizer_path=vectorizer_path
            )
            
            # Update status
            self.queue.put(("status", "Model loaded successfully"))
        except Exception as e:
            self.queue.put(("error", f"Error loading model: {str(e)}"))
    
    def create_widgets(self):
        """Create all the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label with project name styling from the presentation
        title_label = ttk.Label(
            main_frame, 
            text="Sensitive Data Detection and Encryption Security System",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create notebook/tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text analysis tab
        text_tab = ttk.Frame(notebook)
        notebook.add(text_tab, text="Text Analysis")
        
        # File analysis tab
        file_tab = ttk.Frame(notebook)
        notebook.add(file_tab, text="File Analysis")
        
        # Settings tab
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="Settings")
        
        # Setup text analysis tab
        self.setup_text_tab(text_tab)
        
        # Setup file analysis tab
        self.setup_file_tab(file_tab)
        
        # Setup settings tab
        self.setup_settings_tab(settings_tab)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_text_tab(self, parent):
        """Setup the text analysis tab"""
        # Input frame
        input_frame = ttk.LabelFrame(parent, text="Input Text", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text input area
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            wrap=tk.WORD, 
            width=40, 
            height=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        analyze_btn = ttk.Button(
            button_frame, 
            text="Analyze Text", 
            command=self.analyze_text
        )
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame, 
            text="Clear", 
            command=lambda: self.input_text.delete(1.0, tk.END)
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        encrypt_btn = ttk.Button(
            button_frame, 
            text="Encrypt Sensitive Data", 
            command=self.encrypt_sensitive
        )
        encrypt_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Analysis Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results area
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            width=40, 
            height=10, 
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_file_tab(self, parent):
        """Setup the file analysis tab"""
        # File selection frame
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        browse_btn = ttk.Button(
            file_frame, 
            text="Browse", 
            command=self.browse_file
        )
        browse_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        analyze_file_btn = ttk.Button(
            button_frame, 
            text="Analyze File", 
            command=self.analyze_file
        )
        analyze_file_btn.pack(side=tk.LEFT, padx=5)
        
        encrypt_file_btn = ttk.Button(
            button_frame, 
            text="Encrypt File", 
            command=self.encrypt_file
        )
        encrypt_file_btn.pack(side=tk.LEFT, padx=5)
        
        # File analysis results
        file_results_frame = ttk.LabelFrame(parent, text="File Analysis Results", padding="10")
        file_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create a treeview for showing detected sensitive data
        columns = ("Line", "Type", "Value", "Confidence")
        self.file_results_tree = ttk.Treeview(
            file_results_frame,
            columns=columns,
            show="headings"
        )
        
        # Define headings
        for col in columns:
            self.file_results_tree.heading(col, text=col)
            self.file_results_tree.column(col, width=100)
        
        # Add scrollbars
        tree_scroll_y = ttk.Scrollbar(
            file_results_frame, 
            orient=tk.VERTICAL, 
            command=self.file_results_tree.yview
        )
        tree_scroll_x = ttk.Scrollbar(
            file_results_frame, 
            orient=tk.HORIZONTAL, 
            command=self.file_results_tree.xview
        )
        
        self.file_results_tree.configure(
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        # Layout scrollbars and tree
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_results_tree.pack(fill=tk.BOTH, expand=True)
    
    def setup_settings_tab(self, parent):
        """Setup the settings tab"""
        # Sensitivity settings
        sensitivity_frame = ttk.LabelFrame(parent, text="Sensitivity Settings", padding="10")
        sensitivity_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Confidence threshold slider
        ttk.Label(sensitivity_frame, text="Detection Confidence Threshold:").pack(anchor=tk.W, padx=5, pady=5)
        
        self.threshold_var = tk.DoubleVar(value=0.5)
        threshold_slider = ttk.Scale(
            sensitivity_frame, 
            from_=0.0, 
            to=1.0, 
            orient=tk.HORIZONTAL, 
            variable=self.threshold_var, 
            length=300
        )
        threshold_slider.pack(fill=tk.X, padx=5, pady=5)
        
        threshold_label = ttk.Label(sensitivity_frame, textvariable=tk.StringVar(
            value=f"Current: {self.threshold_var.get():.2f}")
        )
        threshold_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # Update label when slider changes
        def update_threshold_label(*args):
            threshold_label.config(text=f"Current: {self.threshold_var.get():.2f}")
        
        self.threshold_var.trace_add("write", update_threshold_label)
        
        # Category selection
        category_frame = ttk.LabelFrame(parent, text="Detection Categories", padding="10")
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create checkboxes for categories
        categories = [
            "Personal Information (Names, IDs)",
            "Contact Information (Emails, Phone)",
            "Financial Information (Credit Cards, Account Numbers)",
            "Addresses and Locations",
            "Custom Patterns"
        ]
        
        self.category_vars = {}
        for category in categories:
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            ttk.Checkbutton(
                category_frame,
                text=category,
                variable=var
            ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Save button
        save_btn = ttk.Button(
            parent,
            text="Save Settings",
            command=self.save_settings
        )
        save_btn.pack(anchor=tk.CENTER, pady=10)
    
    def browse_file(self):
        """Open file browser dialog"""
        filetypes = [
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)
    
    def analyze_text(self):
        """Analyze the text in the input area"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Please enter some text to analyze")
            return
        
        if not self.detector:
            messagebox.showerror("Error", "Detector not initialized")
            return
        
        # Update status
        self.status_var.set("Analyzing text...")
        self.root.update_idletasks()
        
        # Run detection in a separate thread
        threading.Thread(
            target=self._analyze_text_thread,
            args=(text,),
            daemon=True
        ).start()
    
    def _analyze_text_thread(self, text):
        """Thread function for text analysis"""
        try:
            result = self.detector.detect(text)
            self.queue.put(("analysis_result", result))
        except Exception as e:
            self.queue.put(("error", f"Error analyzing text: {str(e)}"))
    
    def analyze_file(self):
        """Analyze the selected file"""
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showinfo("Info", "Please select a valid file")
            return
        
        if not self.detector:
            messagebox.showerror("Error", "Detector not initialized")
            return
        
        # Update status
        self.status_var.set(f"Analyzing file: {os.path.basename(file_path)}...")
        self.root.update_idletasks()
        
        # Run file analysis in a separate thread
        threading.Thread(
            target=self._analyze_file_thread,
            args=(file_path,),
            daemon=True
        ).start()
    
    def _analyze_file_thread(self, file_path):
        """Thread function for file analysis"""
        try:
            # Clear existing results
            self.queue.put(("clear_file_results", None))
            
            # Read file line by line
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Analyze each line
            for i, line in enumerate(lines, 1):
                if line.strip():
                    result = self.detector.detect(line.strip())
                    if result.is_sensitive:
                        self.queue.put((
                            "file_result", 
                            (i, result.sensitive_type, result.sensitive_value, result.confidence)
                        ))
            
            self.queue.put(("status", f"Completed analysis of {os.path.basename(file_path)}"))
        except Exception as e:
            self.queue.put(("error", f"Error analyzing file: {str(e)}"))
    
    def encrypt_sensitive(self):
        """Encrypt sensitive data in the input text"""
        # This would connect to your encryption module
        messagebox.showinfo(
            "Encryption", 
            "Encryption feature will be integrated with your encryption module"
        )
    
    def encrypt_file(self):
        """Encrypt sensitive data in the selected file"""
        # This would connect to your encryption module
        messagebox.showinfo(
            "File Encryption", 
            "File encryption feature will be integrated with your encryption module"
        )
    
    def save_settings(self):
        """Save the current settings"""
        # Here you would save settings to a config file
        threshold = self.threshold_var.get()
        categories = {k: v.get() for k, v in self.category_vars.items()}
        
        messagebox.showinfo(
            "Settings Saved",
            f"Threshold: {threshold:.2f}\nCategories: {sum(categories.values())}/{len(categories)}"
        )
    
    def check_queue(self):
        """Check the queue for messages from worker threads"""
        try:
            while True:
                message_type, data = self.queue.get_nowait()
                
                if message_type == "status":
                    self.status_var.set(data)
                
                elif message_type == "error":
                    self.status_var.set("Error occurred")
                    messagebox.showerror("Error", data)
                
                elif message_type == "analysis_result":
                    self.display_analysis_result(data)
                
                elif message_type == "clear_file_results":
                    # Clear all items from the treeview
                    for item in self.file_results_tree.get_children():
                        self.file_results_tree.delete(item)
                
                elif message_type == "file_result":
                    # Add result to the treeview
                    line_num, sensitive_type, sensitive_value, confidence = data
                    
                    # Ensure confidence is between 0-1
                    confidence = min(max(float(confidence), 0.0), 1.0)
                    
                    self.file_results_tree.insert(
                        "", 
                        tk.END, 
                        values=(
                            line_num,
                            sensitive_type or "Unknown",
                            sensitive_value or "N/A",
                            f"{confidence:.2%}"
                        )
                    )
                
                self.queue.task_done()
                
        except queue.Empty:
            # No more messages, schedule next check
            self.root.after(100, self.check_queue)
    
    def display_analysis_result(self, result):
        """Display the analysis result in the results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Format result display
        if result.is_sensitive:
            self.results_text.insert(tk.END, "⚠️ SENSITIVE DATA DETECTED ⚠️\n\n", "heading")
            
            # FIX: Ensure confidence is between 0-100%
            confidence = min(max(float(result.confidence), 0.0), 1.0)
            self.results_text.insert(tk.END, f"Confidence: {confidence:.2%}\n\n")
            
            if result.sensitive_type:
                self.results_text.insert(tk.END, f"Type: {result.sensitive_type}\n")
            
            if result.sensitive_value:
                self.results_text.insert(tk.END, f"Value: {result.sensitive_value}\n\n")
            
            # Display entities
            if result.entities:
                self.results_text.insert(tk.END, "Detected Entities:\n")
                for entity in result.entities:
                    self.results_text.insert(
                        tk.END, 
                        f"- {entity['text']} ({entity['label']})\n"
                    )
        else:
            self.results_text.insert(tk.END, "✓ No sensitive data detected\n\n")
            
            # FIX: Ensure confidence is between 0-100%
            confidence = min(max(float(1 - result.confidence), 0.0), 1.0)
            self.results_text.insert(tk.END, f"Confidence: {confidence:.2%}\n\n")
            
            # Still show entities if any
            if result.entities:
                self.results_text.insert(tk.END, "Detected Entities (Non-sensitive):\n")
                for entity in result.entities:
                    self.results_text.insert(
                        tk.END, 
                        f"- {entity['text']} ({entity['label']})\n"
                    )
        
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Analysis complete")


def main():
    root = tk.Tk()
    
    # Add a special startup frame that shows while checking dependencies
    startup_frame = ttk.Frame(root, padding="20")
    startup_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(
        startup_frame, 
        text="Sensitive Data Detection System", 
        font=("Arial", 16, "bold")
    ).pack(pady=(0, 20))
    
    ttk.Label(
        startup_frame,
        text="Initializing application and checking dependencies...",
        font=("Arial", 10)
    ).pack(pady=10)
    
    progress = ttk.Progressbar(startup_frame, mode="indeterminate")
    progress.pack(fill=tk.X, padx=50, pady=10)
    progress.start()
    
    def check_deps_and_start():
        # Hide the startup frame
        startup_frame.pack_forget()
        
        # Check if we have all dependencies installed
        if not detector_import_success:
            if check_and_install_dependencies():
                # If dependencies are good but we still had an import error,
                # show a message about restarting
                messagebox.showinfo(
                    "Restart Required",
                    "Dependencies are installed but you need to restart the application."
                )
                root.destroy()
                return
        
        # Start the main application
        app = SensitiveDataGUI(root)
    
    # Schedule the dependency check
    root.after(500, check_deps_and_start)
    
    root.mainloop()

if __name__ == "__main__":
    main()