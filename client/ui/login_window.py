#!/usr/bin/python3
"""Enhanced login window with modern design (desktop-friendly)"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont


class LoginWindow(QWidget):
    login_success = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDMS Login")
        # Desktop-friendly minimum size
        self.setMinimumSize(520, 560)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self._shake_animation = None
        # Track whether we've already switched to fullscreen to avoid toggling repeatedly
        self._fullscreen_done = False

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Build the modern login form layout for desktop screens."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(48, 32, 48, 32)
        main_layout.setSpacing(18)
        # Anchor content toward the top so the form doesn't get squashed when window is short
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header section with logo/icon area
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # App icon/logo placeholder
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFont(QFont("Arial", 44))
        header_layout.addWidget(icon_label)

        title = QLabel("EDMS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)

        subtitle = QLabel("Electronic Document Management System")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitleLabel")
        header_layout.addWidget(subtitle)

        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)

        main_layout.addSpacing(16)

        # Login form card
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_frame.setMaximumWidth(460)  # limit width so fields don't stretch too wide on desktop
        form_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(22, 18, 22, 18)
        form_layout.setSpacing(12)

        # Username and password fields
        username_label = QLabel("Username")
        username_label.setObjectName("fieldLabel")
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setObjectName("inputField")
        self.username_input.setMinimumHeight(44)
        self.username_input.setMinimumWidth(320)
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setObjectName("inputField")
        self.password_input.setMinimumHeight(44)
        self.password_input.setMinimumWidth(320)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.password_input.returnPressed.connect(self.attempt_login)

        # Add widgets in order with explicit spacing so they won't overlap
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(6)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        form_layout.addSpacing(12)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("loginButton")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.attempt_login)
        self.login_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_btn.setMinimumWidth(160)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.setMinimumHeight(48)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cancel_btn.setMinimumWidth(160)

        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(cancel_btn)
        form_layout.addLayout(btn_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        self.status_label.setMinimumHeight(20)
        form_layout.addWidget(self.status_label)

        form_frame.setLayout(form_layout)

        # Center the form_frame horizontally
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_frame)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)

        # Info text at bottom
        info_label = QLabel("Default credentials:\nAdmin: admin/1234 | Staff: staff/1234")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setObjectName("infoLabel")
        main_layout.addWidget(info_label)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def showEvent(self, event):
        """Make the login window fullscreen on first show (desktop default)."""
        super().showEvent(event)
        if not getattr(self, "_fullscreen_done", False):
            # Use showMaximized instead of showFullScreen to keep window decorations if preferred
            self.showMaximized()
            self._fullscreen_done = True

    def apply_styles(self):
        """Apply modern CSS styles"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            #headerFrame {
                background-color: transparent;
            }

            #titleLabel {
                font-size: 32px;
                font-weight: bold;
                color: #2a82da;
                margin: 10px 0;
            }

            #subtitleLabel {
                font-size: 13px;
                color: #666;
                margin-bottom: 10px;
            }

            #formFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }

            #fieldLabel {
                font-size: 13px;
                font-weight: 600;
                color: #333;
                margin-bottom: 5px;
            }

            #inputField {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #fafafa;
                color: #333;
            }

            #inputField:focus {
                border: 2px solid #2a82da;
                background-color: white;
            }

            #loginButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px;
            }

            #loginButton:hover {
                background-color: #1e6bb8;
            }

            #loginButton:pressed {
                background-color: #165a9a;
            }

            #cancelButton {
                background-color: #f5f5f5;
                color: #666;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px;
            }

            #cancelButton:hover {
                background-color: #e8e8e8;
                border: 2px solid #d0d0d0;
            }

            #statusLabel {
                color: #666;
                font-style: italic;
                font-size: 13px;
                margin-top: 10px;
            }

            #infoLabel {
                font-size: 11px;
                color: #999;
                line-height: 1.5;
            }
        """)

    def attempt_login(self):
        """Handle login logic and emit signal on success."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("Please enter both username and password.")
            return

        # Simulated credentials
        if username == "admin" and password == "1234":
            user_data = {"username": username, "role": "admin"}
            self.status_label.setText("Login successful")
            self.status_label.setStyleSheet("color: #28a745; font-weight: 600;")
            self.login_success.emit(user_data)

        elif username == "staff" and password == "1234":
            user_data = {"username": username, "role": "staff"}
            self.status_label.setText("Login successful")
            self.status_label.setStyleSheet("color: #28a745; font-weight: 600;")
            self.login_success.emit(user_data)

        else:
            self.show_error("Invalid username or password.")

    def show_error(self, message):
        """Display error message with animation"""
        self.status_label.setText(f"{message}")
        self.status_label.setStyleSheet("color: #dc3545; font-weight: 600;")

        # Shake animation
        self.shake_window()

    def shake_window(self):
        """Animate window shake on error"""
        # Horizontal shake of the window without extreme jumps
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(300)
        animation.setLoopCount(1)
        animation.setEasingCurve(QEasingCurve.OutBounce)

        start = self.pos()
        offset = 10
        key1 = QPoint(start.x() - offset, start.y())
        key2 = QPoint(start.x() + offset, start.y())

        animation.setKeyValueAt(0.0, start)
        animation.setKeyValueAt(0.25, key1)
        animation.setKeyValueAt(0.5, key2)
        animation.setKeyValueAt(0.75, key1)
        animation.setKeyValueAt(1.0, start)

        # keep a reference so it doesn't get garbage-collected
        self._shake_animation = animation
        animation.start()