#!/usr/bin/python3
"""Enhanced upload dialog with modern design"""
import sys
import requests
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QComboBox, QMessageBox, QProgressBar, QFrame,
    QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon


class UploadWorker(QThread):
    """Background worker for file upload"""
    progress = Signal(int)
    finished = Signal(bool, str)
    
    def __init__(self, file_path, year, api_url):
        super().__init__()
        self.file_path = file_path
        self.year = year
        self.api_url = api_url
    
    def run(self):
        try:
            self.progress.emit(10)
            with open(self.file_path, "rb") as f:
                files = {"file": (Path(self.file_path).name, f)}
                data = {"year": self.year}
                
                self.progress.emit(30)
                response = requests.post(self.api_url, files=files, data=data, timeout=30)
                self.progress.emit(80)
                
                if response.status_code == 200:
                    self.progress.emit(100)
                    self.finished.emit(True, "Upload successful!")
                else:
                    self.finished.emit(False, f"Server error: {response.status_code}")
                    
        except requests.ConnectionError:
            self.finished.emit(False, "Cannot connect to server")
        except Exception as e:
            self.finished.emit(False, str(e))


class UploadDialog(QDialog):
    def __init__(self, api_url="http://127.0.0.1:8000/api/upload", parent=None):
        super().__init__(parent)
        self.api_url = api_url
        self.setWindowTitle("Upload Workbook")
        # allow the dialog to resize so nothing is clipped on smaller screens or
        # when the user has larger fonts / scaling
        self.setMinimumSize(520, 420)
        self.setModal(True)
        try:
            # show a size grip on platforms that support it
            self.setSizeGripEnabled(True)
        except Exception:
            pass

        self.file_path = None
        self.upload_worker = None
        self._init_ui()
        self.apply_styles()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header (compact)
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout()

        title = QLabel("Upload Excel Workbook")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialogTitle")
        header_layout.addWidget(title)

        subtitle = QLabel("Select an Excel file to import into the system")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("dialogSubtitle")
        header_layout.addWidget(subtitle)

        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

        # File selection card
        file_card = QFrame()
        file_card.setObjectName("fileCard")
        file_layout = QVBoxLayout()
        file_layout.setContentsMargins(20, 20, 20, 20)

        file_label = QLabel("Selected File:")
        file_label.setObjectName("fieldLabel")
        file_layout.addWidget(file_label)

        self.file_display = QLabel("No file selected")
        self.file_display.setObjectName("fileDisplay")
        self.file_display.setWordWrap(True)
        # allow the file display to stretch horizontally so long file names are visible
        self.file_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        file_layout.addWidget(self.file_display)

        browse_btn = QPushButton("Browse Files")
        browse_btn.setObjectName("browseButton")
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self.select_file)
        file_layout.addWidget(browse_btn)

        file_card.setLayout(file_layout)
        layout.addWidget(file_card)

        # Year selection
        year_layout = QVBoxLayout()
        year_layout.setSpacing(8)

        year_label = QLabel("Target Year:")
        year_label.setObjectName("fieldLabel")
        year_layout.addWidget(year_label)

        self.year_combo = QComboBox()
        self.year_combo.setObjectName("yearCombo")
        self.year_combo.addItems(["2023", "2024", "2025", "2026", "2027"])
        self.year_combo.setCurrentText("2025")
        # make the combo expand so it doesn't get cropped on high-DPI/fullscreen
        self.year_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        year_layout.addWidget(self.year_combo)

        layout.addLayout(year_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        # allow progress bar to expand horizontally
        self.progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.progress)

        # Status label
        self.status_label = QLabel("Ready to upload")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.upload_btn = QPushButton("Upload")
        self.upload_btn.setObjectName("uploadButton")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setMinimumHeight(45)
        self.upload_btn.clicked.connect(self.upload_file)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setMinimumHeight(45)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.upload_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def showEvent(self, event):
        """On first show, enter full-screen to ensure no controls are clipped.

        We only do this once; subsequent opens will respect the previous window state.
        """
        # If already maximized/fullscreen, do nothing
        try:
            if not self.isFullScreen() and not self.isMaximized():
                # Try full screen first, fall back to maximize for desktop friendliness
                try:
                    self.showFullScreen()
                except Exception:
                    self.showMaximized()
        except Exception:
            pass
        # Allow normal event processing to continue
        super().showEvent(event)

    def apply_styles(self):
        """Apply modern stylesheet"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
            }
            
            #headerFrame {
                background-color: transparent;
            }
            
            #dialogTitle {
                font-size: 20px;
                font-weight: bold;
                color: #2a82da;
                margin: 10px 0;
            }
            
            #dialogSubtitle {
                font-size: 13px;
                color: #666;
            }
            
            #fileCard {
                background-color: white;
                border: 2px dashed #d0d0d0;
                border-radius: 10px;
            }
            
            #fieldLabel {
                font-size: 13px;
                font-weight: 600;
                color: #555;
                margin-bottom: 5px;
            }
            
            #fileDisplay {
                font-size: 14px;
                color: #2a82da;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                min-height: 40px;
            }
            
            #browseButton {
                background-color: #f5f5f5;
                color: #333;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
            }
            
            #browseButton:hover {
                background-color: #e8e8e8;
                border: 2px solid #2a82da;
            }
            
            #yearCombo {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            
            #yearCombo:focus {
                border: 2px solid #2a82da;
            }
            
            #progressBar {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #f0f0f0;
                text-align: center;
            }
            
            #progressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a82da, stop:1 #1e6bb8);
                border-radius: 5px;
            }
            
            #statusLabel {
                font-size: 13px;
                color: #666;
                font-style: italic;
            }
            
            #uploadButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
                font-weight: 600;
            }
            
            #uploadButton:hover {
                background-color: #1e6bb8;
            }
            
            #uploadButton:disabled {
                background-color: #ccc;
                color: #999;
            }
            
            #cancelButton {
                background-color: #f5f5f5;
                color: #666;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 15px;
                font-weight: 600;
            }
            
            #cancelButton:hover {
                background-color: #e8e8e8;
            }
        """)

    def select_file(self):
        """Open file dialog to select Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel Workbook", "",
            "Excel Files (*.xls *.xlsx);;All Files (*)"
        )
        if file_path:
            self.file_path = file_path
            file_name = Path(file_path).name
            file_size = Path(file_path).stat().st_size / 1024  # KB
            
            self.file_display.setText(f"📄 {file_name}\n({file_size:.1f} KB)")
            self.status_label.setText("✓ File ready to upload")
            self.status_label.setStyleSheet("color: #28a745; font-weight: 600;")
        else:
            self.status_label.setText("No file selected")
            self.status_label.setStyleSheet("color: #666;")

    def upload_file(self):
        """Handle file upload with background worker"""
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please select a file first.")
            return

        year = self.year_combo.currentText()
        
        # Disable UI during upload
        self.upload_btn.setEnabled(False)
        self.status_label.setText(f"Uploading to {year} records...")
        self.status_label.setStyleSheet("color: #2a82da; font-weight: 600;")
        self.progress.setValue(0)
        
        # Create and start worker
        self.upload_worker = UploadWorker(self.file_path, year, self.api_url)
        self.upload_worker.progress.connect(self.update_progress)
        self.upload_worker.finished.connect(self.upload_finished)
        self.upload_worker.start()

    def update_progress(self, value):
        """Update progress bar"""
        self.progress.setValue(value)

    def upload_finished(self, success, message):
        """Handle upload completion"""
        self.upload_btn.setEnabled(True)
        
        if success:
            self.progress.setValue(100)
            self.status_label.setText("✓ " + message)
            self.status_label.setStyleSheet("color: #28a745; font-weight: 600;")
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            self.progress.setValue(0)
            self.status_label.setText("✗ " + message)
            self.status_label.setStyleSheet("color: #dc3545; font-weight: 600;")
            QMessageBox.critical(self, "Upload Failed", message)