"""
Database setup and utilities for the Data Insights App.
Creates a sample database with 500+ rows of sales data.
"""
import sqlite3
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample data for generating realistic records
PRODUCTS = [
    "Laptop Pro", "Wireless Mouse", "Mechanical Keyboard", "USB-C Hub",
    "Monitor 27in", "Webcam HD", "Headphones", "Desk Lamp", "Standing Desk",
    "Ergonomic Chair", "Tablet", "Smartphone", "Smartwatch", "Bluetooth Speaker",
    "Power Bank", "Cable Set", "Screen Protector", "Laptop Bag", "USB Drive",
    "External SSD", "Gaming Mouse", "RGB Keyboard", "Microphone", "Streaming Camera"
]

CUSTOMERS = [
    "Acme Corp", "Tech Solutions Inc", "Global Industries", "Digital Ventures",
    "Innovation Labs", "Future Systems", "Cloud Services", "Data Analytics Co",
    "Software Solutions", "Hardware Plus", "Network Systems", "Security Pro",
    "Enterprise Solutions", "Startup Hub", "Dev Tools Inc", "AI Research Lab",
    "Blockchain Co", "Mobile Apps Ltd", "Web Services", "IT Consulting"
]

REGIONS = ["North America", "Europe", "Asia Pacific", "South America", "Middle East", "Africa"]

CATEGORIES = ["Electronics", "Accessories", "Furniture", "Software", "Services"]


def create_database(db_path: str = "sales_data.db") -> None:
    """Create database with sales data schema and populate with 500+ rows."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            customer TEXT NOT NULL,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            region TEXT NOT NULL,
            sales_rep TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            region TEXT NOT NULL,
            contact_email TEXT,
            total_orders INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0
        )
    """)
    
    # Generate sample data
    logger.info("Generating sample sales data...")
    sales_data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(600):  # Generate 600 rows to exceed 500 requirement
        date = start_date + timedelta(days=random.randint(0, 365))
        customer = random.choice(CUSTOMERS)
        product = random.choice(PRODUCTS)
        category = random.choice(CATEGORIES)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10.0, 2000.0), 2)
        total_amount = round(quantity * unit_price, 2)
        region = random.choice(REGIONS)
        sales_rep = f"Rep_{random.randint(1, 10)}"
        
        sales_data.append((
            date.strftime("%Y-%m-%d"),
            customer,
            product,
            category,
            quantity,
            unit_price,
            total_amount,
            region,
            sales_rep
        ))
    
    cursor.executemany("""
        INSERT INTO sales (date, customer, product, category, quantity, unit_price, total_amount, region, sales_rep)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sales_data)
    
    # Populate customers table
    for customer in CUSTOMERS:
        cursor.execute("""
            SELECT COUNT(*), SUM(total_amount) 
            FROM sales 
            WHERE customer = ?
        """, (customer,))
        result = cursor.fetchone()
        total_orders = result[0] if result[0] else 0
        total_spent = result[1] if result[1] else 0.0
        
        cursor.execute("""
            INSERT OR REPLACE INTO customers (name, region, contact_email, total_orders, total_spent)
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer,
            random.choice(REGIONS),
            f"{customer.lower().replace(' ', '_')}@example.com",
            total_orders,
            total_spent
        ))
    
    conn.commit()
    logger.info(f"Database created with {len(sales_data)} sales records")
    conn.close()


def get_db_connection(db_path: str = "sales_data.db"):
    """Get database connection."""
    return sqlite3.connect(db_path)


def execute_query(query: str, db_path: str = "sales_data.db") -> List[Dict[str, Any]]:
    """Execute a SELECT query and return results as list of dictionaries."""
    conn = get_db_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()


def get_table_info(db_path: str = "sales_data.db") -> Dict[str, Any]:
    """Get information about database tables."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    info = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        info[table_name] = {
            "row_count": count,
            "columns": [col[1] for col in columns]
        }
    
    conn.close()
    return info


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")

