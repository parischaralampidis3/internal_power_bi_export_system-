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

from app.core.database import SessionLocal
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