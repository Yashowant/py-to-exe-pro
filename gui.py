import os
import queue
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

from validator import Validator
from builder import PyInstallerBuilder
from config import ConfigManager

class PyToExeApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Py to EXE Compiler - Pro")
        self.geometry("900x700")
        
        self.log_queue = queue.Queue()
        self.builder = None
        self.build_in_progress = False

        self._init_vars()
        self._build_ui()
        self._check_environment()

    def _init_vars(self):
        # Path Variables
        self.main_file_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.icon_path_var = tk.StringVar()
        
        # Options Variables
        self.one_file_var = tk.BooleanVar(value=True)
        self.windowed_var = tk.BooleanVar(value=False)
        self.uac_admin_var = tk.BooleanVar(value=False)
        self.upx_var = tk.BooleanVar(value=False)
        self.clean_temp_var = tk.BooleanVar(value=True)
        
        # Metadata Variables
        self.app_name_var = tk.StringVar(value="MyApp")
        self.developer_var = tk.StringVar()
        self.version_var = tk.StringVar(value="1.0.0.0")
        self.company_var = tk.StringVar()
        self.copyright_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.hidden_imports_var = tk.StringVar()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.tab_main = ttk.Frame(notebook)
        self.tab_meta = ttk.Frame(notebook)
        self.tab_logs = ttk.Frame(notebook)

        notebook.add(self.tab_main, text="Configuration")
        notebook.add(self.tab_meta, text="Metadata & Advanced")
        notebook.add(self.tab_logs, text="Build Logs")

        self._build_main_tab()
        self._build_meta_tab()
        self._build_logs_tab()

        # Bottom Action Bar
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=X, padx=10, pady=10)
        
        self.btn_save_profile = ttk.Button(action_frame, text="Save Profile", command=self.save_profile, bootstyle=SECONDARY)
        self.btn_save_profile.pack(side=LEFT, padx=5)

        self.btn_build = ttk.Button(action_frame, text="🚀 BUILD EXE", command=self.start_build, bootstyle=SUCCESS)
        self.btn_build.pack(side=RIGHT, padx=5)
        
        self.progress_bar = ttk.Progressbar(action_frame, mode='indeterminate', bootstyle=SUCCESS)

    # ALL METHODS BELOW MUST BE INDENTED TO BE PART OF THE CLASS
    def _build_main_tab(self):
        frame = ttk.LabelFrame(self.tab_main, text="Paths & Core Options")
        frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

        # File Selection
        ttk.Label(frame, text="Main Script (.py):").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.main_file_var, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse File", command=lambda: self._browse_file(self.main_file_var, [("Python Files", "*.py")])).grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.output_dir_var, width=60).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="Browse Folder", command=lambda: self._browse_dir(self.output_dir_var)).grid(row=1, column=2, padx=5)

        ttk.Label(frame, text="Custom Icon (.ico):").grid(row=2, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.icon_path_var, width=60).grid(row=2, column=1, padx=5)
        ttk.Button(frame, text="Browse Icon", command=lambda: self._browse_file(self.icon_path_var, [("Icon Files", "*.ico")])).grid(row=2, column=2, padx=5)

        # Checkboxes
        opts_frame = ttk.Frame(frame)
        opts_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky=W)
        
        ttk.Checkbutton(opts_frame, text="One File (--onefile)", variable=self.one_file_var, bootstyle="round-toggle").pack(side=LEFT, padx=15)
        ttk.Checkbutton(opts_frame, text="Hide Console (--windowed)", variable=self.windowed_var, bootstyle="round-toggle").pack(side=LEFT, padx=15)
        ttk.Checkbutton(opts_frame, text="Request Admin (--uac-admin)", variable=self.uac_admin_var, bootstyle="round-toggle").pack(side=LEFT, padx=15)
        ttk.Checkbutton(opts_frame, text="Clean Temp Files", variable=self.clean_temp_var, bootstyle="round-toggle").pack(side=LEFT, padx=15)

    def _build_meta_tab(self):
        frame = ttk.LabelFrame(self.tab_meta, text="Application Information")
        frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

        fields = [
            ("App Name:", self.app_name_var),
            ("Version:", self.version_var),
            ("Company Name:", self.company_var),
            ("Description:", self.description_var),
            ("Copyright:", self.copyright_var),
            ("Hidden Imports (comma separated):", self.hidden_imports_var)
        ]

        for i, (label, var) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=W, pady=5, padx=5)
            ttk.Entry(frame, textvariable=var, width=50).grid(row=i, column=1, pady=5, padx=5)

    def _build_logs_tab(self):
        self.log_area = ScrolledText(self.tab_logs, wrap=tk.WORD, state=DISABLED, font=("Consolas", 10))
        self.log_area.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # --- Actions & Logic ---

    def _browse_file(self, var, filetypes):
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path: var.set(path)

    def _browse_dir(self, var):
        path = filedialog.askdirectory()
        if path: var.set(path)

    def _check_environment(self):
        if not Validator.check_pyinstaller():
            messagebox.showwarning("Warning", "PyInstaller is not detected in your PATH. Please install it (`pip install pyinstaller`).")

    def _write_log(self, text):
        self.log_area.text.config(state=NORMAL)
        self.log_area.text.insert(tk.END, text + "\n")
        self.log_area.text.see(tk.END)
        self.log_area.text.config(state=DISABLED)

    def save_profile(self):
        config = self._gather_config()
        if ConfigManager.save_profile("default_profile", config):
            messagebox.showinfo("Success", "Profile saved successfully!")

    def _gather_config(self):
        return {
            "main_file": self.main_file_var.get(),
            "output_dir": self.output_dir_var.get(),
            "icon": self.icon_path_var.get(),
            "one_file": self.one_file_var.get(),
            "windowed": self.windowed_var.get(),
            "uac_admin": self.uac_admin_var.get(),
            "clean_temp": self.clean_temp_var.get(),
            "app_name": self.app_name_var.get(),
            "version": self.version_var.get(),
            "company": self.company_var.get(),
            "description": self.description_var.get(),
            "copyright": self.copyright_var.get(),
            "hidden_imports": self.hidden_imports_var.get()
        }

    def start_build(self):
        if self.build_in_progress:
            return
        
        config = self._gather_config()
        if not Validator.validate_py_file(config["main_file"]):
            messagebox.showerror("Error", "Invalid Main Python File selected.")
            return
        
        self.build_in_progress = True
        self.btn_build.config(state=DISABLED)
        self.progress_bar.pack(side=RIGHT, padx=10)
        self.progress_bar.start(10)
        
        # Corrected indentation and .text usage here
        self.log_area.text.config(state=NORMAL)
        self.log_area.text.delete('1.0', tk.END)
        self.log_area.text.config(state=DISABLED)

        self.children['!notebook'].select(self.tab_logs)
        self.builder = PyInstallerBuilder(config, self.log_queue)
        self.builder.build()
        self.after(100, self._poll_logs)

    def _poll_logs(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                if msg == "PROCESS_COMPLETE":
                    self._finish_build()
                    return
                self._write_log(msg)
        except queue.Empty:
            pass
        self.after(100, self._poll_logs)

    def _finish_build(self):
        self.build_in_progress = False
        self.btn_build.config(state=NORMAL)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        target_exe = os.path.join(self.output_dir_var.get(), f"{self.app_name_var.get()}.exe")
        if os.path.exists(target_exe):
            if messagebox.askyesno("Shortcut", "Build complete! Create a desktop shortcut?"):
                PyInstallerBuilder.create_shortcut(target_exe, self.app_name_var.get(), self.icon_path_var.get())
            if messagebox.askyesno("Open Folder", "Open the output directory?"):
                os.startfile(self.output_dir_var.get())