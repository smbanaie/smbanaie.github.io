# Pelican Website Builder (Tornado Admin Panel)

A comprehensive Tornado-based admin interface for managing Pelican-powered websites. Create, edit, and manage blog posts, users, categories, and site content through a modern, responsive web interface with Persian (Farsi) language support.

## 🚀 Features

### ✅ Modern Admin Panel
- **Bootstrap 5 UI**: Clean, responsive design with modern styling
- **RTL Support**: Full Persian/Arabic text support with proper RTL layout
- **Vazir Font**: Beautiful Persian typography throughout the interface
- **Mobile Responsive**: Works seamlessly on all device sizes

### ✅ Content Management
- **Post Creation**: Rich Markdown editor for creating blog posts
- **Category Management**: Create, edit, and organize content categories
- **User Management**: Manage authors and contributors
- **Image Upload**: Drag-and-drop image management system
- **Article Organization**: Automatic organization by date and category

### ✅ Dashboard & Analytics
- **Statistics Overview**: Real-time counts of posts, categories, and authors
- **Maintenance Tools**: Recalculate statistics, create backups
- **Site Generation**: One-click Pelican site building (local and production)
- **Category Consistency**: Check and fix category mapping issues

### ✅ Validation & Security
- **English Name Validation**: Ensures technical names (users/categories) contain only English characters
- **Input Sanitization**: Protection against malicious input
- **Error Handling**: Comprehensive error messages and graceful failure handling

### ✅ Testing Framework
- **Comprehensive Test Suite**: 61+ test scenarios covering all functionality
- **pytest Integration**: Automated testing with detailed coverage
- **CI/CD Ready**: Test structure ready for continuous integration

## 📋 Requirements

- **Python**: 3.13+
- **Dependencies**: See `pyproject.toml`
- **Pelican**: For site generation features

### Installation

```bash
# Using uv (recommended)
uv venv .venv
.\\.venv\\Scripts\\activate
uv pip install -e .

# Or using pip
pip install -r requirements.txt
```

## 🏁 Quick Start

1. **Configure User Settings**
   Create `user_area/smbanaie/smbanaie/userconf.py`:

```python
from pathlib import Path

# Local path to the Pelican project
USER_DIR = r"e:\Projects\pelicanwebsitebuilder\user_area\smbanaie\smbanaie"

# Content directory inside USER_DIR
CONTENT_DIR = str(Path(USER_DIR) / "content")

# Author list used by the admin form
AUTHORS = ["smbanaie", "مجتبی بنائی", "testuser"]

# Categories used by the admin UI
CATEGORIES = {
    "cat_list": [
        ("Culture", "فرهنگ و جامعه"),
        ("Diary", "روزنوشت"),
        ("Meditation", "بر بلندای شعر و عرفان"),
        ("Tech", "فناوری")
    ],
    "default_category": "Diary",
    "status": {
        "Culture": "active",
        "Diary": "active",
        "Meditation": "active",
        "Tech": "active"
    }
}

# Author status mapping
AUTHOR_STATUS = {
    "smbanaie": "active",
    "مجتبی بنائی": "active",
    "testuser": "active"
}

# Default author for new articles
DEFAULT_AUTHOR = "smbanaie"

# Site repository (optional)
SITE_REPO = "https://github.com/smbanaie/smbanaie.github.io"
```

2. **Start the Server**

```bash
# Using uv
.\\.venv\\Scripts\\activate
uv run start.py

# Or using python
python start.py
```

Server runs on `http://localhost:8090` by default.

3. **Access Admin Panel**
- **Dashboard**: http://localhost:8090/admin
- **Add Post**: http://localhost:8090/posts/add
- **User Management**: http://localhost:8090/admin/users
- **Category Management**: http://localhost:8090/admin/categories

## 📁 Project Structure

