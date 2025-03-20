import sqlite3

DB_NAME = "job_scraper.db"

def create_database():
    """Create a database and job_sites table if not exists"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        url TEXT
    )
    """)

    # Add default job sites
    cursor.execute("INSERT OR IGNORE INTO job_sites (name, url) VALUES (?, ?)", 
                   ("LinkedIn", "https://www.linkedin.com/jobs/search/?keywords={}&location={}"))
    cursor.execute("INSERT OR IGNORE INTO job_sites (name, url) VALUES (?, ?)", 
                   ("Indeed", "https://www.indeed.com/jobs?q={}&l={}"))
    cursor.execute("INSERT OR IGNORE INTO job_sites (name, url) VALUES (?, ?)", 
                   ("Glassdoor", "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={}&locT=C&locId={}"))

    conn.commit()
    conn.close()

def add_site(name, url):
    """Add a new job website to the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO job_sites (name, url) VALUES (?, ?)", (name, url))
        conn.commit()
        print(f"✅ Added {name} to job sites.")
    except sqlite3.IntegrityError:
        print(f"⚠️ {name} already exists!")
    conn.close()

def delete_site(name):
    """Delete a job website from the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM job_sites WHERE name = ?", (name,))
    conn.commit()
    print(f"🗑️ Removed {name} from job sites.")
    conn.close()

def get_sites():
    """Fetch all stored job websites"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, url FROM job_sites")
    sites = cursor.fetchall()
    conn.close()
    return sites

# Run this once to create the database
if __name__ == "__main__":
    create_database()
