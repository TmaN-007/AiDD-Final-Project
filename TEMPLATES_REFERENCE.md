# Templates Quick Reference Guide

## Summary
Created 14 fully-functional HTML templates for the Campus Resource Hub Flask application.
Total: 2,651 lines of template code with Bootstrap 5, Jinja2, and JavaScript.

## Template File Paths

### Authentication (3 templates)
- `/src/views/auth/login.html` - User login form
- `/src/views/auth/register.html` - User registration form
- `/src/views/auth/profile.html` - User profile management

### Dashboard (1 template)
- `/src/views/dashboard.html` - Main user dashboard

### Resources (4 templates)
- `/src/views/resources/list.html` - Browse resources with filters
- `/src/views/resources/view.html` - Resource detail page
- `/src/views/resources/create.html` - Create new resource
- `/src/views/resources/edit.html` - Edit existing resource

### Bookings (2 templates)
- `/src/views/bookings/create.html` - Create booking
- `/src/views/bookings/view.html` - Booking detail and management

### Messages (3 templates)
- `/src/views/messages/inbox.html` - Message inbox list
- `/src/views/messages/thread.html` - Message conversation view
- `/src/views/messages/compose.html` - Compose new message

### Admin (1 template)
- `/src/views/admin/dashboard.html` - Admin dashboard with stats

## Required URL Routes

Each template expects specific Flask route endpoints. Ensure your Flask app defines:

### Auth Routes
- `auth.login` - GET/POST
- `auth.register` - GET/POST
- `auth.profile` - GET/POST
- `auth.change_password` - POST
- `auth.forgot_password` - GET/POST

### Dashboard Routes
- `dashboard.index` or similar - GET

### Resource Routes
- `resources.list` - GET
- `resources.view` - GET (with resource_id parameter)
- `resources.create` - GET/POST
- `resources.edit` - GET/POST (with resource_id parameter)
- `resources.delete` - POST (with resource_id parameter)
- `resources.add_review` - POST (with resource_id parameter)

### Booking Routes
- `bookings.list` - GET
- `bookings.pending` - GET
- `bookings.create` - GET/POST (with resource_id parameter)
- `bookings.view` - GET (with booking_id parameter)
- `bookings.approve` - POST (with booking_id parameter)
- `bookings.reject` - POST (with booking_id parameter)
- `bookings.cancel` - POST (with booking_id parameter)

### Message Routes
- `messages.inbox` - GET (optional folder parameter)
- `messages.thread` - GET (with thread_id parameter)
- `messages.reply` - POST (with thread_id parameter)
- `messages.compose` - GET/POST
- `messages.archive_thread` - POST (with thread_id parameter)
- `messages.unarchive_thread` - POST (with thread_id parameter)
- `messages.delete_thread` - POST (with thread_id parameter)

### Admin Routes
- `admin.dashboard` - GET
- `admin.users` - GET
- `admin.resources` - GET
- `admin.bookings` - GET
- `admin.logs` - GET
- `admin.user_detail` - GET (with user_id parameter)

## Template Context Variables Expected

### Login Template
- `error` - Error message (optional)

### Register Template
- `error` - Error message (optional)

### Profile Template
- `current_user` - User object with properties:
  - `name`, `email`, `role`, `department`, `created_at`

### Dashboard Template
- `current_user` - User object
- `my_resources` - List of resources
- `my_bookings` - List of bookings
- `bookings_for_my_resources` - List of bookings for owner's resources
- `upcoming_bookings` - List of future bookings

### Resource List Template
- `resources` - List of resource objects
- `request.args` - Query parameters (keyword, category, location)

### Resource View Template
- `resource` - Resource object with:
  - `id`, `title`, `description`, `category`, `location`, `capacity`, `status`, `owner_id`, `image_url`, `owner`
- `current_user` - Current user object
- `reviews` - List of review objects
- `is_owner` - Boolean (current user is resource owner)

### Resource Create/Edit Templates
- `resource` - Resource object (edit only, for pre-population)
- `error` - Error message (optional)

### Booking Create Template
- `resource` - Resource object
- `error` - Error message (optional)

### Booking View Template
- `booking` - Booking object with:
  - `id`, `status`, `resource`, `user`, `start_datetime`, `end_datetime`, `notes`
- `current_user` - Current user object
- `is_owner` - Boolean (current user is resource owner)
- `is_booker` - Boolean (current user made the booking)

### Messages Inbox Template
- `threads` - List of message threads with:
  - `id`, `other_user`, `last_message`, `unread_count`
- `request.args` - Query parameters (folder)

### Messages Thread Template
- `thread_id` - Thread ID
- `other_user` - Other participant object
- `messages` - List of message objects
- `current_user` - Current user object
- `is_archived` - Boolean

