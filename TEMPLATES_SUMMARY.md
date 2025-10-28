# Campus Resource Hub - HTML Templates Summary

All 14 essential HTML templates have been successfully created for the Campus Resource Hub Flask application. Each template extends `base.html` and uses Bootstrap 5 for styling.

## Templates Created

### Authentication Templates (src/views/auth/)

#### 1. login.html
- Email and password input fields
- Remember me checkbox
- Form validation with error messages
- Link to registration and password reset pages
- Client-side form validation with Bootstrap styling

#### 2. register.html
- Full name, email, password fields
- Confirm password with real-time validation
- Role selection dropdown (student/staff/admin)
- Department input field
- Password strength requirements display
- Link to login page

#### 3. profile.html
- User profile display with avatar
- Account information display (email, role, department, member since)
- Edit profile modal dialog
- Change password modal dialog
- Security section with password change option

### Dashboard Template (src/views/)

#### dashboard.html
- Welcome message with user role and department
- Statistics cards showing:
  - My Resources count
  - My Bookings count
  - Pending Approvals count
  - Upcoming Bookings count
- Upcoming Bookings section with resource details
- Pending Approvals section with approval buttons
- My Resources section with add resource link
- My Recent Bookings section with status badges

### Resource Templates (src/views/resources/)

#### 1. list.html
- Search and filter form with:
  - Keyword search
  - Category dropdown filter
  - Location filter
- Resource cards displaying:
  - Image (or placeholder)
  - Title and description
  - Category and location
  - Capacity information
  - Status badge (Available/Maintenance/Unavailable)
  - View Details button
- Edit and Delete buttons for resource owners
- Delete confirmation modals
- Empty state message

#### 2. view.html
- Resource detail header with image
- Resource information (title, description, location, capacity, status)
- Category and status badges
- Owner information
- Sidebar with:
  - Book Now button (if available and not owner)
  - Resource information card
- Reviews section displaying:
  - Review author and date
  - Star ratings
  - Review comments
- Review form for non-owners with:
  - Star rating dropdown
  - Comment textarea
  - Submit button
- Delete resource modal for owners

#### 3. create.html
- Resource creation form with fields:
  - Title (required, min 3 chars)
  - Description (required, min 10 chars)
  - Category dropdown (classroom/lab/equipment/venue/other)
  - Location (required)
  - Capacity (required, 1-1000)
  - Status dropdown (available/maintenance/unavailable)
  - Image URL (optional)
- Form validation with error messages
- Cancel button linking back to resources list

#### 4. edit.html
- Pre-populated form with existing resource data
- Same fields as create.html
- Save Changes and Cancel buttons
- Maintains resource data in form fields

### Booking Templates (src/views/bookings/)

#### 1. create.html
- Resource details display card
- Booking form with:
  - Start date and time input (datetime-local)
  - End date and time input (datetime-local)
  - Additional notes textarea (optional)
  - Terms and conditions checkbox
- Dynamic duration display (calculated on input change)
- Booking information card with details about:
  - Booking status (pending approval)
  - Confirmation via email
  - Cancellation policy
  - Resource owner contact
- Minimum date set to today
- JavaScript for duration calculation

#### 2. view.html
- Status badge with color coding:
  - Pending (yellow)
  - Approved (green)
  - Rejected (red)
  - Cancelled (gray)
- Resource information section with:
  - Resource name and link
  - Category, location, capacity
- Booking schedule with:
  - Start and end datetime
  - Duration calculation and display
- User information (booked by, email)
- Additional notes display
- Created/updated timestamps
- Action buttons:
  - Approve/Reject (for resource owner on pending bookings)
  - Cancel (for booker on pending/approved bookings)
- Sidebar with:
  - Resource owner information
  - Status timeline with markers
- Reject booking modal with optional reason
- Cancel booking modal with confirmation

### Message Templates (src/views/messages/)

#### 1. inbox.html
- Sidebar with filter options:
  - Inbox view
  - Archived view
- Message thread list with:
  - User avatar
  - Participant name
  - Preview of last message
  - Date of last message
  - Unread message count badge
- Compose New button
- Empty state message when no messages

#### 2. thread.html
- Thread header with:
  - Participant name
  - Back to Inbox button
- Scrollable message display area showing:
  - Messages aligned by sender (sent/received styling)
  - Message timestamps
  - Message content
- Reply form with:
  - Textarea for reply content
  - Send button
  - Character counter
- Thread actions:
  - Archive/Restore button
  - Delete conversation button
- Sidebar with thread information:
  - Participant details (name, email, department)
  - Total message count
- Delete confirmation modal
- Auto-scroll to bottom on load

#### 3. compose.html
- Recipient selection dropdown with user list
- Message content textarea with:
  - Real-time character counter
  - Minimum 1 character validation
- Send Message and Cancel buttons
- Tips card with messaging guidelines

### Admin Templates (src/views/admin/)

#### dashboard.html
- Statistics cards showing:
  - Total Users
  - Total Resources
  - Total Bookings
  - Pending Bookings
- Pending Bookings table displaying:
  - Resource name
  - User name
  - Date
  - Status badge
  - Review button link
- Recent Activity section showing:
  - Activity description
  - Activity type badge
  - Timestamp
- Recent Users table with:
  - User name (linked)
  - Email
  - Role badge
  - Join date
- System Information card with:
  - Resources by status breakdown
  - Bookings by status breakdown
  - Users by role breakdown
- Management Actions buttons linking to:
  - User management
  - Resource management
  - Booking management
  - System logs

## Key Features Across All Templates

### Bootstrap 5 Styling
- Responsive grid layout
- Card components for content organization
- Form validation styling with visual feedback
- Badge components for status indicators
- Modal dialogs for confirmations and actions
- Table components with responsive wrappers
- Alert components for messages

### Form Validation
- HTML5 validation attributes (required, minlength, type, etc.)
- Bootstrap client-side validation styling
- JavaScript validation script included in forms
- Custom validation for password matching (register template)
- Duration calculation validation (booking form)

### Permission-Based UI
- Edit/Delete buttons only shown to resource owners
- Book Now button hidden for resource owners
- Review form hidden for resource owners
- Approve/Reject buttons only shown to resource owners
- Cancel button only shown to booking creator
- Admin-only management links

### User Experience Features
- Loading spinners and disabled buttons
- Empty state messages
- Confirmation modals for destructive actions
- Breadcrumb navigation
- Status badges with color coding
- Timestamps for created/updated information
- Unread message indicators
- Dynamic element display based on conditions

### Accessibility
- Semantic HTML structure
- Form labels properly associated with inputs
- ARIA labels for modal dialogs
- Button types correctly specified
- Color not used as sole indicator (badges include text)
- Sufficient contrast for readability

## Template Structure

All templates follow a consistent structure:
```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <!-- Page content using Bootstrap 5 -->
{% endblock %}
```

## File Locations

```
src/views/
├── auth/
│   ├── login.html
│   ├── register.html
│   └── profile.html
├── resources/
│   ├── list.html
│   ├── view.html
│   ├── create.html
│   └── edit.html
├── bookings/
│   ├── create.html
│   └── view.html
├── messages/
│   ├── inbox.html
│   ├── thread.html
│   └── compose.html
├── admin/
│   └── dashboard.html
└── dashboard.html
```

## Notes

- All templates use Jinja2 template syntax
- Forms include CSRF protection hooks (should be added in base.html)
- URLs use Flask's url_for() function for route generation
- Datetime fields use datetime-local input type for browser support
- JavaScript is included inline for form validation and interactions
- Bootstrap Icons (bi-) are used throughout for visual elements
- All color coding is intentional for status visualization
