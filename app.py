from flask import Flask, render_template, request, jsonify
import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

app = Flask(__name__)
fake = Faker()

def get_db_connection():
    conn = sqlite3.connect('oms_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database with tables if they don't exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Subscription_Plan Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Subscription_Plan'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE Subscription_Plan (
                    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_name TEXT NOT NULL,
                    price REAL NOT NULL,
                    duration INTEGER NOT NULL
                )
            ''')
        
        # User Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE User (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    join_date DATE NOT NULL
                )
            ''')
        
        # Content Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Content'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE Content (
                    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    type TEXT NOT NULL,
                    release_year INTEGER,
                    duration INTEGER
                )
            ''')
        
        # Subscription Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Subscription'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE Subscription (
                    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    plan_id INTEGER NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES User(user_id),
                    FOREIGN KEY (plan_id) REFERENCES Subscription_Plan(plan_id)
                )
            ''')
        
        # Device Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Device'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE Device (
                    device_id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    device_type TEXT NOT NULL,
                    last_login DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES User(user_id)
                )
            ''')
        
        # Viewing_History Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Viewing_History'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE Viewing_History (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content_id INTEGER NOT NULL,
                    watch_date DATE NOT NULL,
                    watch_duration INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES User(user_id),
                    FOREIGN KEY (content_id) REFERENCES Content(content_id)
                )
            ''')
        
        # Payment Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Payment'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE Payment (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subscription_id INTEGER NOT NULL,
                    payment_date DATE NOT NULL,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    payment_status TEXT NOT NULL,
                    FOREIGN KEY (subscription_id) REFERENCES Subscription(subscription_id)
                )
            ''')
        
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    query = data.get('query')
    
    if not query or not query.strip():
        return jsonify({"status": "error", "message": "Query cannot be empty"})
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        # If SELECT query, return data rows
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            if not rows:
                return jsonify({"status": "success", "columns": [], "data": []})
            columns = list(rows[0].keys())
            result = [dict(row) for row in rows]
            return jsonify({"status": "success", "columns": columns, "data": result})
        
        conn.commit()
        return jsonify({"status": "success", "message": "Command executed successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()

@app.route('/load/<table_name>', methods=['POST'])
def load_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if table already has data
        cursor.execute(f"SELECT COUNT(*) as count FROM \"{table_name}\"")
        result = cursor.fetchone()
        if result and result['count'] > 0:
            return jsonify({"status": "error", "message": f"{table_name} already has data"})
        
        base_date = datetime(2025, 5, 1)  # Start from May 2025
        
        if table_name == "Subscription_Plan":
            plans = [
                ("Basic", 4.99, 30),
                ("Standard", 9.99, 30),
                ("Premium", 15.99, 30),
                ("Family", 19.99, 30),
                ("Student", 5.99, 30),
                ("Annual", 99.99, 365),
            ]
            cursor.executemany(
                "INSERT INTO Subscription_Plan (plan_name, price, duration) VALUES (?, ?, ?)",
                plans
            )
        
        elif table_name == "User":
            data = []
            used_emails = set()
            for i in range(3000):
                name = fake.name()
                # Create unique email using counter to ensure no duplicates
                email_domain = random.choice(['gmail.com', 'outlook.com'])
                email = f"user{i}@{email_domain}"
                
                # Ensure email is unique (in case of rare collisions)
                while email in used_emails:
                    email = f"user{i}_{random.randint(1000, 9999)}@{email_domain}"
                
                used_emails.add(email)
                password = '*' * random.randint(8, 16)
                join_date = base_date + timedelta(days=random.randint(0, 365))
                data.append((name, email, password, join_date.strftime('%Y-%m-%d')))
            
            cursor.executemany(
                "INSERT INTO User (name, email, password, join_date) VALUES (?, ?, ?, ?)",
                data
            )
        
        elif table_name == "Content":
            content_types = ['Movie', 'TV Show', 'Documentary', 'Series', 'Special', 'Stand-up']
            data = []
            for i in range(10000):
                title = fake.word() + ' ' + fake.word()
                ctype = random.choice(content_types)
                year = random.randint(1990, 2026)
                duration = random.randint(45, 240)
                data.append((title, ctype, year, duration))
            
            cursor.executemany(
                "INSERT INTO Content (title, type, release_year, duration) VALUES (?, ?, ?, ?)",
                data
            )
        
        elif table_name == "Subscription":
            # 3000 subscriptions, no empty cells
            data = []
            for i in range(3000):
                user_id = random.randint(1, 3000)
                plan_id = random.randint(1, 6)
                start_date = base_date + timedelta(days=random.randint(0, 300))
                end_date = start_date + timedelta(days=30)
                status = random.choice(['Active', 'Inactive', 'Cancelled'])
                data.append((user_id, plan_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), status))
            
            cursor.executemany(
                "INSERT INTO Subscription (user_id, plan_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
                data
            )
        
        elif table_name == "Device":
            # Device IDs starting from 0000001, max 4 devices per user
            data = []
            device_id_counter = 1
            user_device_count = {}
            
            for i in range(10000):  # Try to generate enough devices
                user_id = random.randint(1, 3000)
                
                # Check if this user already has 4 devices
                if user_id not in user_device_count:
                    user_device_count[user_id] = 0
                
                if user_device_count[user_id] < 4:
                    device_id = str(device_id_counter).zfill(7)
                    device_type = random.choice(['Mobile', 'Tablet', 'Desktop', 'Smart TV', 'Laptop'])
                    last_login = base_date + timedelta(days=random.randint(0, 365))
                    data.append((device_id, user_id, device_type, last_login.strftime('%Y-%m-%d')))
                    device_id_counter += 1
                    user_device_count[user_id] += 1
            
            cursor.executemany(
                "INSERT INTO Device (device_id, user_id, device_type, last_login) VALUES (?, ?, ?, ?)",
                data
            )
        
        elif table_name == "Viewing_History":
            data = []
            for i in range(10000):
                user_id = random.randint(1, 3000)
                content_id = random.randint(1, 10000)
                watch_date = base_date + timedelta(days=random.randint(0, 365))
                watch_duration = random.randint(1, 300)
                data.append((user_id, content_id, watch_date.strftime('%Y-%m-%d'), watch_duration))
            
            cursor.executemany(
                "INSERT INTO Viewing_History (user_id, content_id, watch_date, watch_duration) VALUES (?, ?, ?, ?)",
                data
            )
        
        elif table_name == "Payment":
            payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Google Pay', 'Apple Pay']
            payment_statuses = ['Completed', 'Pending', 'Failed', 'Refunded']
            data = []
            for i in range(10000):
                subscription_id = random.randint(1, 3000)
                payment_date = base_date + timedelta(days=random.randint(0, 365))
                amount = round(random.uniform(4.99, 99.99), 2)
                payment_method = random.choice(payment_methods)
                payment_status = random.choice(payment_statuses)
                data.append((subscription_id, payment_date.strftime('%Y-%m-%d'), amount, payment_method, payment_status))
            
            cursor.executemany(
                "INSERT INTO Payment (subscription_id, payment_date, amount, payment_method, payment_status) VALUES (?, ?, ?, ?, ?)",
                data
            )
        
        else:
            return jsonify({"status": "error", "message": f"Unknown table: {table_name}"})
        
        conn.commit()
        return jsonify({"status": "success", "message": f"Data loaded successfully for {table_name}"})
    
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