```
pelicanwebsitebuilder/
├── docs/
│   ├── scratchpad.md          # Development notes and task tracking
│   └── test-cases.yml         # Comprehensive test scenarios
├── handlers/
│   ├── admin_handler.py       # Main admin functionality
│   └── index_handler.py       # Home page and utilities
├── static/                    # CSS, JS, images, fonts
├── templates/                 # Tornado templates
│   ├── admin/                 # Admin panel templates
│   └── home/                  # Public site templates
├── tests/                     # Test suite
│   ├── conftest.py           # Test configuration
│   └── test_scenarios/       # Test scenario definitions
├── user_area/                # Pelican project structure
│   └── smbanaie/
│       └── smbanaie/
│           ├── content/      # Markdown content files
│           ├── pelicanconf.py # Pelican configuration
│           └── userconf.py   # Admin panel configuration
├── start.py                  # Application entry point
├── urls.py                   # Route definitions
└── pyproject.toml           # Project configuration
```

## 🔧 Admin Panel Features

### Dashboard
- **Statistics Cards**: Total posts, categories, authors
- **Maintenance Actions**:
  - Recalculate statistics
  - Create backups
  - Generate Pelican site
- **Recent Activity**: Latest posts and changes

### User Management
- Add/edit/delete users
- Username validation (English characters only)
- Active/inactive status management
- Default author assignment
- Article count tracking

### Category Management
- Create and manage categories
- Persian display names with English technical names
- Category status (active/inactive)
- Article count display
- Migration options for category deletion

### Content Creation
- Markdown editor with live preview
- Image upload and management
- Category and author selection
- Automatic file organization
- Persian date support (Jalali calendar)

### Site Generation
- **Local Build**: Development preview generation
- **Production Build**: Optimized production site generation
- **Error Handling**: Comprehensive error reporting
- **Progress Tracking**: Real-time status updates

## 🧪 Testing

The project includes a comprehensive test suite with 61+ test scenarios:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=handlers --cov-report=html tests/

# Run specific test categories
pytest -k "user_management"
pytest -k "category_management"
pytest -k "validation"
```

### Test Categories
- **User Management**: CRUD operations, validation, permissions
- **Category Management**: Organization, migration, constraints
- **Article Counting**: Statistics accuracy, Persian text handling
- **Validation**: Input sanitization, security checks
- **Site Generation**: Pelican integration, error handling
- **UI/UX**: Responsive design, accessibility, Persian support

## 🔗 Pelican Integration

The admin panel creates Pelican-compatible Markdown files with proper front-matter:

```markdown
title: مقاله نمونه
date: 2024-01-15
modified: 2024-01-15
icon: icon-link2
lang: fa
category: فناوری
tags: نمونه, مقاله
authors: نویسنده نمونه
slug: نمونه-مقاله
summary: خلاصه مقاله
image: /images/sample.jpg

محتوای مقاله در اینجا قرار می‌گیرد...
```

### Building the Site

```bash
# Navigate to Pelican project
cd user_area/smbanaie/smbanaie

# Local development build
invoke build

# Production build
invoke preview

# Serve locally
invoke serve
```

## 🌍 Internationalization

- **Persian (Farsi) Support**: Complete RTL interface
- **Jalali Calendar**: Persian date handling
- **Cultural Adaptation**: Persian number formatting and text direction

## 🔒 Security Features

- **Input Validation**: Comprehensive form validation
- **XSS Protection**: Sanitized user inputs
- **Path Security**: Safe file operations
- **Access Control**: Proper permission handling

## 📊 Monitoring & Logging

- **Comprehensive Logging**: Detailed operation logs
- **Error Tracking**: Graceful error handling with user feedback
- **Performance Monitoring**: Response time tracking
- **Audit Trail**: User action logging

## 🚀 Deployment

### Using Docker
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .
COPY . .
EXPOSE 8090
CMD ["python", "start.py"]
```

### Production Deployment
```bash
# Install dependencies
pip install -e .

# Configure production settings
export PYTHONPATH=/path/to/app

# Start with production config
python start.py --port=80 --debug=false
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is open source. See individual files for license information.

## 🐛 Known Issues & Troubleshooting

- **Import Errors**: Ensure `userconf.py` exists with proper configuration
- **Permission Issues**: Check file system permissions for content directories
- **Pelican Integration**: Verify Pelican installation and configuration
- **Browser Compatibility**: Test with modern browsers supporting ES6+

## 📞 Support

For issues and questions:
1. Check the test cases in `docs/test-cases.yml`
2. Review logs in the `logs/` directory
3. Ensure all dependencies are properly installed

---
*Generated with ❤️ for the Persian developer community*

