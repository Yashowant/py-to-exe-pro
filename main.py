import logging
from gui import PyToExeApp

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app_builder.log"), logging.StreamHandler()]
    )

if __name__ == "__main__":
    setup_logging()
    app = PyToExeApp()
    app.mainloop()