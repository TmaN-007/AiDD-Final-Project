# Campus Resource Hub - Glossary

## Project Terms

**Campus Resource Hub**
- The full name of the application
- A web-based system for managing and booking campus resources

**Resource**
- Any bookable campus asset (study room, equipment, lab space, etc.)
- Has properties: title, description, category, location, capacity, status
- Lifecycle: draft → published → archived

**Booking**
- A reservation request for a resource
- Status flow: pending → approved/rejected → completed/cancelled
- Includes start time, end time, and notes

**Conflict Detection**
- System logic that prevents overlapping bookings
- Checks for time slot collisions
- Critical business logic for booking system

## User Roles

**Student**
- Default role for registered users
- Can browse resources, create bookings, and leave reviews
- Cannot approve bookings for others

**Staff**
- Elevated user role
- Can create resources and approve bookings
- Has access to resource management features

**Admin**
- Highest permission level
- Full system access including user management
- Can moderate content and view analytics

## Technical Terms

**MVC (Model-View-Controller)**
- Architectural pattern used in this project
- Model: Database schema and data models
- View: Jinja2 HTML templates
- Controller: Flask route handlers

**DAL (Data Access Layer)**
- Encapsulated database operations
- Separate module for each entity (UserDAL, ResourceDAL, etc.)
- Prevents SQL injection through parameterized queries

**Blueprint**
- Flask's modular routing system
- Each controller is a blueprint
- Enables organized, maintainable code structure

**Context Pack**
- AI-first repository structure
- Includes `.prompt/` and `docs/context/` folders
- Helps AI tools understand project architecture

## Database Terms

**Schema**
- Database table definitions
- Defined in `src/models/schema.py`
- 7 tables: users, resources, bookings, messages, reviews, admin_logs

**Foreign Key**
- Relationship between tables
- Ensures referential integrity
- Example: booking references resource_id

**Index**
- Database performance optimization
- Speeds up queries on frequently searched columns
- Applied to emails, dates, status fields

## AI Terms

**AI Concierge**
- AI-powered feature in the application
- Answers natural language queries about resources
- Grounded in real database data (no fabrication)

**Context Grounding**
- Ensuring AI responses use actual data
- Prevents hallucination/fabrication
- Validated through automated tests

**Golden Prompt**
- Highly effective AI prompt that yielded excellent results
- Documented in `.prompt/golden_prompts.md`
- Reusable for similar tasks

**Prompt Engineering**
- Crafting effective instructions for AI tools
- Key skill for AI-assisted development
- Improves with practice and documentation

## Security Terms

**bcrypt**
- Password hashing algorithm
- Used for secure password storage
- Industry standard, computationally expensive (prevents brute force)

**XSS (Cross-Site Scripting)**
- Security vulnerability where malicious scripts injected
- Prevented through Jinja2 auto-escaping
- Input sanitization

**SQL Injection**
- Attack where malicious SQL inserted through input
- Prevented through parameterized queries
- All queries use `?` placeholders

**CSRF (Cross-Site Request Forgery)**
- Attack where unauthorized commands submitted
- Prevented through CSRF tokens (Flask-WTF)
- Validates request origin

**Server-Side Validation**
- Input validation performed on backend
- Never trust client-side validation alone
- Implemented in `src/utils/validators.py`

## Status Values

### Resource Status
- `draft` - Resource created but not visible to users
- `published` - Resource available for booking
- `archived` - Resource no longer available

### Booking Status
- `pending` - Awaiting approval from resource owner/staff
- `approved` - Booking confirmed
- `rejected` - Booking denied
- `cancelled` - Requester cancelled booking
- `completed` - Booking finished successfully

### User Roles
- `student` - Standard user
- `staff` - Resource managers
- `admin` - System administrators

## Flask Terms

**Session**
- Server-side user state storage
- Stores user_id, user_name, user_role
- Cleared on logout

**Flash Message**
- Temporary notification to user
- Categories: success, danger, warning, info
- Displayed once, then cleared

**Template**
- HTML file with Jinja2 syntax
- Located in `src/views/`
- Extends `base.html` for consistent layout

**Static Files**
- CSS, JavaScript, images
- Located in `src/static/`
- Served directly by Flask

## Project Management Terms

**PRD (Product Requirements Document)**
- Detailed specification of features
- Guides development work
- Living document that evolves

**Acceptance Criteria**
- Conditions that must be met for feature to be complete
- Used in testing
- Example: "User can register and log in"

**Test Coverage**
- Percentage of code executed by tests
- Goal: >90% for this project
- Measured with pytest-cov

## Common Abbreviations

- **CRUD** - Create, Read, Update, Delete
- **API** - Application Programming Interface
- **UI** - User Interface
- **UX** - User Experience
- **DB** - Database
- **SQL** - Structured Query Language
- **HTML** - HyperText Markup Language
- **CSS** - Cascading Style Sheets
- **JS** - JavaScript
- **AI** - Artificial Intelligence
- **LLM** - Large Language Model
- **ORM** - Object-Relational Mapping

---

**Note**: This glossary is maintained for both human developers and AI tools to ensure consistent understanding of project terminology.

**Last Updated**: October 28, 2025
