#!/usr/bin/python3
"""Enhanced main window with modern design and full integration"""
#!/usr/bin/python3
"""Enhanced main window with a professional, stripped-down UI."""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QFileDialog, QMessageBox, QStatusBar,
    QSplitter, QFrame, QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont
from ui.uploader import UploadDialog
from ui.user_admin import UserAdminWindow


class MainWindow(QMainWindow):
    logout_signal = Signal()

    def __init__(self, user=None):
        super().__init__()

        # Handle user data
        if isinstance(user, dict):
            self.role = user.get('role', 'staff')
            self.username = user.get('username', 'Guest')
        else:
            self.role = 'staff'
            self.username = 'Guest'

        self.setWindowTitle("EDMS - Electronic Document Management System")
        self.resize(1200, 700)

        self._create_menu_bar()
        self._create_status_bar()
        self._init_ui()
        self.apply_styles()

    def _create_menu_bar(self):
        """Create a clean, professional menu bar."""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")

        upload_action = QAction("Upload Workbook", self)
        upload_action.setShortcut("Ctrl+U")
        upload_action.triggered.connect(self.open_upload_dialog)
        file_menu.addAction(upload_action)

        file_menu.addSeparator()

        export_action = QAction("Export Results", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        logout_action = QAction("Logout", self)
        logout_action.setShortcut("Ctrl+L")
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menubar.addMenu("View")
        refresh_action = QAction("Refresh Data", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.perform_search)
        view_menu.addAction(refresh_action)

        # Admin Menu (only for admin)
        if self.role == "admin":
            admin_menu = menubar.addMenu("Admin")
            user_mgmt_action = QAction("User Management", self)
            user_mgmt_action.triggered.connect(self.open_user_admin)
            admin_menu.addAction(user_mgmt_action)

            sys_settings_action = QAction("System Settings", self)
            sys_settings_action.triggered.connect(self.open_settings)
            admin_menu.addAction(sys_settings_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About EDMS", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def _create_status_bar(self):
        """Create a minimal status bar showing user and connection state."""
        status = QStatusBar()

        user_label = QLabel(f"{self.username} ({self.role.title()})")
        status.addPermanentWidget(user_label)

        self.conn_label = QLabel("Connected")
        status.addPermanentWidget(self.conn_label)

        status.showMessage("Ready")
        self.setStatusBar(status)

    def _init_ui(self):
        """Build the main interface layout."""
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = self._create_header()
        main_layout.addWidget(header)

        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        left_panel = self._create_filter_panel()
        right_panel = self._create_main_panel()

        content_splitter.addWidget(left_panel)
        content_splitter.addWidget(right_panel)
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 3)

        main_layout.addWidget(content_splitter)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_header(self):
        """Header with title and quick actions."""
        header = QFrame()
        header.setObjectName("headerFrame")
        header.setMaximumHeight(80)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)

        title_layout = QVBoxLayout()
        title = QLabel("Document Management Dashboard")
        title.setObjectName("headerTitle")
        subtitle = QLabel(f"Welcome back, {self.username}!")
        subtitle.setObjectName("headerSubtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)

        layout.addStretch()

        upload_btn = QPushButton("Upload")
        upload_btn.setObjectName("quickActionBtn")
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.clicked.connect(self.open_upload_dialog)

        export_btn = QPushButton("Export")
        export_btn.setObjectName("quickActionBtn")
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self.export_results)

        layout.addWidget(upload_btn)
        layout.addWidget(export_btn)

        header.setLayout(layout)
        return header

    def _create_filter_panel(self):
        """Left-side filter panel."""
        panel = QFrame()
        panel.setObjectName("filterPanel")
        panel.setMaximumWidth(280)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        title = QLabel("Search Filters")
        title.setObjectName("panelTitle")
        layout.addWidget(title)

        layout.addWidget(self._create_filter_section("Year",
            ["All Years", "2023", "2024", "2025", "2026"]))
        self.year_combo = layout.itemAt(layout.count()-1).widget().findChild(QComboBox)

        layout.addWidget(self._create_filter_section("Department",
            ["All Departments", "Admin", "Account", "Audit", "Agriculture",
             "Education", "Environmental", "Health", "Works"]))
        self.dept_combo = layout.itemAt(layout.count()-1).widget().findChild(QComboBox)

        layout.addWidget(self._create_filter_section("Local Government",
            ["All LGAs", "Ajingi", "Albasu", "Bagwai", "Bebeji", "Bichi",
             "Bunkure", "Dala", "Dambatta", "Dawakin Kudu", "Dawakin Tofa"]))
        self.lga_combo = layout.itemAt(layout.count()-1).widget().findChild(QComboBox)

        search_label = QLabel("Keyword Search")
        search_label.setObjectName("filterLabel")
        layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("File number, name, etc...")
        self.search_input.setObjectName("searchInput")
        self.search_input.returnPressed.connect(self.perform_search)
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.clicked.connect(self.perform_search)
        layout.addWidget(search_btn)

        clear_btn = QPushButton("Clear Filters")
        clear_btn.setObjectName("clearButton")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_filters)
        layout.addWidget(clear_btn)

        layout.addStretch()

        stats_card = self._create_stats_card()
        layout.addWidget(stats_card)

        panel.setLayout(layout)
        return panel

    def _create_filter_section(self, label_text, items):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        label = QLabel(label_text)
        label.setObjectName("filterLabel")
        layout.addWidget(label)

        combo = QComboBox()
        combo.setObjectName("filterCombo")
        combo.addItems(items)
        # Make combos expand to fill the panel width on large/full screens
        combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        combo.setMinimumWidth(200)
        layout.addWidget(combo)

        container.setLayout(layout)
        return container

    def _create_stats_card(self):
        card = QFrame()
        card.setObjectName("statsCard")

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Quick Stats")
        title.setObjectName("statsTitle")
        layout.addWidget(title)

        stats_text = QLabel("Total Records: 1,234\nThis Year: 567\nPending: 45")
        stats_text.setObjectName("statsText")
        layout.addWidget(stats_text)

        card.setLayout(layout)
        return card

    def _create_main_panel(self):
        panel = QFrame()
        panel.setObjectName("mainPanel")

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Table header
        header_layout = QHBoxLayout()
        results_label = QLabel("Search Results")
        results_label.setObjectName("panelTitle")
        header_layout.addWidget(results_label)

        header_layout.addStretch()

        self.result_count = QLabel("0 records")
        self.result_count.setObjectName("resultCount")
        header_layout.addWidget(self.result_count)

        layout.addLayout(header_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "File No", "Name", "Department", "Year", "LGA", "Status"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setObjectName("mainTable")

        layout.addWidget(self.table)

        # Action buttons for selected row
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        view_btn = QPushButton("View Details")
        view_btn.setObjectName("actionButton")
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.clicked.connect(self.view_record)

        download_btn = QPushButton("Download")
        download_btn.setObjectName("actionButton")
        download_btn.setCursor(Qt.PointingHandCursor)
        download_btn.clicked.connect(self.download_record)

        action_layout.addWidget(view_btn)
        action_layout.addWidget(download_btn)

        layout.addLayout(action_layout)

        panel.setLayout(layout)
        return panel

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            
            #headerFrame {
                background-color: white;
                border-bottom: 2px solid #e0e0e0;
            }
            
            #headerTitle {
                font-size: 20px;
                font-weight: bold;
                color: #2a82da;
            }
            
            #headerSubtitle {
                font-size: 13px;
                color: #666;
            }
            
            #filterPanel, #mainPanel {
                background-color: white;
                border-radius: 8px;
                margin: 10px;
            }
            
            #panelTitle {
                font-size: 16px;
                font-weight: 600;
                color: #333;
                margin-bottom: 10px;
            }
            
            #filterLabel {
                font-size: 13px;
                font-weight: 600;
                color: #555;
            }
            
            #filterCombo, #searchInput {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: #fafafa;
                font-size: 13px;
            }
            
            #filterCombo:focus, #searchInput:focus {
                border: 2px solid #2a82da;
                background-color: white;
            }
            
            #searchButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            
            #searchButton:hover {
                background-color: #1e6bb8;
                self.search_input = QLineEdit()
                self.search_input.setPlaceholderText("File number, name, etc...")
                self.search_input.setObjectName("searchInput")
                self.search_input.returnPressed.connect(self.perform_search)
                # Make the search input expand to available width
                self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.search_input.setMinimumWidth(240)
                layout.addWidget(self.search_input)
                font-size: 13px;
            }
            
            #clearButton:hover {
                background-color: #e8e8e8;
            }
            
            #statsCard {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            
            #statsTitle {
                font-size: 14px;
                font-weight: 600;
                color: #333;
                margin-bottom: 8px;
            }
            
            #statsText {
                font-size: 12px;
                color: #666;
                line-height: 1.6;
            }
            
            #resultCount {
                font-size: 13px;
                color: #666;
                padding: 5px 10px;
                background-color: #f0f0f5;
                border-radius: 4px;
            }
            
            #mainTable {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                gridline-color: #f0f0f0;
            }
            
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 600;
                color: #333;
            }
            
            #actionButton, #quickActionBtn {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 6px;
                    # Keep the result count visible on wide/full screens
                    self.result_count.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.result_count.setMinimumWidth(140)
                    self.result_count.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                    header_layout.addWidget(self.result_count)
            
            #actionButton:hover, #quickActionBtn:hover {
                background-color: #1e6bb8;
            }
            
            QMenuBar {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 5px;
            }
            
            QMenuBar::item {
                padding: 8px 12px;
                background-color: transparent;
            }
            
            QMenuBar::item:selected {
                background-color: #f0f0f5;
                border-radius: 4px;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            
            QMenu::item {
                padding: 8px 25px;
            }
            
            QMenu::item:selected {
                background-color: #e3f2fd;
            }
            
            QStatusBar {
                background-color: white;
                border-top: 1px solid #e0e0e0;
                color: #666;
            }
        """)

    # Action handlers
    def perform_search(self):
        """Simulate a record search and populate table."""
        self.statusBar().showMessage("Searching records...")
        self.table.setRowCount(0)

        fake_data = [
            ["WRK-001", "John Doe", "Works", "2025", "Dala", "Active"],
            ["ACC-002", "Jane Smith", "Account", "2025", "Albasu", "Pending"],
            ["EDU-003", "Abdul Rasheed", "Education", "2024", "Bichi", "Active"],
            ["HLT-004", "Fatima Abubakar", "Health", "2025", "Dambatta", "Active"],
            ["AGR-005", "Muhammad Ali", "Agriculture", "2024", "Bebeji", "Archived"],
            ["AUD-006", "Aisha Bello", "Audit", "2025", "Ajingi", "Pending"],
            ["ENV-007", "Ibrahim Hassan", "Environmental", "2024", "Bagwai", "Active"],
            ["ADM-008", "Zainab Usman", "Admin", "2025", "Bunkure", "Active"],
        ]

        for row_data in fake_data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                if col == 5:  # Status column
                    if value == "Active":
                        item.setForeground(Qt.darkGreen)
                    elif value == "Pending":
                        item.setForeground(Qt.darkYellow)
                    else:
                        item.setForeground(Qt.gray)
                self.table.setItem(row, col, item)

        self.result_count.setText(f"{len(fake_data)} records")
        self.statusBar().showMessage(f"Found {len(fake_data)} records", 3000)

    def clear_filters(self):
        """Clear all filters"""
        self.year_combo.setCurrentIndex(0)
        self.dept_combo.setCurrentIndex(0)
        self.lga_combo.setCurrentIndex(0)
        self.search_input.clear()
        self.table.setRowCount(0)
        self.result_count.setText("0 records")
        self.statusBar().showMessage("Filters cleared", 2000)

    def open_upload_dialog(self):
        """Open file upload dialog."""
        dialog = UploadDialog(parent=self)
        if dialog.exec():
            self.statusBar().showMessage("Upload completed successfully", 3000)
            self.perform_search()

    def export_results(self):
        """Export current results"""
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "No Data", "No records to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        if file_path:
            QMessageBox.information(self, "Export", f"Results exported to: {file_path}")
            self.statusBar().showMessage(f"Exported to {file_path}", 3000)

    def view_record(self):
        """View details of selected record"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a record to view.")
            return

        file_no = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()

        QMessageBox.information(
            self, "Record Details",
            f"File Number: {file_no}\nName: {name}\n\n[Full details would appear here]"
        )

    def download_record(self):
        """Download selected record"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a record to download.")
            return

        file_no = self.table.item(row, 0).text()
        QMessageBox.information(self, "Download", f"Downloading file: {file_no}")
        self.statusBar().showMessage(f"Downloaded {file_no}", 3000)

    def open_user_admin(self):
        """Open user admin window (only for admins)."""
        if self.role != "admin":
            QMessageBox.warning(
                self, "Access Denied",
                "You do not have permission to access user management."
            )
            return

        self.user_admin = UserAdminWindow()
        self.user_admin.show()

    def open_settings(self):
        """Open system settings"""
        QMessageBox.information(
            self, "Settings",
            "System settings panel\n[Configuration options would appear here]"
        )

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About EDMS",
            "<h2>Electronic Document Management System</h2>"
            "<p>Version 1.0.0</p>"
            "<p>A comprehensive solution for managing government documents</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Document upload and storage</li>"
            "<li>Advanced search and filtering</li>"
            "<li>User access control</li>"
            "<li>Export and reporting</li>"
            "</ul>"
            "<p><b>Contact:</b> +234 8172 992 396, support@rashnotech.tech</p>"
            "<p>© 2025 Rashnotech Solutions</p>"
        )

    def logout(self):
        """Return to login screen."""
        reply = QMessageBox.question(
            self, "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.logout_signal.emit()