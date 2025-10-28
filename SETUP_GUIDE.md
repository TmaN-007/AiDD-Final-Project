# Campus Resource Hub - Complete Setup Guide

This guide will walk you through setting up the Campus Resource Hub application from scratch.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Creating Test Data](#creating-test-data)
7. [Running Tests](#running-tests)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.10 or higher**
   ```bash
   python3 --version  # Should show 3.10.0 or higher
   ```

   **Installation**:
   - macOS: `brew install python@3.10`
   - Ubuntu: `sudo apt install python3.10`
   - Windows: Download from [python.org](https://www.python.org/downloads/)

2. **pip (Python package manager)**
   ```bash
   pip3 --version
   ```

   Usually comes with Python. If not:
   ```bash
   python3 -m ensurepip --upgrade
   ```

3. **Git** (optional, for version control)
   ```bash
   git --version
   ```

### System Requirements
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for application and dependencies
- **OS**: macOS, Linux, or Windows 10/11

---

## Installation

### Step 1: Get the Code

**Option A: Clone with Git**
```bash
git clone <repository-url>
cd "Final Project"
```

**Option B: Download ZIP**
1. Download project ZIP file
2. Extract to desired location
3. Open terminal in that directory

### Step 2: Create Virtual Environment

**Why?** Isolates project dependencies from your system Python.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**Verify activation**: Your terminal prompt should show `(venv)`

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output**: Installation of Flask, bcrypt, pytest, and other packages.

**If you get errors**:
- Try: `pip install --upgrade pip` first
- Then retry: `pip install -r requirements.txt`

### Step 4: Verify Installation

```bash
python -c "import flask; print(f'Flask version: {flask.__version__}')"
```

Should print: `Flask version: 3.0.0` (or similar)

---

## Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

### Step 2: Edit .env File

Open `.env` in a text editor and configure:

```bash
# REQUIRED: Change this to a random secret string
SECRET_KEY=your-very-secret-key-here-change-this-in-production

# Database file location (optional to change)
DATABASE_PATH=campus_hub.db

# Flask environment
FLASK_ENV=development

# File upload settings
UPLOAD_FOLDER=src/static/uploads
MAX_UPLOAD_SIZE=5242880
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif
```

**Generating a secure SECRET_KEY:**

```bash
# Option 1: Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# Option 2: OpenSSL
openssl rand -hex 32
```

Copy the output and use it as your `SECRET_KEY`.

### Step 3: Create Upload Directory

```bash
mkdir -p src/static/uploads
```

---

## Database Setup

### Automatic Initialization

The database will be created automatically when you first run the application.

```bash
python app.py
```

This will:
1. Create `campus_hub.db` in the project root
2. Run all schema creation scripts
3. Set up tables with indexes

### Manual Initialization (Optional)

If you want to initialize the database without starting the server:

```python
# In Python shell
from src.data_access.database import Database
db = Database()
print("Database initialized!")
```

### Verify Database

```bash
# Check that database file exists
ls -lh campus_hub.db

# Should show a SQLite database file
```

**Optional**: Use SQLite Browser to inspect:
```bash
# Install SQLite Browser
brew install --cask db-browser-for-sqlite  # macOS

# Open database
open campus_hub.db
```

---

## Running the Application

### Start the Server

```bash
python app.py
```

**Expected output**:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

You should see the Campus Resource Hub homepage!

### Stop the Server

Press `CTRL+C` in the terminal where the server is running.

---

## Creating Test Data

### Method 1: Through the UI

1. **Register an Admin User**
   - Go to http://localhost:5000/auth/register
   - Fill in form with role=`admin`
   - Submit registration

2. **Create a Resource**
   - Log in with your admin account
   - Go to Dashboard → "Create Resource"
   - Fill in resource details:
     - Title: "Study Room A"
     - Description: "Quiet study space with whiteboard"
     - Category: "Study Room"
     - Location: "Library Building, Floor 2"
     - Capacity: 8
     - Status: "Published"
   - Submit

3. **Create a Booking**
   - Browse to the resource you created
   - Click "Book Now"
   - Select start and end times (future dates)
   - Submit booking

4. **Leave a Review**
   - After a booking is completed
   - Go to the resource page
   - Submit a rating and comment

### Method 2: Python Script

Create a file `seed_data.py`:

```python
from src.data_access.database import Database
from src.data_access.user_dal import UserDAL
from src.data_access.resource_dal import ResourceDAL
from src.utils.auth import hash_password

db = Database()
user_dal = UserDAL(db)
resource_dal = ResourceDAL(db)

# Create users
print("Creating users...")
admin_id = user_dal.create_user(
    "Admin User",
    "admin@campus.edu",
    hash_password("Admin123"),
    "admin",
    "IT Department"
)

student_id = user_dal.create_user(
    "Test Student",
    "student@campus.edu",
    hash_password("Student123"),
    "student",
    "Computer Science"
)

# Create resources
print("Creating resources...")
resource_dal.create_resource(
    owner_id=admin_id,
    title="Study Room A",
    description="Quiet study space with whiteboard",
    category="Study Room",
    location="Library Building, Floor 2",
    capacity=8,
    status="published"
)

resource_dal.create_resource(
    owner_id=admin_id,
    title="Conference Room B",
    description="Large meeting space with projector",
    category="Meeting Room",
    location="Admin Building, Room 305",
    capacity=20,
    status="published"
)

print("✅ Test data created successfully!")
print(f"Admin login: admin@campus.edu / Admin123")
print(f"Student login: student@campus.edu / Student123")
```

Run the script:
```bash
python seed_data.py
```

---

## Running Tests

### Install Test Dependencies

Already included in `requirements.txt`, but if needed:
```bash
pip install pytest pytest-flask pytest-cov
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# AI validation tests
pytest tests/ai_eval/

# Specific test file
pytest tests/unit/test_user_dal.py
```

### Run with Coverage Report

```bash
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in a browser to see detailed coverage report.

### Run with Verbose Output

```bash
pytest -v
```

### Expected Test Results

All tests should pass:
```
==================== test session starts ====================
collected 25 items

tests/unit/test_user_dal.py ........       [32%]
tests/unit/test_booking_logic.py .....     [52%]
tests/integration/test_auth_flow.py ....   [68%]
tests/ai_eval/test_concierge.py ........   [100%]

==================== 25 passed in 2.53s ====================
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Database Locked

**Error**: `database is locked`

**Solution**:
```bash
# Stop all running Flask instances
# Delete the database and restart
rm campus_hub.db
python app.py
```

#### 3. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux

# Or use different port
flask run --port 5001
```

#### 4. Permission Errors

**Error**: `Permission denied: 'src/static/uploads'`

**Solution**:
```bash
chmod 755 src/static/uploads
```

#### 5. Template Not Found

**Error**: `jinja2.exceptions.TemplateNotFound: base.html`

**Solution**:
- Verify you're running `python app.py` from the project root directory
- Check that `src/views/base.html` exists
- Ensure `template_folder='src/views'` in app.py

#### 6. SECRET_KEY Not Set

**Error**: `RuntimeError: The session is unavailable because no secret key was set`

**Solution**:
```bash
# Make sure .env file exists
cp .env.example .env

# Edit .env and set SECRET_KEY
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
```

---

## Development Tips

### Hot Reload

Flask's debug mode automatically reloads when you change code:
```bash
# Already enabled in app.py
app.run(debug=True)
```

### View Logs

```bash
# Flask logs appear in terminal where you ran app.py
# For more detailed logs, set logging level:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Database Management

```bash
# Backup database
cp campus_hub.db campus_hub.db.backup

# Reset database
rm campus_hub.db
python app.py  # Recreates fresh database
```

### Testing Individual Features

```bash
# Test authentication
python -m pytest tests/integration/test_auth_flow.py -v

# Test booking logic
python -m pytest tests/unit/test_booking_logic.py -v

# Test AI concierge
python -m pytest tests/ai_eval/test_concierge.py -v
```

---

## Next Steps

Once the application is running:

1. **Explore Features**
   - Register multiple users with different roles
   - Create various resources
   - Test the booking workflow
   - Try the AI Concierge at `/concierge`

2. **Review Code**
   - Read through `src/controllers/` to understand routing
   - Examine `src/data_access/` to see DAL pattern
   - Check `tests/` for testing examples

3. **Customize**
   - Modify templates in `src/views/`
   - Add your own CSS in `src/static/css/style.css`
   - Extend AI Concierge with new query types

4. **Deploy** (Future)
   - Switch to PostgreSQL for production
   - Use gunicorn instead of Flask development server
   - Set up HTTPS with SSL certificates
   - Deploy to Heroku, AWS, or similar platform

---

## Getting Help

### Resources

- **README.md**: Overview and architecture
- **.prompt/dev_notes.md**: AI development log
- **docs/context/shared/glossary.md**: Project terminology

### Support

If you encounter issues:
1. Check this troubleshooting section
2. Review error messages carefully
3. Search for similar issues on Stack Overflow
4. Ask your team or instructor

---

## Summary Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] .env file configured with SECRET_KEY
- [ ] Database initialized (campus_hub.db exists)
- [ ] Server starts without errors
- [ ] Application accessible at http://localhost:5000
- [ ] All tests pass with pytest
- [ ] Test data created (optional)
- [ ] AI Concierge accessible at /concierge

**If all checkboxes are checked, you're ready to develop!** 🎉

---

**Last Updated**: October 28, 2025
