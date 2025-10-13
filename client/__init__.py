#!/usr/bin/python3
"""
UI Package for EDMS Application
Contains all user interface components
"""

from .login_window import LoginWindow
from .main_window import MainWindow
from .uploader import UploadDialog
from .user_admin import UserAdminWindow, UserDialog

__all__ = [
    'LoginWindow',
    'MainWindow',
    'UploadDialog',
    'UserAdminWindow',
    'UserDialog'
]

__version__ = '1.0.0'