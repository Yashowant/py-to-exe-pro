# 🚀 Py-to-EXE Professional Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A production-ready, modular desktop application to convert Python scripts (`.py`) into standalone Windows executables (`.exe`). Built with **ttkbootstrap** for a modern UI and **PyInstaller** for robust backend compilation.

## ✨ Key Features
* **Modern GUI:** Clean dark-mode interface with a real-time progress bar.
* **Batch & Single Mode:** Convert isolated scripts or complex multi-file packages.
* **Professional Metadata:** Inject Version Info, Company Name, and Copyrights into the EXE details.
* **Asset Management:** Support for custom `.ico` icons and hidden imports.
* **Automation:** Automatic cleanup of temporary `.spec` files and `build/` directories.
* **Desktop Shortcut:** One-click option to create a Windows shortcut after a successful build.

## 🛠️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/py-to-exe-pro.git](https://github.com/YOUR_USERNAME/py-to-exe-pro.git)
    cd py-to-exe-pro
    ```

2.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the Application:**
    ```bash
    python main.py
    ```

## 📂 Project Structure
* `main.py` - Entry point of the application.
* `gui.py` - Modern UI layout and event handling.
* `builder.py` - Core logic for PyInstaller subprocess execution.
* `validator.py` - Path and file format validation logic.
* `config.py` - Save/Load build profiles in JSON format.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.