# Complaint Management System (CMS)
**Riphah International University**

---

## 📋 Project Overview

The Complaint Management System is a comprehensive web-based application developed for Riphah International University to streamline the complaint handling process. It provides a centralized platform for users to submit complaints, track their status, and receive real-time notifications while enabling administrators to manage, assign, and resolve complaints efficiently.

**Status:** ✅ **COMPLETE - PRODUCTION READY**  
**Version:** 1.0  
**Last Updated:** December 2025

---

## 🎯 Key Objectives Met

✅ Centralized complaint registration and tracking  
✅ Role-based user access (Users & Admins)  
✅ Real-time in-app notifications  
✅ Secure file attachment handling  
✅ Comprehensive dashboard with analytics  
✅ Mobile-responsive user interface  
✅ 100% test coverage (27/27 tests passing)  
✅ Production-ready deployment configuration  

---

## 🏗️ System Architecture

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11.9, Flask 3.1.2, Flask-SQLAlchemy 3.1.1 |
| **Frontend** | HTML5, Jinja2, Bootstrap 5.3.0, JavaScript |
| **Database** | MySQL 8.0+ (Production), SQLite (Development) |
| **Security** | Werkzeug (Password Hashing), Flask-Login, Flask-WTF (CSRF) |
| **Deployment** | Gunicorn 23.0.0, Railway, Docker Ready |

### Architecture Pattern
The system follows the **MVC (Model-View-Controller)** pattern:
- **Models**: SQLAlchemy ORM (User, Complaint, Comment, Notification)
- **Views**: Jinja2 templates with Bootstrap CSS
- **Controllers**: Flask routes and blueprints

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- MySQL 8.0+ (for production) or SQLite (for development)

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/Talhaaftab5462/Riphah-Complaint-Management-System.git
cd cms-project

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with configuration
# Copy and modify environment variables:
# MYSQLHOST=localhost
# MYSQLUSER=root
# MYSQLPASSWORD=password
# MYSQLDATABASE=cms_db
# SECRET_KEY=your-secret-key-here

# 6. Initialize database
flask init-db

# 7. Create admin user
python create_admin.py

# 8. Run development server
flask run
```

The application will be available at: `http://localhost:5000`

---

## 🚀 Deployment

### Production Deployment (Railway)

1. **Set up MySQL Database**
   - Provision MySQL 8.0+ instance
   - Create database and user

2. **Configure Environment Variables**
   ```
   MYSQLHOST=<host>
   MYSQLPORT=3306
   MYSQLUSER=<user>
   MYSQLPASSWORD=<password>
   MYSQLDATABASE=<database>
   SECRET_KEY=<secure-random-string>
   ```

3. **Deploy Application**
   ```bash
   # Via Railway (recommended)
   railway up
   
   # Or via traditional deployment
   gunicorn "cms_app:create_app()"
   ```

4. **Initialize Production Database**
   ```bash
   flask init-db
   python create_admin.py
   ```

---

## 📚 Core Features

### 1. User Authentication
- **Registration**: Email, username, secure password hashing
- **Login/Logout**: Session-based authentication via Flask-Login
- **Password Security**: PBKDF2 hashing via Werkzeug

### 2. Complaint Management
- **Submit Complaints**: Title, Category, Priority, Description, File Attachment
- **Categories**: Academic, Facilities, Transport, Hostel, Administration
- **Priority Levels**: Low, Medium, High
- **Status Tracking**: Pending → In Progress → Approved/Denied/Resolved
- **File Attachments**: Secure upload with filename sanitization

### 3. Notifications
- **Automatic Alerts**: On status changes
- **In-App Display**: Notification dropdown with unread count
- **Message Format**: "Your complaint '[Title]' status has been updated to '[Status]'"
- **Mark as Read**: Users can mark notifications as read

### 4. Admin Functions
- **View All Complaints**: From all users
- **Assign Complaints**: To staff members
- **Update Status**: Change complaint status
- **Add Comments**: Collaborate with users
- **Dashboard Analytics**: Real-time statistics by status and category

### 5. Dashboard
- **User Dashboard**: Only their own complaints
- **Admin Dashboard**: All complaints + statistics
- **Statistics Cards**: Total, Pending, In Progress, Resolved, Approved, Denied
- **Category Breakdown**: Complaints grouped by category
- **Real-Time Updates**: Statistics update on every change

---

## 🔐 Security Features

✅ **Password Security**: Werkzeug PBKDF2-based hashing (never plaintext)  
✅ **CSRF Protection**: Flask-WTF tokens on all forms  
✅ **Session Management**: Secure cookies via Flask-Login  
✅ **SQL Injection Prevention**: SQLAlchemy parameterized queries  
✅ **File Upload Security**: Werkzeug secure_filename() prevents directory traversal  
✅ **Authorization**: Role-based access control (User/Admin)  
✅ **Environment Secrets**: Credentials via environment variables  

---

## 📝 Project Structure

