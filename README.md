**Application architecture**


|   Django Admin UI         |
|---------------------------|
| - Add Power BI iframe     |
| - Assign report ID        |
| - Define pages            |
| - Import filters via Excel|
+------------+--------------+
             |
             v
+---------------------------+
|   Metadata Database       |
|---------------------------|
| - reports table           |
|    report_id, iframe_url, page_names |
| - filters table           |
|    report_id, filter_label, column_name, allowed_values |
+------------+--------------+
             |
             v
+---------------------------+
| Python Export Service     |
|---------------------------|
| - API endpoint: /export   |
| - Validates filters against DB |
| - Builds filtered Power BI URL |
| - Headless browser renders report |
| - Captures PNG / multi-page PDF |
| - Worker queue & caching support |
+------------+--------------+
             |
             v
+---------------------------+
| Front-End / CMS / Desktop |
|---------------------------|
| - Drupal / WordPress      |
| - Desktop app (Electron / PyQt) |
| - Fetch filter options via API |
| - Select filters & page   |
| - Click "Download PNG / Preview" |
+---------------------------+



**Technology stack**

Admin UI	Django, Python, pandas/openpyxl
Export API	Python, FastAPI/Flask, Selenium/Playwright, Chrome/Chromium
Database	SQLite (dev), PostgreSQL/MySQL (prod)
Worker queue (optional)	Celery + Redis
Front-end / CMS	HTML/CSS/JS, Drupal/WordPress integration, optional desktop app (Electron / PyQt)
Deployment	Docker / Docker Compose (internal server)
Filter input	Excel or CSV


**Project Goal**
This project provides a robust, internal solution for dynamically exporting Power BI dashboards as images, with:

Cross-platform front-end support

Excel-driven filter management

Admin UI for easy report management

Docker-based deployment for internal servers

Scalable and future-proof design


**actions made**

-initiated git repo

--installed django framework--
run server: python manage.py runserver

--installed pandas--

Reading Excel or CSV filter metadata

Cleaning and validating filter data

Preparing it for database storage

Enabling dynamic, flexible filters without hardcoding


**Next Actions**
Add ONE report manually

Add ONE page

Add ONE filter


**Database Architecture**

┌─────────────────────────────────────────────────────┐
│  Your FastAPI Code (routers/reports.py)            │
│  db.query(Report).all()                            │
└────────────────────┬────────────────────────────────┘
                     │
         ╔═══════════╩═══════════╗
         ║   SQLAlchemy (ORM)    ║  ← Translates Python → SQL
         ║  Converts queries      ║
         ║  Maps results to objs  ║
         ╚═══════════╦═══════════╝
                     │
┌────────────────────▼────────────────────────────────┐
│  SQLite Database (db.sqlite3)                       │
│  SELECT * FROM reports_report;                      │
└─────────────────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│        Your FastAPI Route                │
│  @router.get("/reports")                │
│  def get_reports(db: Session = ...)     │
└────────────────┬─────────────────────────┘
                 │ Depends(get_db)
                 ↓
┌──────────────────────────────────────────┐
│    database.py                           │
│  1. Finds db.sqlite3                     │
│  2. Creates engine (connection pool)    │
│  3. Creates SessionLocal factory         │
│  4. get_db() yields sessions to routes  │
└────────────────┬─────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│    Django's db.sqlite3                   │
│  - reports_report table                  │
│  - reports_filter table                  │
│  - reports_pages table                   │
└──────────────────────────────────────────┘


FastAPI route calls get_db()
   ↓
2. get_db() creates: db = SessionLocal()
   ↓
3. get_db() yields db to the route
   ↓
4. Route runs and uses db to query the database
   ↓
5. Route finishes
   ↓
6. get_db() resumes and closes the database: db.close()
   ↓
7. Session is cleaned up, ready for next request

**Script for start up db**

import app.core.database import SessionLocal
db = SessionLocal()
try:
    print(db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
finally:
    db.close()


***Specific Topics***
---------------------

**How db is attached to routes**
Why dependency injection matters

FastAPI:

tracks lifecycle per request

isolates concurrent requests

avoids shared state

This is not optional in real systems.

----------------------------------
db: Session
This is:

a DB connection manager

a transaction boundary

a cursor provider

----------------------------------
text("SELECT report_id, title FROM reports_report")
Why required?

Because SQLAlchemy:

must distinguish SQL from Python strings

validates parameters

prevents SQL injection

----------------------------------

Threading & Concurrency (CRITICAL)

When 100 users hit /api/reports:

Each request gets:

its own DB session

its own transaction

Sessions are never shared

SQLite threading is respected

---------------------------------

The Pattern (Memorize This)
SQL → rows → loop → dicts → JSON


You will repeat this pattern in:

/reports

/pages/{report_id}

/filters/{report_id}

---------------------------------
**Apply smoke tests**
------------------------

# start FastAPI (from fast_api/)
uvicorn main:app --reload --port 8001

# request filters for report 1
curl http://127.0.0.1:8001/api/filters/1

# request pages for report 1 
curl http://127.0.0.1:8001/api/pages/1

# start FastAPI (if not already)
uvicorn main:app --reload --port 8001

# request the endpoint
curl http://127.0.0.1:8001/api/reports/





----------------------------------------
***IMPORTANT: Freeze the API Contract (Do This Now)***

Importance of API Contracts in System Design
API contracts play a crucial role in system design, providing a clear and formalized definition of the interactions between different components of a system. Here are some key reasons why API contracts are important:

1. Clarity & Consistency

Clear Specs: Define endpoints, parameters, responses, and errors clearly for a shared understanding.
Consistency: Ensure uniform behavior across versions and implementations.
2. Parallel Development

Team Collaboration: Frontend and backend teams can work independently using the contract.
Fewer Dependencies: Reduces the need for teams to wait on each other.
3. Interoperability

Standardization: Encourages common protocols and data formats.
Easy Integration: Simplifies connecting with third-party or external systems.
4. Testing & Validation

Automated Testing: Validates that APIs follow the contract.
Mocking: Enables early testing with mock APIs.
5. Error Handling & Reliability

Defined Errors: Clear error formats help clients handle issues better.
Better Reliability: Prevents miscommunication and reduces system failures.

Before moving forward, freeze your response shapes.

Example (filters):

{
  "filters": [
    {
      "label": "Year",
      "column": "year",
      "allowed_values": [2022, 2023],
      "default": 2023
    }
  ]
}


Why this matters:

Frontend depends on this

Export service depends on this

Changing later causes bugs

