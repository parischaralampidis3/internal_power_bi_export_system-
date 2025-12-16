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