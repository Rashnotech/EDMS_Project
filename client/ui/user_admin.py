#!/usr/bin/python3
"""Enhanced user admin window with modern design"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog,
    QLabel, QLineEdit, QComboBox, QDialogButtonBox, QFrame, QHeaderView
)
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class UserAdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management - EDMS Admin")
        self.setWindowIcon(QIcon("client/assets/icon.png"))
        self.resize(1200, 700)

        self.users = []
        self._init_ui()
        self.apply_styles()
        self.load_users()

    def _init_ui(self):
        """Build the user management interface"""
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header = QFrame()
        header.setObjectName("headerFrame")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 15, 15, 15)
        
        title_layout = QVBoxLayout()
        title = QLabel("👥 User Management")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Manage system users and permissions")
        subtitle.setObjectName("pageSubtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # Stats
        stats_label = QLabel(f"Total Users: {len(self.users)}")
        stats_label.setObjectName("statsLabel")
        header_layout.addWidget(stats_label)
        
        header.setLayout(header_layout)
        main_layout.addWidget(header)

        # Action buttons
        btn_frame = QFrame()
        btn_frame.setObjectName("buttonFrame")
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout.setSpacing(10)
        
        add_btn = QPushButton("➕ Add User")
        add_btn.setObjectName("actionButton")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_user)
        
        edit_btn = QPushButton("✏️ Edit User")
        edit_btn.setObjectName("actionButton")
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_user)
        
        delete_btn = QPushButton("🗑️ Delete User")
        delete_btn.setObjectName("deleteButton")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_user)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_users)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        
        btn_frame.setLayout(btn_layout)
        main_layout.addWidget(btn_frame)

        # User table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["User ID", "Username", "Role", "Status"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setObjectName("userTable")
        main_layout.addWidget(self.table)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def apply_styles(self):
        """Apply modern stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            
            #headerFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            
            #pageTitle {
                font-size: 22px;
                font-weight: bold;
                color: #2a82da;
            }
            
            #pageSubtitle {
                font-size: 13px;
                color: #666;
                margin-top: 5px;
            }
            
            #statsLabel {
                font-size: 14px;
                font-weight: 600;
                color: #666;
                padding: 8px 15px;
                background-color: #f0f0f5;
                border-radius: 6px;
            }
            
            #buttonFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            
            #actionButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            
            #actionButton:hover {
                background-color: #1e6bb8;
            }
            
            #deleteButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            
            #deleteButton:hover {
                background-color: #c82333;
            }
            
            #refreshButton {
                background-color: #f5f5f5;
                color: #666;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            
            #refreshButton:hover {
                background-color: #e8e8e8;
                border: 2px solid #2a82da;
            }
            
            #userTable {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            
            #userTable::item {
                padding: 12px;
            }
            
            #userTable::item:selected {
                background-color: #e3f2fd;
                color: #1e6bb8;
            }
            
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 600;
                color: #333;
                font-size: 13px;
            }
        """)

    def load_users(self):
        """Fetch users from the backend (currently simulated data)."""
        self.users = [
            {"id": 1, "username": "admin", "role": "admin", "status": "Active"},
            {"id": 2, "username": "account_officer", "role": "staff", "status": "Active"},
            {"id": 3, "username": "audit_user", "role": "staff", "status": "Active"},
            {"id": 4, "username": "environmental_user", "role": "staff", "status": "Active"},
            {"id": 5, "username": "health_officer", "role": "staff", "status": "Inactive"},
            {"id": 6, "username": "education_admin", "role": "staff", "status": "Active"},
        ]
        self.populate_table()

    def populate_table(self):
        """Populate the table with user data"""
        self.table.setRowCount(0)
        for user in self.users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(user["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)
            
            # Username
            username_item = QTableWidgetItem(user["username"])
            self.table.setItem(row, 1, username_item)
            
            # Role
            role_item = QTableWidgetItem(user["role"].title())
            role_item.setTextAlignment(Qt.AlignCenter)
            if user["role"] == "admin":
                role_item.setForeground(Qt.darkBlue)
            self.table.setItem(row, 2, role_item)
            
            # Status
            status_item = QTableWidgetItem(user["status"])
            status_item.setTextAlignment(Qt.AlignCenter)
            if user["status"] == "Active":
                status_item.setForeground(Qt.darkGreen)
            else:
                status_item.setForeground(Qt.darkRed)
            self.table.setItem(row, 3, status_item)

    def add_user(self):
        """Open dialog to add new user"""
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["username"] or not data["password"]:
                QMessageBox.warning(self, "Invalid Input", "Username and password are required.")
                return
            
            new_id = max([u["id"] for u in self.users], default=0) + 1
            self.users.append({
                "id": new_id,
                "username": data["username"],
                "role": data["role"],
                "status": "Active"
            })
            self.populate_table()
            QMessageBox.information(
                self, "Success",
                f"✓ User '{data['username']}' added successfully!"
            )

    def edit_user(self):
        """Open dialog to edit selected user"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a user to edit.")
            return

        user = self.users[row]
        dialog = UserDialog(self, user)
        if dialog.exec() == QDialog.Accepted:
            updated = dialog.get_data()
            if not updated["username"]:
                QMessageBox.warning(self, "Invalid Input", "Username is required.")
                return
                
            self.users[row]["username"] = updated["username"]
            self.users[row]["role"] = updated["role"]
            if updated["password"]:  # Only update password if provided
                pass  # In real app, hash and store password
            
            self.populate_table()
            QMessageBox.information(
                self, "Updated",
                f"✓ User '{updated['username']}' updated successfully!"
            )

    def delete_user(self):
        """Delete selected user"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a user to delete.")
            return

        user = self.users[row]
        
        # Prevent deleting admin user
        if user["username"] == "admin":
            QMessageBox.warning(
                self, "Cannot Delete",
                "The default admin user cannot be deleted."
            )
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete user '{user['username']}'?\n\n"
            "This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            username = self.users[row]["username"]
            del self.users[row]
            self.populate_table()
            QMessageBox.information(
                self, "Deleted",
                f"✓ User '{username}' deleted successfully!"
            )


class UserDialog(QDialog):
    """Dialog for adding/editing users"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.setWindowTitle("User Details")
        # Allow the dialog to resize so fields are not clipped on different DPI/scaling
        self.setMinimumSize(480, 420)
        self.setModal(True)
        try:
            self.setSizeGripEnabled(True)
        except Exception:
            pass
        self.user_data = user_data
        self._init_ui()
        self.apply_styles()

    def _init_ui(self):
        layout = QVBoxLayout()
        # slightly reduced margins so the form fits comfortably
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Header (compact)
        header_layout = QVBoxLayout()
        # smaller icon to keep header compact and avoid pushing the form off-screen
        icon = QLabel("👤" if not self.user_data else "✏️")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 28px;")
        header_layout.addWidget(icon)

        title = QLabel("Add New User" if not self.user_data else "Edit User")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialogTitle")
        header_layout.addWidget(title)

        layout.addLayout(header_layout)

        # Form fields
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Username
        username_label = QLabel("Username:")
        username_label.setObjectName("fieldLabel")
        form_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setObjectName("inputField")
        # allow the input to expand horizontally
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(self.username_input)

        # Password
        password_label = QLabel("Password:")
        password_label.setObjectName("fieldLabel")
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password" if not self.user_data else "Leave blank to keep current")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("inputField")
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(self.password_input)

        # Role
        role_label = QLabel("Role:")
        role_label.setObjectName("fieldLabel")
        form_layout.addWidget(role_label)

        self.role_combo = QComboBox()
        self.role_combo.setObjectName("roleCombo")
        self.role_combo.addItems(["staff", "admin"])
        self.role_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(self.role_combo)

        # Fill existing data if editing
        if self.user_data:
            self.username_input.setText(self.user_data["username"])
            self.role_combo.setCurrentText(self.user_data["role"])

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.setObjectName("dialogButtons")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def apply_styles(self):
        """Apply modern stylesheet"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
            }
            
            #dialogTitle {
                font-size: 20px;
                font-weight: bold;
                color: #2a82da;
                margin: 10px 0 20px 0;
            }
            
            #formFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            
            #fieldLabel {
                font-size: 13px;
                font-weight: 600;
                color: #555;
            }
            
            #inputField, #roleCombo {
                padding: 5px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: #fafafa;
                font-size: 14px;
                min-height: 20px;
            }
            
            #inputField:focus, #roleCombo:focus {
                border: 2px solid #2a82da;
                background-color: white;
            }
            
            #dialogButtons QPushButton {
                padding: 10px 25px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
            }
            
            #dialogButtons QPushButton[text="OK"] {
                background-color: #2a82da;
                color: white;
                border: none;
            }
            
            #dialogButtons QPushButton[text="OK"]:hover {
                background-color: #1e6bb8;
            }
            
            #dialogButtons QPushButton[text="Cancel"] {
                background-color: #f5f5f5;
                color: #666;
                border: 2px solid #e0e0e0;
            }
            
            #dialogButtons QPushButton[text="Cancel"]:hover {
                background-color: #e8e8e8;
            }
        """)

    def get_data(self):
        """Return form data as dictionary"""
        return {
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "role": self.role_combo.currentText(),
        }