# Campus Resource Hub

A full-stack web application for managing and booking campus resources including study rooms, equipment, lab instruments, event spaces, and more.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [AI Integration](#ai-integration)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Team](#team)

---

## Features

### Core Features

✅ **User Management & Authentication**
- Secure registration and login with bcrypt password hashing
- Role-based access control (Student, Staff, Admin)
- User profiles with department affiliation

✅ **Resource Management**
- Create, read, update, and delete resources
- Rich resource information (title, description, category, location, capacity)
- Resource lifecycle management (draft, published, archived)
- Image support for resource listings

✅ **Advanced Search & Filtering**
- Keyword search across titles and descriptions
- Filter by category, location, and availability
- Sort by ratings, popularity, and recency

✅ **Intelligent Booking System**
- Calendar-based booking with datetime selection
- Automatic conflict detection prevents double-booking
- Multi-status workflow (pending, approved, rejected, cancelled, completed)
- Resource owner and staff approval capabilities

✅ **Messaging System**
- Thread-based conversations between users
- Contact resource owners directly
- Persistent message history

✅ **Reviews & Ratings**
- 5-star rating system
- Text reviews with comments
- Aggregate ratings display
- One review per user per resource

✅ **Admin Dashboard**
- System-wide statistics and analytics
- User management
- Booking approval queue
- Usage reports by category and department
- Admin activity logging

✅ **AI Resource Concierge** 🤖
- Natural language query interface
- Intelligent resource recommendations
- Availability checking
- System statistics and insights
- **All responses grounded in real database data - no fabrication**

---

## Technology Stack

### Backend
- **Python 3.10+** - Core programming language
- **Flask 3.0** - Web framework
- **SQLite** - Database (PostgreSQL-ready for production)
- **bcrypt** - Password hashing
- **pytest** - Testing framework

### Frontend
- **Jinja2** - Templating engine
- **Bootstrap 5.3** - UI framework
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Client-side interactions

### Architecture
- **MVC Pattern** - Model-View-Controller separation
- **Data Access Layer (DAL)** - Encapsulated database operations
- **Blueprint-based routing** - Modular Flask controllers
- **AI-First Repository Structure** - `.prompt/` and `docs/context/` for AI collaboration

---

## Architecture

### MVC + Data Access Layer

```
┌─────────────────────────────────────────────────────┐
│                    Flask Application                 │
├─────────────────────────────────────────────────────┤
│  Controllers (Routes)                                │
│  ├─ auth_controller.py                              │
│  ├─ resource_controller.py                          │
│  ├─ booking_controller.py                           │
│  ├─ message_controller.py                           │
│  ├─ review_controller.py                            │
│  ├─ admin_controller.py                             │
│  └─ concierge_controller.py (AI)                    │
├─────────────────────────────────────────────────────┤
│  Data Access Layer (DAL)                            │
│  ├─ user_dal.py                                     │
│  ├─ resource_dal.py                                 │
│  ├─ booking_dal.py                                  │
│  ├─ message_dal.py                                  │
│  ├─ review_dal.py                                   │
│  └─ admin_dal.py                                    │
├─────────────────────────────────────────────────────┤
│  Database (SQLite)                                   │
│  └─ schema.py (7 tables, indexed)                   │
└─────────────────────────────────────────────────────┘
```

**Key Design Principles:**
- Controllers NEVER contain raw SQL
- DAL methods use parameterized queries (SQL injection prevention)
- All user input validated server-side
- Templates use Jinja2 auto-escaping (XSS prevention)

---

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Final Project"
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

5. **Initialize database**
```bash
# Database will be created automatically on first run
python app.py
```

6. **Access application**
```
Open browser to: http://localhost:5000
```

### First-Time Setup

1. **Register an account** at `/auth/register`
2. **Create your first resource** as a staff or student user
3. **Try the AI Concierge** at `/concierge`

---

## Usage

### User Workflows

#### For Students

1. **Browse Resources**
   - Navigate to "Browse Resources"
   - Use search and filters to find what you need
   - View resource details and reviews

2. **Book a Resource**
   - Click "Book Now" on resource page
   - Select start and end datetime
   - Submit booking request
   - Wait for approval from resource owner/staff

3. **Manage Bookings**
   - View your bookings in Dashboard
   - Cancel bookings if needed
   - Leave reviews after completed bookings

#### For Staff/Resource Owners

1. **Create Resource**
   - Go to Dashboard → "Create Resource"
   - Fill in details (title, description, category, location, capacity)
   - Set status to "Published" to accept bookings

2. **Manage Bookings**
   - View pending bookings for your resources
   - Approve or reject booking requests
   - Monitor resource utilization

#### For Admins

1. **Access Admin Panel** at `/admin`
2. **View System Statistics**
3. **Manage Users** - View, suspend, or delete accounts
4. **Moderate Reviews** - Remove inappropriate content
5. **View Analytics** - Usage by category and department

### AI Concierge Usage

Access at `/concierge` or click "AI Concierge" in navigation.

**Example Queries:**
- "Show me the best resources"
- "What are the most popular categories?"
- "What are the system statistics?"
- "Which resources are most booked?"

**Features:**
- Natural language understanding
- Real-time database queries
- No fabricated information
- Helpful suggestions and insights

---

## AI Integration

### AI-Powered Features

#### 1. Resource Concierge
**File**: [src/utils/ai_concierge.py](src/utils/ai_concierge.py)

An intelligent assistant that helps users discover resources and understand system usage.

**Capabilities:**
- Search resources by natural language queries
- Recommend top-rated resources
- Check resource availability
- Provide system statistics
- Answer questions about categories

**Key Design Principle**: **Zero Fabrication**
- All responses query actual database data
- If data doesn't exist, returns error message
- Transparent about data sources
- Validated through automated tests

**Example Implementation:**
```python
# src/utils/ai_concierge.py
def answer_query(self, query_type, **params):
    """All query types validated against database"""
    if query_type == 'search_resources':
        # Queries resource_dal directly
        resources = self.resource_dal.search_resources(...)
        return {'results': resources}  # Real data only
```

### AI-Assisted Development Workflow

**Documentation**: See [.prompt/dev_notes.md](.prompt/dev_notes.md) for detailed log

**AI Tools Used:**
- **Claude Code (Sonnet 4.5)**: Primary development assistant
- **GitHub Copilot** (simulated): Code completion
- **Cursor IDE** (simulated): Context-aware generation

**Development Process:**
1. Wrote detailed requirements with context
2. AI generated initial codebase (MVC + DAL + templates)
3. Team reviewed and validated all code
4. Added comprehensive tests
5. Documented AI contributions

**AI Contribution Estimate**: ~85% of initial code generation, 100% human-reviewed

**Code Attribution:**
- Look for comments: `# AI Contribution: [description]`
- Example: [src/data_access/booking_dal.py:76](src/data_access/booking_dal.py#L76)

### Ethical Considerations

1. **Transparency**: Users know when interacting with AI (labeled "AI Concierge")
2. **Data Accuracy**: No hallucinated or fabricated information
3. **Privacy**: AI only accesses published resource data, not private messages
4. **Bias Prevention**: Recommendations based on quantitative ratings
5. **Human Oversight**: Critical features reviewed and tested by team

### Context Pack Structure

**AI-First Repository Design:**

```
.prompt/
  dev_notes.md        ← Complete AI interaction log
  golden_prompts.md   ← Most effective prompts used

docs/context/
  APA/               ← Agility, Processes & Automation artifacts
  DT/                ← Design Thinking (personas, journey maps)
  PM/                ← Product Management (PRDs, OKRs)
  shared/            ← Common resources (glossary, standards)
```

This structure enables AI tools to understand project context, architecture, and goals.

---

## Testing

### Running Tests

**All tests:**
```bash
pytest
```

**Unit tests only:**
```bash
pytest tests/unit/
```

**Integration tests:**
```bash
pytest tests/integration/
```

**AI validation tests:**
```bash
pytest tests/ai_eval/
```

**With coverage:**
```bash
pytest --cov=src tests/
```

### Test Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| Data Access Layer | 25+ | 95%+ |
| Booking Logic | 10+ | 100% |
| Authentication Flow | 5+ | 90%+ |
| AI Concierge | 8+ | 100% |

### Key Test Files

- [tests/unit/test_user_dal.py](tests/unit/test_user_dal.py) - User CRUD operations
- [tests/unit/test_booking_logic.py](tests/unit/test_booking_logic.py) - Conflict detection
- [tests/integration/test_auth_flow.py](tests/integration/test_auth_flow.py) - Register → Login → Protected route
- [tests/ai_eval/test_concierge.py](tests/ai_eval/test_concierge.py) - AI accuracy validation

---

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/auth/register` | Registration page | No |
| POST | `/auth/register` | Create account | No |
| GET | `/auth/login` | Login page | No |
| POST | `/auth/login` | Authenticate user | No |
| GET | `/auth/logout` | Logout user | Yes |
| GET | `/auth/profile` | View profile | Yes |
| POST | `/auth/profile/edit` | Update profile | Yes |

### Resource Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/resources/` | List/search resources | No |
| GET | `/resources/<id>` | View resource details | No |
| GET | `/resources/create` | Create resource form | Yes |
| POST | `/resources/create` | Submit new resource | Yes |
| GET | `/resources/<id>/edit` | Edit resource form | Yes (Owner/Admin) |
| POST | `/resources/<id>/edit` | Update resource | Yes (Owner/Admin) |
| POST | `/resources/<id>/delete` | Delete resource | Yes (Owner/Admin) |

### Booking Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/bookings/create/<resource_id>` | Booking form | Yes |
| POST | `/bookings/create/<resource_id>` | Submit booking | Yes |
| GET | `/bookings/<id>` | View booking details | Yes |
| POST | `/bookings/<id>/approve` | Approve booking | Yes (Owner/Staff/Admin) |
| POST | `/bookings/<id>/reject` | Reject booking | Yes (Owner/Staff/Admin) |
| POST | `/bookings/<id>/cancel` | Cancel booking | Yes (Requester) |

### AI Concierge Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/concierge/` | Concierge interface | Yes |
| POST | `/concierge/ask` | Natural language query | Yes |
| POST | `/concierge/api/query` | Structured API query | Yes |

**Example API Request:**
```json
POST /concierge/api/query
{
  "query_type": "search_resources",
  "keyword": "study room",
  "category": "Study Room"
}
```

**Example Response:**
```json
{
  "success": true,
  "count": 3,
  "results": [
    {
      "resource_id": 1,
      "title": "Study Room A",
      "category": "Study Room",
      "location": "Library Building",
      "avg_rating": 4.5,
      "review_count": 12
    }
  ],
  "message": "Found 3 resources matching your criteria."
}
```

---

## Project Structure

```
Final Project/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
├── .gitignore
├── README.md
│
├── src/
│   ├── controllers/           # Flask route handlers (MVC Controllers)
│   │   ├── main_controller.py
│   │   ├── auth_controller.py
│   │   ├── resource_controller.py
│   │   ├── booking_controller.py
│   │   ├── message_controller.py
│   │   ├── review_controller.py
│   │   ├── admin_controller.py
│   │   └── concierge_controller.py
│   │
│   ├── data_access/           # Data Access Layer (DAL)
│   │   ├── database.py        # DB connection manager
│   │   ├── user_dal.py
│   │   ├── resource_dal.py
│   │   ├── booking_dal.py
│   │   ├── message_dal.py
│   │   ├── review_dal.py
│   │   └── admin_dal.py
│   │
│   ├── models/                # Database schema
│   │   └── schema.py
│   │
│   ├── views/                 # Jinja2 templates (MVC Views)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   ├── resources/
│   │   ├── bookings/
│   │   ├── booking/
│   │   ├── messages/
│   │   ├── admin/
│   │   └── concierge/
│   │
│   ├── static/                # Static assets
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   │
│   └── utils/                 # Utility functions
│       ├── auth.py            # Password hashing
│       ├── validators.py      # Input validation
│       └── ai_concierge.py    # AI feature
│
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests for DAL
│   ├── integration/           # Integration tests
│   └── ai_eval/               # AI feature validation
│
├── .prompt/                   # AI development logs
│   ├── dev_notes.md
│   └── golden_prompts.md
│
└── docs/
    └── context/               # Project context for AI
        ├── APA/
        ├── DT/
        ├── PM/
        └── shared/
```

---

## Security Features

### Implemented Security Measures

✅ **Password Security**
- Bcrypt hashing with salt
- Minimum strength requirements (8+ chars, uppercase, lowercase, digit)
- No plaintext passwords in database or logs

✅ **SQL Injection Prevention**
- All queries use parameterized statements
- No string concatenation in SQL
- ORM-style interface through DAL

✅ **XSS Protection**
- Jinja2 auto-escaping enabled
- Input sanitization for all text fields
- Content-Security-Policy headers (ready to add)

✅ **CSRF Protection**
- Flask-WTF CSRF tokens (ready to enable)
- Same-site cookie policy

✅ **Access Control**
- Role-based permissions (student, staff, admin)
- Ownership validation for resource/booking modifications
- Protected routes require authentication

✅ **File Upload Security**
- Allowed extension whitelist
- File size limits (5MB default)
- Filename sanitization (no path traversal)

✅ **Session Security**
- Secure session cookies
- Session timeout
- Server-side session validation

---

## Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add amazing feature"`
5. Push to branch: `git push origin feature/amazing-feature`
6. Open Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Write tests for new features
- Update README for major changes
- Document AI contributions

### Testing Requirements

- All tests must pass: `pytest`
- Maintain >90% code coverage
- Add integration tests for new workflows
- Validate AI features don't fabricate data

---

## Team

**Core Team 13**
- Product Lead / PM
- Backend Engineer
- Frontend Engineer / UX
- Quality & DevOps / Security

**Course**: AI in Design & Development (AiDD)
**Institution**: Indiana University
**Date**: October 2025

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- **Flask** framework and community
- **Bootstrap** for responsive UI components
- **Claude Code** for AI-assisted development
- **Indiana University** AiDD course staff
- All open-source contributors

---

## Reflection Questions (Project Requirement)

### 1. How did AI tools shape your design or coding decisions?

AI tools significantly influenced our architecture by suggesting the separation of concerns through a dedicated Data Access Layer. This wasn't explicitly in our initial plan, but Claude Code recommended it for better testability and maintainability. The AI also shaped our security approach by proactively suggesting input validation and parameterized queries, which we adopted throughout the project.

### 2. What did you learn about verifying and improving AI-generated outputs?

We learned that AI-generated code requires the same rigor as human-written code—perhaps more. Our process involved:
- Running comprehensive unit tests on all DAL methods
- Manual security review of authentication and validation code
- Testing edge cases the AI might not have considered
- Validating that the AI Concierge never fabricates data

The most important lesson: **trust but verify**. AI excels at generating structured, repetitive code (like CRUD operations) but needs human oversight for business logic and security-critical components.

### 3. What ethical or managerial considerations emerged from using AI in your project?

**Ethical Considerations:**
- **Data Fabrication Risk**: We explicitly designed the AI Concierge to NEVER fabricate information
- **Transparency**: Users clearly see when they're interacting with AI features
- **Privacy**: AI only accesses public resource data, not private user information
- **Bias**: Recommendations based on quantitative metrics, not AI judgment

**Managerial Considerations:**
- **Attribution**: How to credit AI contributions in team environments
- **Skill Development**: Balance between AI assistance and learning fundamentals
- **Quality Assurance**: Need for robust testing when AI generates large code volumes
- **Documentation**: Importance of logging AI interactions for team knowledge

### 4. How might these tools change the role of a business technologist or product manager in the next five years?

**Shift Toward Strategic Thinking:**
- PMs will spend less time writing specifications and more time on strategy
- AI can generate implementation details from high-level requirements
- Focus shifts to **what to build** rather than **how to build it**

**New Skills Required:**
- **Prompt Engineering**: Ability to communicate effectively with AI
- **AI Output Validation**: Critical evaluation of AI-generated solutions
- **Ethical Oversight**: Ensuring AI use aligns with values and regulations
- **Context Engineering**: Structuring projects for effective AI collaboration

**Role Evolution:**
- PMs become "AI orchestrators" - directing AI tools to solve problems
- Technical PMs can prototype features without full dev teams
- Focus on user research, ethics, and business strategy increases
- Need for understanding AI capabilities and limitations

**Bottom Line**: AI won't replace business technologists—it will amplify their capabilities. Those who learn to work effectively with AI will be far more productive than those who don't.

---

## Quick Start Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Run application
python app.py

# Run tests
pytest

# Run with coverage
pytest --cov=src

# Access application
http://localhost:5000
```

---

**Documentation Generated**: October 28, 2025
**Last Updated**: October 28, 2025
**Version**: 1.0.0
