import sqlite3
import os
from database import create_database, add_site, get_sites  # Import DB functions
from scraper import scrape_jobs  # Import the job scraping function
from datetime import datetime
import pandas as pd
from fpdf import FPDF

DB_NAME = "job_scraper.db"

# Function to ensure database exists
def ensure_database():
    if not os.path.exists(DB_NAME):  # If the database file doesn't exist
        print("⚠️ Database not found. Creating new database...")
        create_database()

# Function to prompt user to add job websites if none exist
def ensure_sites_exist():
    sites = get_sites()
    if not sites:  # If the database is empty
        print("\n🚀 No job websites found. Please add at least one job search site.")
        
        attempts = 0
        while attempts < 5:
            name = input("Enter the website name (or type 'done' to finish): ").strip()
            if name.lower() in ["done", "quit"]:
                break
            
            url = input(f"Enter the search URL for {name} (Use {{}} for job title and location): ").strip()
            if not url or "{}" not in url:
                print("⚠️ Invalid URL format. Please use `{}` placeholders for job title and location.")
                continue

            add_site(name, url)
            attempts += 1

        print("\n✅ Websites successfully added!")
    else:
        print(f"\n✅ {len(sites)} job websites found in the database.")

# Function to generate a unique filename
def generate_filename(job_title, ext):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{job_title.replace(' ', '_')}_{timestamp}.{ext}"

# Save jobs to CSV
def save_to_csv(jobs, job_title):
    filename = generate_filename(job_title, "csv")
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"📁 Jobs saved to {filename}")

# Save jobs to PDF
def save_to_pdf(jobs, job_title):
    filename = generate_filename(job_title, "pdf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Job Listings", ln=True, align="C")

    for job in jobs:
        pdf.cell(200, 10, txt=f"Title: {job['Title']}", ln=True)
        pdf.cell(200, 10, txt=f"Company: {job['Company']}", ln=True)
        pdf.cell(200, 10, txt=f"Location: {job['Location']}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Link: {job['Link']}")
        pdf.cell(200, 10, txt="---------------------------------------", ln=True)

    pdf.output(filename, "F")
    print(f"📁 Jobs saved to {filename}")

# Main function
def main():
    print("\n🔍 Job Scraper is starting...")

    # Ensure the database exists
    ensure_database()

    # Ensure there are job sites in the database
    ensure_sites_exist()

    # Ask the user for job details
    job_title = input("\nEnter job title: ").strip()
    location = input("Enter job location: ").strip()

    # Fetch stored job sites
    sites = get_sites()

    # Confirm number of websites being used
    print(f"\n🔍 Searching across {len(sites)} job websites...")

    # Scrape jobs
    jobs = scrape_jobs(job_title, location, sites)

    # Save results
    if jobs:
        save_to_csv(jobs, job_title)
        save_to_pdf(jobs, job_title)
    else:
        print("❌ No jobs found.")

if __name__ == "__main__":
    main()
