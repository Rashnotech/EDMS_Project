# EDMS - Electronic Document Management System

A modern, professional desktop application for managing government documents with advanced search, filtering, and user management capabilities.

## 🎨 Features

### Visual Enhancements
- **Professional Splash Screen** - Shows on startup with smooth animations
- **Modern UI Design** - Clean, contemporary interface with blue-gray theme
- **Responsive Layout** - Adaptive design that works on different screen sizes
- **Smooth Animations** - Polished transitions and interactions
- **Status Indicators** - Real-time feedback for user actions

### Core Functionality
- **User Authentication** - Secure login with role-based access
- **Document Upload** - Excel workbook upload with progress tracking
- **Advanced Search** - Filter by year, department, LGA, and keywords
- **User Management** - Admin panel for managing system users
- **Data Export** - Export search results to Excel/CSV
- **Real-time Stats** - Dashboard showing document statistics

## 📁 Project Structure

```
edms_project/
├── client/
│   ├── main.py                 # Application entry point with splash screen
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_window.py     # Enhanced login interface
│   │   ├── main_window.py      # Main dashboard
│   │   ├── uploader.py         # File upload dialog
│   │   └── user_admin.py       # User management window
│   └── assets/
│       └── icon.png            # Application icon (create this)
├── requirements.txt
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
```bash
git clone <your-repository-url>
cd edms_project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create Requirements File
Create `requirements.txt` with the following content:

```
PySide6>=6.5.0
requests>=2.31.0
```

### Step 4: Create Asset Folder (Optional)
```bash
mkdir -p client/assets
# Add your icon.png file to client/assets/
```

## 🎮 Running the Application

### Start the Application
```bash
cd client
python main.py
```

### Default Login Credentials
- **Admin Account**
  - Username: `admin`
  - Password: `1234`
  - Access: Full system access including user management

- **Staff Account**
  - Username: `staff`
  - Password: `1234`
  - Access: Standard document management features

## 📋 User Guide

### 1. Login
- Launch the application
- Wait for the splash screen (2-3 seconds)
- Enter your credentials
- Click "Login"

### 2. Dashboard Overview
- **Header**: Quick action buttons for Upload and Export
- **Left Panel**: Search filters (Year, Department, LGA, Keywords)
- **Main Panel**: Search results table
- **Status Bar**: Shows current user and connection status

### 3. Searching Documents
1. Select filters (Year, Department, LGA) or leave as "All"
2. Enter keywords in the search box (optional)
3. Click "Search" or press Enter
4. Results appear in the main table
5. Click on any row to select it
6. Use "View Details" or "Download" buttons

### 4. Uploading Documents
1. Click "Upload" in the header or menu (File → Upload Workbook)
2. Click "Browse Files" to select an Excel file
3. Choose the target year
4. Click "Upload"
5. Wait for progress bar to complete

### 5. User Management (Admin Only)
1. Go to Admin → User Management
2. **Add User**: Click "Add User" button
3. **Edit User**: Select user, click "Edit User"
4. **Delete User**: Select user, click "Delete User"
5. **Refresh**: Click "Refresh" to reload user list

### 6. Exporting Data
1. Perform a search to get results
2. Click "Export" button or File → Export Results
3. Choose save location and format (Excel/CSV)
4. Click Save

### 7. Logout
- File → Logout
- Confirm logout
- Returns to login screen

## 🛠️ Configuration

### Customizing Colors
Edit the color scheme in each file's `apply_styles()` method:
- Primary Blue: `#2a82da`
- Background: `#f5f5f7`
- Text: `#333333`

### API Integration
To connect to a real backend:

1. **Update API URL** in `uploader.py`:
```python
dialog = UploadDialog(api_url="http://your-server:port/api/upload")
```

2. **Implement Authentication** in `login_window.py`:
```python
def attempt_login(self):
    # Replace simulated login with API call
    response = requests.post('http://your-server/api/login', 
                            data={'username': username, 'password': password})
```

3. **Implement Search** in `main_window.py`:
```python
def perform_search(self):
    # Replace fake data with API call
    response = requests.get('http://your-server/api/search',
                           params={'year': year, 'dept': dept})
```

## 🔧 Development

### File Descriptions

**main.py**
- Application controller
- Manages window transitions
- Handles splash screen
- Sets global styling

**login_window.py**
- User authentication interface
- Form validation
- Signal emission on success

**main_window.py**
- Main application dashboard
- Search and filter functionality
- Table display
- Menu and toolbar management

**uploader.py**
- File upload dialog
- Progress tracking
- Background upload worker
- API communication

**user_admin.py**
- User CRUD operations
- Role management
- User listing and filtering

### Adding New Features

1. **Add New Menu Item**:
```python
def _create_menu_bar(self):
    new_menu = menubar.addMenu("New Menu")
    action = QAction("New Action", self)
    action.triggered.connect(self.new_function)
    new_menu.addAction(action)
```

2. **Add New Filter**:
```python
self.status_combo = QComboBox()
self.status_combo.addItems(["All", "Active", "Pending", "Archived"])
```

3. **Add New Table Column**:
```python
self.table.setColumnCount(7)  # Increase count
self.table.setHorizontalHeaderLabels([..., "New Column"])
```

## 🐛 Troubleshooting

### Application Won't Start
- Verify Python version: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check for import errors

### Splash Screen Doesn't Appear
- Check if QApplication is created before splash screen
- Verify `processEvents()` is called
- Ensure proper timing with QTimer

### Upload Fails
- Check server is running
- Verify API URL is correct
- Check file permissions
- Review network connectivity

### Styling Issues
- Ensure `setStyle('Fusion')` is called
- Check stylesheet syntax
- Verify object names match CSS selectors

## 📝 TODO / Future Enhancements

- [ ] Database integration (PostgreSQL/MySQL)
- [ ] RESTful API backend
- [ ] Advanced reporting and analytics
- [ ] Document preview functionality
- [ ] Bulk operations
- [ ] Activity logging and audit trail
- [ ] Email notifications
- [ ] PDF generation
- [ ] Multi-language support
- [ ] Dark mode theme

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Credits

Developed for government document management needs.

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Version**: 1.0.0  
**Last Updated**: October 2025