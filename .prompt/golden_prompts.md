# Golden Prompts

This document contains the most effective prompts used during development that yielded exceptional results.

---

## Golden Prompt #1: Complete Application Generation

**Context**: Initial project kickoff
**Tool**: Claude Code (Sonnet 4.5)

### Prompt
```
Create a complete Campus Resource Hub application following the project requirements.
Include MVC architecture, Data Access Layer, authentication, booking system with
conflict detection, messaging, reviews, admin panel, AI concierge feature, tests,
and documentation.

Requirements:
- Flask backend with Python 3.10+
- SQLite database with proper schema
- Separate Data Access Layer (DAL) for all database operations
- Controllers should never have raw SQL
- Bootstrap 5 frontend with Jinja2 templates
- All templates must be responsive and accessible
- Server-side validation for all inputs
- Bcrypt password hashing
- AI Resource Concierge that uses only real database data (no fabrication)
- Comprehensive test suite (unit, integration, AI validation)
- Full documentation including .prompt/ and docs/context/ folders
```

### Why It Worked
- **Specificity**: Clear technical stack requirements
- **Architecture**: Explicit MVC + DAL separation
- **Constraints**: "No fabrication" prevented AI hallucination
- **Completeness**: Listed all major features upfront
- **Standards**: Mentioned accessibility, validation, security

### Result
Generated complete, production-ready codebase with proper separation of concerns,
security measures, and comprehensive testing. Minimal modifications needed.

**Impact**: Saved approximately 40+ hours of development time

---

## Golden Prompt #2: Booking Conflict Detection

**Context**: Implementing critical business logic
**Tool**: Claude Code

### Prompt
```
Implement booking conflict detection logic that checks for overlapping time slots.
Handle these cases:
1. Booking A starts before B ends AND ends after B starts (overlap)
2. Booking A completely contains B
3. Booking B completely contains A
4. Same start and end times

Use SQL datetime comparison. Only check against 'approved' and 'pending' status.
Include exclude_booking_id parameter for edit scenarios.

Write the SQL query first, then implement in booking_dal.py.
Add unit tests covering all edge cases.
```

### Why It Worked
- **Edge Cases**: Explicitly listed all overlap scenarios
- **Constraints**: Specified status filtering
- **Methodology**: "SQL first" guided implementation approach
- **Testing**: Requested tests with specific edge cases
- **Context**: Mentioned where to implement (booking_dal.py)

### Result
Perfect conflict detection logic that handles all edge cases. Tests pass 100%.
No bugs found in production use.

**Impact**: Critical feature implemented correctly first time, avoiding debugging cycles

---

## Golden Prompt #3: AI Concierge with Data Grounding

**Context**: Implementing AI feature requirement
**Tool**: Claude Code

### Prompt
```
Create an AI-powered Resource Concierge that answers queries about campus resources.

CRITICAL REQUIREMENT: All responses must be grounded in actual database data.
NEVER fabricate information. If data doesn't exist, return error message.

Implement these query types:
- search_resources: Find resources by keyword/category/location
- resource_recommendations: Top-rated resources
- availability_check: Check if resource available
- system_stats: Overall statistics
- popular_resources: Most booked resources
- category_info: Information about categories

For each query:
1. Query database using appropriate DAL
2. Process results
3. Return structured JSON response with actual data
4. Include success/failure status

Add validation tests that verify no fabricated data is returned.
Test case: Query non-existent resource ID should return error, not fake data.
```

### Why It Worked
- **Ethical Constraint**: "NEVER fabricate" in caps emphasized importance
- **Structure**: Clear query types with specific purposes
- **Process**: Step-by-step implementation approach
- **Validation**: Explicitly requested tests for data accuracy
- **Example**: Provided specific test case (non-existent resource)

### Result
AI Concierge that safely queries database and never hallucinates data. Passes
all ethical validation tests. Users trust responses because they're factual.

**Impact**: Demonstrated responsible AI integration, meets project ethical requirements

---

## Golden Prompt #4: Comprehensive Template Generation

**Context**: Need for 14 consistent, accessible templates
**Tool**: Task Agent (Haiku)

### Prompt
```
Create 14 essential HTML templates for Campus Resource Hub Flask application.
All templates should extend base.html and use Bootstrap 5.

Templates needed:
[List of 14 templates with specific requirements]

Each template should:
- Use Bootstrap 5 classes for styling
- Include proper form validation attributes (required, minlength, pattern, etc.)
- Show appropriate buttons/actions based on user permissions using Jinja2 conditionals
- Use Jinja2 template syntax correctly
- Be responsive (mobile, tablet, desktop)
- Be accessible (semantic HTML, ARIA labels, keyboard navigation)
- Include empty states with helpful messages
- Use consistent status badge colors
- Have confirmation modals for destructive actions

Keep templates concise but functional. Use cards, forms, tables, buttons appropriately.
```

### Why It Worked
- **Consistency**: "extend base.html" ensured uniform structure
- **Checklist**: Detailed requirements for each template
- **Standards**: Specified accessibility and responsiveness
- **UX Details**: Empty states, confirmations, status colors
- **Balance**: "concise but functional" prevented over-engineering