### Messages Compose Template
- `users` - List of available recipients
- `error` - Error message (optional)

### Admin Dashboard Template
- `stats` - Dictionary with keys:
  - `total_users`, `total_resources`, `total_bookings`, `pending_bookings`
  - `resources_available`, `resources_maintenance`, `resources_unavailable`
  - `bookings_pending`, `bookings_approved`, `bookings_rejected`
  - `users_students`, `users_staff`, `users_admins`
- `pending_bookings` - List of pending booking objects
- `recent_activity` - List of activity logs
- `recent_users` - List of recent user objects

## Bootstrap 5 Classes Used

Primary classes utilized:
- `.container`, `.container-fluid` - Layout containers
- `.row`, `.col-*` - Grid system
- `.card` - Content containers
- `.form-control`, `.form-select` - Form inputs
- `.btn`, `.btn-primary`, `.btn-outline-*` - Buttons
- `.badge` - Status indicators
- `.table` - Data tables
- `.alert` - Alert messages
- `.modal` - Modal dialogs
- `.d-flex`, `.justify-content-*`, `.align-items-*` - Flexbox utilities
- `.mb-*`, `.mt-*`, `.p-*` - Spacing utilities
- `.text-muted`, `.text-center` - Text utilities
- `.bg-light`, `.shadow`, `.shadow-sm` - Styling utilities

## Jinja2 Features Used

- `{% extends "base.html" %}` - Template inheritance
- `{% block title %}`, `{% block content %}` - Blocks
- `{% if condition %} ... {% endif %}` - Conditionals
- `{% for item in list %} ... {% endfor %}` - Loops
- `{{ variable }}` - Variable output
- `{{ function() }}` - Function calls
- `|` filters: `|upper`, `|length`, `|strftime`, `|selectattr`
- `url_for()` - URL generation
- Comments: `{# comment #}`

## JavaScript Included

Features with client-side JavaScript:
1. **Form Validation** - Bootstrap 5 validation pattern
2. **Password Matching** - Register template password confirmation
3. **Duration Calculation** - Booking form calculates booking length
4. **Character Counter** - Compose message form
5. **Auto-scroll** - Message thread scrolls to bottom

## Bootstrap Icons Used

Icons from Bootstrap Icons library (bi-):
- `bi-inbox`, `bi-archive`, `bi-trash` - Messages
- `bi-calendar-event`, `bi-calendar-plus`, `bi-calendar-check` - Bookings/Dates
- `bi-people`, `bi-user` - Users
- `bi-box-seam` - Resources
- `bi-pencil`, `bi-pencil-square` - Edit
- `bi-plus`, `bi-check-circle`, `bi-x-circle` - Actions
- `bi-geo-alt` - Location
- `bi-tag` - Categories
- `bi-clock` - Time
- `bi-star`, `bi-star-fill` - Ratings
- `bi-info-circle` - Information
- `bi-send` - Send
- `bi-arrow-left` - Navigation

## Form Validation Attributes

HTML5 validation used:
- `required` - Field is mandatory
- `type="email"` - Email validation
- `type="password"` - Password input
- `type="datetime-local"` - Date/time input
- `type="number"` - Number input
- `type="url"` - URL validation
- `minlength="n"` - Minimum character length
- `maxlength="n"` - Maximum character length
- `min="n"`, `max="n"` - Number range
- `pattern="regex"` - Regex validation (if needed)

## Color Scheme

Status colors used consistently:
- Green (#198754) - Approved, Success
- Yellow (#ffc107) - Pending, Warning
- Red (#dc3545) - Rejected, Danger
- Gray (#6c757d) - Cancelled, Secondary
- Blue (#007bff) - Primary actions
- Light gray (#e9ecef) - Backgrounds

## Responsive Design

- Mobile-first approach
- Breakpoints: xs, sm (576px), md (768px), lg (992px), xl (1200px)
- Grid column classes: `col-md-6`, `col-lg-8`, etc.
- Flexible tables with `.table-responsive`
- Responsive forms

## Accessibility Features

- Semantic HTML structure
- Form labels with `for` attribute
- Modal ARIA labels
- Button types properly specified
- Color coding combined with text labels
- Good contrast ratios
- Readable font sizes

## Dependencies

Required:
- Bootstrap 5 (CSS & JS)
- Bootstrap Icons
- Flask with Jinja2 templating
- Python datetime module

Optional (but recommended):
- jQuery (if using old Bootstrap features)
- Font Awesome (alternative to Bootstrap Icons)

## Base Template Requirements

Your `base.html` should include:
- Bootstrap 5 CSS
- Bootstrap 5 JS
- Bootstrap Icons CSS
- Navigation menu with links
- CSRF token in forms (Flask-WTF)
- Flash message display
- Footer (optional)