```
cms-project/
├── cms_app/
│   ├── __init__.py              # App factory & initialization
│   ├── models.py                # SQLAlchemy ORM models
│   ├── routes.py                # Flask routes & controllers
│   ├── forms.py                 # WTForms (ComplaintForm)
│   ├── static/
│   │   ├── css/                 # Stylesheets
│   │   ├── images/              # Logo, icons
│   │   ├── js/                  # JavaScript files
│   │   └── uploads/             # User file attachments
│   └── templates/
│       ├── base.html            # Master layout
│       ├── index.html           # Home page
│       ├── login.html           # Login form
│       ├── register.html        # Registration form
│       ├── dashboard.html       # Main dashboard
│       ├── complaint_form.html  # Complaint submission
│       └── view_complaint.html  # Complaint details
├── config.py                    # Application configuration
├── create_admin.py              # Admin user creation utility
├── requirements.txt             # Python dependencies
├── Procfile                     # Gunicorn entry point
└── README.md                    # This file
```

---

## 🧪 Testing

### Test Coverage
- **Unit Tests**: 10 tests (Authentication, Complaint Submission, Validation)
- **Integration Tests**: 3 tests (Complaint Workflow, Notifications, Comments)
- **System Tests**: 5 tests (End-to-end user journeys, Authorization)
- **Security Tests**: 5 tests (SQL Injection, CSRF, File Security)
- **Performance Tests**: 4 tests (Dashboard Load, Form Submission, Queries)

**Total: 27 Tests | Pass Rate: 100% ✅**

### Running Tests
```bash
# Execute test suite
pytest

# With coverage report
pytest --cov=cms_app
```

---

## 📊 API Endpoints

| Method | Route | Purpose | Auth |
|--------|-------|---------|------|
| GET | `/` | Home page | No |
| GET/POST | `/register` | User registration | No |
| GET/POST | `/login` | User login | No |
| GET | `/logout` | User logout | Yes |
| GET | `/dashboard` | Dashboard with statistics | Yes |
| GET/POST | `/submit_complaint` | Submit new complaint | Yes |
| GET | `/complaint/<id>` | View complaint details | Yes |
| POST | `/complaint/<id>` | Add comment | Yes |
| POST | `/assign/<id>` | Assign complaint | Yes (Admin) |
| GET | `/update_status/<id>/<status>` | Update status | Yes (Admin) |
| GET | `/notification/read/<id>` | Mark notification read | Yes |

---

## 📱 Browser Compatibility

✅ Chrome 90+  
✅ Firefox 88+  
✅ Safari 14+  
✅ Edge 90+  
✅ Mobile Browsers (iOS Safari, Chrome Mobile)  

---

## 🔄 Workflow Example

### Complete Complaint Lifecycle

1. **User Registration**
   - Navigate to `/register`
   - Create account with email and password

2. **Submit Complaint**
   - Click "Submit Complaint"
   - Fill form (Title, Category, Priority, Description, optional file)
   - Status auto-set to "Pending"

3. **Admin Assignment**
   - Admin views dashboard
   - Selects staff member and assigns complaint

4. **Status Update**
   - Admin changes status: Pending → In Progress
   - User receives notification

5. **Collaboration**
   - User and admin exchange comments
   - Both see conversation in complaint details

6. **Resolution**
   - Admin updates status to "Resolved"
   - User notified and cannot comment further
   - Complaint appears in resolved statistics

---

## 🐛 Known Limitations (v1.0)

- Email notifications not implemented (in-app only)
- No password reset functionality
- No complaint editing after submission
- Single-server deployment (not scaled)
- File storage local to server (not S3/cloud)
- No advanced reporting/charts

---

## 🚧 Future Enhancements

- Email notification integration (SMTP)
- Advanced analytics with charts
- Complaint templates
- SLA tracking and escalation
- Mobile application (iOS/Android)
- Bulk operations (export, archive)
- Audit logging
- Multi-language support

---

## 📞 Support & Contact

For questions, issues, or deployment assistance:

**Project Repository**: [https://github.com/Talhaaftab5462/Riphah-Complaint-Management-System](https://github.com/Talhaaftab5462/Riphah-Complaint-Management-System)

**Lead Developer**: Talha Aftab

**Other Developers**: Haris Habib, Habibullah Naz, Shehbaz Touqeer
**Institution**: Riphah International University

---

## 📄 Documentation Files

- **SRS_CMS_Riphah.docx** - Detailed Software Requirements Specification
- **SystemDesign_CMS_Riphah.docx** - Complete System Design Document
- **TestCases_CMS_Riphah.docx** - Comprehensive Test Cases (27 tests)
- **CMS_Presentation.pptx** - Final Presentation Guide
- **Readme.md** - This file

---

## ✨ Acknowledgments

This project was developed as part of the academic curriculum at Riphah International University, following best practices in software engineering, security, and user interface design.

---

**Status**: ✅ Complete and Ready for Production Use  
**Last Updated**: December 2025  
**Version**: 1.0
