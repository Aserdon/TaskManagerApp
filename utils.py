import os
import sys

def get_base_path():
    """Return the base path of the application, accounting for PyInstaller's frozen state."""
    return sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
