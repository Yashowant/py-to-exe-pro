import os
import subprocess
import logging

class Validator:
    """Validates user inputs and environment state."""
    
    @staticmethod
    def validate_py_file(path: str) -> bool:
        """Checks if the path is a valid Python file."""
        return os.path.isfile(path) and path.lower().endswith('.py')

    @staticmethod
    def validate_folder(path: str) -> bool:
        """Checks if the path is a valid directory."""
        return os.path.isdir(path)

    @staticmethod
    def validate_ico_file(path: str) -> bool:
        """Checks if the path is a valid .ico file."""
        if not path: 
            return True  # Icon is optional
        return os.path.isfile(path) and path.lower().endswith('.ico')

    @staticmethod
    def check_pyinstaller() -> bool:
        """Checks if PyInstaller is available in the system PATH."""
        try:
            subprocess.run(["pyinstaller", "--version"], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE, 
                           check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.error("PyInstaller not found in environment.")
            return False