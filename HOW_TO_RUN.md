# How to Run the OMS Application

## Prerequisites

Before running the application, ensure you have the following installed:

| Requirement | Version | Purpose |
|------------|---------|---------|
| Python | 3.7 or higher | Backend runtime |
| pip | Latest | Package manager |
| Web Browser | Chrome/Firefox/Edge | Frontend access |
| Git (Optional) | Latest | Version control |

---

## Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\91951\Desktop\UNT\Spring 2026 sem 2\fdb\project\OMS
```

### Step 2: Install Required Dependencies
```bash
pip install flask faker
```

Dependencies:
- **flask** - Web framework for backend API
- **faker** - Library for generating realistic test data

### Step 3: Verify Installation
```bash
pip list
```
Confirm both Flask and Faker appear in the installed packages.

---

## Running the Application

### Step 1: Start the Flask Server
```bash
python app.py
```

Expected output:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

### Step 2: Open Web Browser

Navigate to: `http://localhost:5000` or `http://127.0.0.1:5000`

You should see the OMS interface with:
- Database Tables sidebar (left)
- SQL Query Editor (center/right)
- Results display area

### Step 3: Stop the Server

Press `CTRL + C` in the terminal to stop the Flask server.

---

## Basic Usage Walkthrough

### Creating Tables:
1. Click on any table name (e.g., "User")
2. Click "+ CREATE TABLE" button
3. Review the CREATE TABLE query in editor
4. Click "EXECUTE" button
5. See success message in toast notification

### Loading Sample Data:
1. Click on a table name (e.g., "Subscription_Plan")
2. Click "LOAD DATA" button
3. Wait for generation to complete (shows progress toast)
4. Badge "[Loaded]" appears next to table name

### Running Queries:
1. Write SQL query in the editor:
   ```sql
   SELECT * FROM "User" LIMIT 10;
   ```
2. Click "EXECUTE" button
3. Results display in table format below
4. View row count: "Results [showing X rows]"

### Downloading Results:
1. Run a SELECT query
2. Click "📥 CSV" to download as spreadsheet
3. Click "📥 PNG" to download as image

---

## Example Queries to Try

### Insert a test user:
```sql
INSERT INTO User (name, email, password, join_date) 
VALUES ('TEST_USER_001', 'testuser001@gmail.com', 'password123', '2026-04-24');
```

### Find all active subscriptions (JOIN example):
```sql
SELECT u.name, sp.plan_name, s.status 
FROM Subscription s
INNER JOIN User u ON s.user_id = u.user_id
INNER JOIN Subscription_Plan sp ON s.plan_id = sp.plan_id
WHERE s.status = 'Active'
LIMIT 50;
```

### Aggregate revenue by plan:
```sql
SELECT sp.plan_name, COUNT(s.subscription_id) as subscriptions, SUM(p.amount) as total_revenue
FROM Subscription_Plan sp
LEFT JOIN Subscription s ON sp.plan_id = s.plan_id
LEFT JOIN Payment p ON s.subscription_id = p.subscription_id
GROUP BY sp.plan_id
ORDER BY total_revenue DESC;
```

---

## Project Structure on Disk

```
OMS/
├── app.py                      # Main Flask application (run this)
├── oms_database.db             # SQLite database (auto-created)
├── HOW_TO_RUN.md              # This file
├── static/
│   ├── css/
│   │   └── style.css          # UI styling
│   └── js/
│       └── script.js          # Frontend logic
└── templates/
    └── index.html             # Web interface
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Flask not found" | Run `pip install flask` |
| "Port 5000 already in use" | Change port in app.py: `app.run(debug=True, port=5001)` |
| "Database locked" | Close other instances; restart Flask server |
| "No module named faker" | Run `pip install faker` |
| "Query executed but no results" | Check table exists: `SELECT * FROM sqlite_master WHERE type='table';` |
| "Email unique constraint failed" | Use unique emails; test data auto-generates unique ones |

---

## Database File Management

### Reset Database (Delete all data):
```bash
# Stop Flask server first
del oms_database.db
# Restart Flask server (creates fresh database)
python app.py
```

### Backup Database:
```bash
# Copy database file
copy oms_database.db oms_database_backup.db
```

### View Database Directly (Optional):
```bash
# Install SQLite browser (optional)
pip install db-browser-for-sqlite

# Or use command-line:
sqlite3 oms_database.db
# Then type: .tables (to list tables)
# Or: SELECT * FROM User LIMIT 5;
```

---

## Performance Tips

### 1. Large Result Sets
Use LIMIT clause to restrict rows:
```sql
SELECT * FROM Content LIMIT 1000;
```

### 2. Speed Up Queries
Add WHERE conditions:
```sql
SELECT * FROM User WHERE status = 'Active';
```

### 3. Avoid Timeouts
Complex JOINs on large datasets:
```sql
-- Good: Limits results
SELECT * FROM User u 
JOIN Subscription s ON u.user_id = s.user_id 
LIMIT 100;

-- Avoid: Can be slow without LIMIT
SELECT * FROM User u 
JOIN Subscription s ON u.user_id = s.user_id;
```

---

## Application Features

### Sidebar Table Management
- View all database tables
- Expand table options with dropdown arrow
- CREATE TABLE - Generate table creation queries
- LOAD DATA - Generate and load sample records
- DROP TABLE - Generate table deletion queries
- [Loaded] badge - Indicates table has been populated

### SQL Query Editor
- Write custom SQL queries
- Execute any valid SQL statement
- Auto-load SELECT queries for new tables
- Clear editor with CLEAR button

### Results Display
- Shows query results in formatted table
- Displays row count: "Results [showing X rows]"
- Download results as CSV or PNG
- Scroll horizontally/vertically for large datasets

### File Operations
- UPLOAD QUERY - Load .sql or .txt files
- SAVE (.sql/.txt) - Export current query

---

## System Requirements

### Minimum
- CPU: Dual-core processor
- RAM: 2GB
- Storage: 500MB (includes database)
- OS: Windows, macOS, or Linux

### Recommended
- CPU: Quad-core processor
- RAM: 4GB+
- Storage: 1GB
- OS: Windows 10+, macOS 10.14+, or modern Linux

---

## Getting Help

If you encounter issues:

1. Check the Troubleshooting section above
2. Verify all dependencies are installed: `pip list`
3. Ensure Flask server is running on correct port
4. Check browser console for JavaScript errors (F12)
5. Review Flask server terminal output for error messages

---

## Contact & Support

For questions or issues with the OMS application, refer to:
- Project documentation in the main report
- Database schema details in app.py comments
- Example queries in this guide
