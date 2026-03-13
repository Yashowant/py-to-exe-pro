import os
import subprocess
import threading
import queue
import shutil
import logging
from pathlib import Path

# Try importing win32com for shortcut creation
try:
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    logging.warning("pywin32 not installed. Shortcut creation disabled.")

class PyInstallerBuilder:
    """Handles the PyInstaller build process via subprocess."""
    
    def __init__(self, config: dict, log_queue: queue.Queue):
        self.config = config
        self.log_queue = log_queue
        self.process = None
        self.output_dir = self.config.get("output_dir", "dist")

    def log(self, message: str):
        self.log_queue.put(message)

    def generate_version_file(self) -> str:
        """Generates a PyInstaller version info file for Windows metadata."""
        version = self.config.get("version", "1.0.0.0")
        # Ensure version is x.x.x.x format
        v_parts = (version.split('.') + ['0', '0', '0', '0'])[:4]
        v_tuple = ",".join(v_parts)
        
        template = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({v_tuple}),
    prodvers=({v_tuple}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', '{self.config.get("company", "")}'),
        StringStruct('FileDescription', '{self.config.get("description", "")}'),
        StringStruct('FileVersion', '{version}'),
        StringStruct('LegalCopyright', '{self.config.get("copyright", "")}'),
        StringStruct('OriginalFilename', '{self.config.get("app_name", "app")}.exe'),
        StringStruct('ProductName', '{self.config.get("app_name", "app")}'),
        StringStruct('ProductVersion', '{version}')])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
        version_file_path = os.path.join(os.getcwd(), "version_info.txt")
        with open(version_file_path, "w") as f:
            f.write(template)
        return version_file_path

    def build(self):
        """Builds the executable in a separate thread."""
        thread = threading.Thread(target=self._run_build, daemon=True)
        thread.start()

    def _run_build(self):
        try:
            main_file = self.config.get("main_file")
            cmd = ["pyinstaller", "--noconfirm"]

            if self.config.get("one_file"): cmd.append("--onefile")
            else: cmd.append("--onedir")
            
            if self.config.get("windowed"): cmd.append("--windowed")
            
            if self.config.get("icon"): 
                cmd.extend(["--icon", self.config.get("icon")])
                
            if self.config.get("uac_admin"): 
                cmd.append("--uac-admin")
                
            if self.config.get("upx"): 
                cmd.append("--upx-dir=upx") # Assumes UPX is in PATH or upx/ folder

            if self.config.get("app_name"):
                cmd.extend(["--name", self.config.get("app_name")])
                
            out_dir = self.config.get("output_dir")
            if out_dir:
                cmd.extend(["--distpath", out_dir])

            # Metadata
            if any([self.config.get("company"), self.config.get("version")]):
                vf = self.generate_version_file()
                cmd.extend(["--version-file", vf])

            # Hidden Imports
            hidden_imports = self.config.get("hidden_imports", "")
            if hidden_imports:
                for imp in hidden_imports.split(","):
                    cmd.extend(["--hidden-import", imp.strip()])

            cmd.append(main_file)

            self.log(f"Executing: {' '.join(cmd)}")
            
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            )

            for line in self.process.stdout:
                self.log(line.strip())

            self.process.wait()
            
            if self.process.returncode == 0:
                self.log("✅ BUILD SUCCESSFUL!")
                self._post_build_cleanup()
            else:
                self.log("❌ BUILD FAILED. Check logs above.")

        except Exception as e:
            self.log(f"❌ Error during build: {str(e)}")
        finally:
            self.log("PROCESS_COMPLETE")

    def _post_build_cleanup(self):
        """Cleans up temp .spec files and build folders."""
        if self.config.get("clean_temp", True):
            self.log("Cleaning temporary files...")
            spec_file = f"{self.config.get('app_name', Path(self.config['main_file']).stem)}.spec"
            if os.path.exists(spec_file): os.remove(spec_file)
            if os.path.exists("build"): shutil.rmtree("build")
            if os.path.exists("version_info.txt"): os.remove("version_info.txt")

    @staticmethod
    def create_shortcut(target_exe: str, app_name: str, icon_path: str = None):
        """Creates a desktop shortcut using win32com."""
        if not WIN32_AVAILABLE:
            return False
        try:
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            path = os.path.join(desktop, f"{app_name}.lnk")
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target_exe
            shortcut.WorkingDirectory = os.path.dirname(target_exe)
            if icon_path and os.path.exists(icon_path):
                shortcut.IconLocation = icon_path
            shortcut.save()
            return True
        except Exception as e:
            logging.error(f"Failed to create shortcut: {e}")
            return False