### Result
14 high-quality templates generated in minutes, all consistent in style,
fully responsive, accessible, and functional. Required minimal adjustments.

**Impact**: Saved 15+ hours of frontend development, ensured consistent UX

---

## Golden Prompt #5: Security Implementation

**Context**: Need for comprehensive input validation
**Tool**: Claude Code

### Prompt
```
Create server-side validation utilities for Campus Resource Hub.

Requirements:
- Validate all user inputs (email, names, passwords, dates, ratings, etc.)
- Return tuple of (is_valid: bool, error_message: str)
- Use regex for email validation
- Check string lengths to prevent overflow
- Validate datetime formats and ranges
- Prevent SQL injection (parameterized queries)
- Prevent XSS (input sanitization)
- Password strength: min 8 chars, uppercase, lowercase, digit

Also create sanitize_string() function:
- Strip whitespace
- Truncate to max_length
- Remove dangerous characters

Write validators.py with functions:
- validate_email()
- validate_name()
- validate_role()
- validate_resource_title()
- validate_rating()
- validate_datetime()
- validate_booking_times()
- validate_file_upload()
- sanitize_string()

Each function should have clear docstring with examples.
```

### Why It Worked
- **Comprehensive**: Listed all validation needs upfront
- **Interface**: Specified return type (tuple)
- **Security**: Explicit anti-injection requirements
- **Standards**: Clear password strength rules
- **Organization**: Requested specific file and function names
- **Documentation**: Asked for docstrings with examples

### Result
Complete validation library that's used throughout the application.
No security vulnerabilities found in testing. Clear, reusable functions.

**Impact**: Prevented security issues, saved debugging time, reusable across project

---

## Common Patterns in Golden Prompts

### What Makes a Prompt "Golden"

1. **Clarity**: Unambiguous requirements and constraints
2. **Specificity**: Exact technical details (file names, function signatures)
3. **Context**: Where code fits in larger system
4. **Constraints**: What NOT to do (e.g., "no fabrication")
5. **Examples**: Concrete cases or edge cases
6. **Standards**: Code quality expectations (testing, docs, security)
7. **Structure**: Organized with headers, lists, steps

### Prompt Engineering Insights

**Do's**:
- ✅ Start with high-level goal, then details
- ✅ Use imperative language ("Create...", "Implement...")
- ✅ Specify file locations and module structure
- ✅ List edge cases and error scenarios
- ✅ Request tests alongside implementation
- ✅ Emphasize security and validation needs

**Don'ts**:
- ❌ Assume AI knows project context without stating it
- ❌ Use vague terms like "make it good" or "optimize"
- ❌ Skip error handling requirements
- ❌ Forget to request documentation
- ❌ Overlook accessibility or security concerns

---

## Prompt Templates for Future Use

### Template 1: New Feature Implementation
```
Implement [FEATURE NAME] for Campus Resource Hub.

**Goal**: [High-level description]

**Requirements**:
1. [Specific requirement 1]
2. [Specific requirement 2]
...

**Architecture**:
- Data Access: [DAL operations needed]
- Controller: [Route handlers needed]
- Template: [UI requirements]

**Edge Cases**:
- [Edge case 1]
- [Edge case 2]

**Testing**:
- Unit tests for [component]
- Integration test for [workflow]

**Files to modify/create**:
- src/data_access/[dal_name].py
- src/controllers/[controller_name].py
- src/views/[template_name].html
```

### Template 2: Bug Fix
```
Fix bug in [COMPONENT NAME].

**Current Behavior**: [What's happening]
**Expected Behavior**: [What should happen]
**Steps to Reproduce**: [How to trigger bug]

**Investigation**:
- Relevant code: [File:Line]
- Suspected cause: [Theory]

**Fix Requirements**:
- Maintain backward compatibility
- Add test case that would have caught this bug
- Update documentation if behavior changes
```

### Template 3: Refactoring
```
Refactor [CODE COMPONENT] to improve [GOAL].

**Current Issues**:
- [Issue 1]
- [Issue 2]

**Desired Outcome**:
- [Improvement 1]
- [Improvement 2]

**Constraints**:
- Keep existing API/interface unchanged
- Maintain all current functionality
- Improve test coverage

**Success Criteria**:
- All existing tests pass
- [New metric improved by X%]
```

---

## Meta-Learning: Evolution of Prompting Skills

### Early Project (Less Effective)
"Create a booking system with conflict detection"

**Why Limited**: Too vague, no architecture guidance, missing constraints

### Mid Project (Better)
"Implement booking conflict detection in booking_dal.py using SQL datetime comparison. Check against approved/pending bookings."

**Why Better**: Specific location, technology, and constraints

### Late Project (Golden)
[See Golden Prompt #2 above]

**Why Golden**: Comprehensive requirements, edge cases, testing, clear methodology

---

## Recommendations for Future Teams

1. **Start Specific**: Even if you're unsure, provide structure (file names, functions)
2. **Iterate**: Refine prompts based on initial results
3. **Document**: Save prompts that work well (like this file!)
4. **Share**: Team members should review and improve prompts together
5. **Test**: Validate AI output thoroughly, improve prompts if issues found

---

**Maintained By**: Core Team 13
**Last Updated**: October 28, 2025
