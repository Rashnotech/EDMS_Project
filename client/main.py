# client/main.py
import sys
import time
from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont, QColor, QPainter, QBrush, QPen
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


class EDMSApp:
    """
    Main controller for the entire EDMS desktop application.
    Handles window switching and user session data.
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')  # Modern cross-platform style
        # Keep default palette but apply only if explicitly desired
        try:
            self.set_app_palette()
        except Exception:
            pass
        
        self.current_user = None
        self.login_window = None
        self.main_window = None
        
        # Show splash screen
        self.show_splash_screen()

    def set_app_palette(self):
        """Set modern color scheme for the application"""
        from PySide6.QtGui import QPalette
        
        palette = QPalette()
        # Modern blue-gray theme
        palette.setColor(QPalette.Window, QColor(240, 240, 245))
        palette.setColor(QPalette.WindowText, QColor(33, 33, 33))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 250))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(33, 33, 33))
        palette.setColor(QPalette.Text, QColor(33, 33, 33))
        palette.setColor(QPalette.Button, QColor(255, 255, 255))
        palette.setColor(QPalette.ButtonText, QColor(33, 33, 33))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        self.app.setPalette(palette)

    def show_splash_screen(self):
        """Display a cleaner, shorter splash screen while app initializes"""
        w, h = 560, 300
        splash_pix = QPixmap(w, h)
        splash_pix.fill(Qt.transparent)

        painter = QPainter(splash_pix)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw rounded background
        rect_brush = QBrush(QColor(42, 130, 218))
        painter.setBrush(rect_brush)
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(0, 0, w, h, 12, 12)

        # Draw centered title
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Segoe UI", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(splash_pix.rect(), Qt.AlignCenter, "Electronic\nDocument Management System")
        painter.end()

        self.splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pix.mask())
        self.splash.show()
        self.app.processEvents()

        # Shorter, non-blocking splash
        QTimer.singleShot(900, self.initialize_app)

    def initialize_app(self):
        """Initialize application components after splash screen"""
        self.splash.showMessage(
            "Electronic Document Management System\n\nLoading components...\n\n Powered by Rashnotech Solutions",
            Qt.AlignCenter | Qt.AlignBottom,
            QColor(255, 255, 255)
        )
        self.app.processEvents()
        
        # Initialize login window
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.launch_main_window)
        
        # Close splash and show login
        QTimer.singleShot(1000, self.show_login)

    def show_login(self):
        """Show login window and close splash"""
        self.splash.finish(self.login_window)
        self.login_window.show()

    def launch_main_window(self, user_data: dict):
        """Open the main dashboard after successful login."""
        self.current_user = user_data
        self.login_window.close()

        self.main_window = MainWindow(user=self.current_user)
        self.main_window.logout_signal.connect(self.handle_logout)
        self.main_window.show()

    def handle_logout(self):
        """Handle logout and return to login screen"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        
        self.current_user = None
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.launch_main_window)
        self.login_window.show()

    def run(self):
        """Start the EDMS application."""
        try:
            sys.exit(self.app.exec())
        except Exception as e:
            QMessageBox.critical(None, "Fatal Error", f"Unexpected Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    app = EDMSApp()
    app.run()