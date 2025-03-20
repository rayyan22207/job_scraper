import time
import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime
from database import get_sites  # Import database functions

# Set up Selenium WebDriver
def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver
def scrape_jobs(job_title, location, sites):
    driver = init_driver()
    all_jobs = []

    for site_name, site_url in sites:
        print(f"🔍 Searching {site_name}...")
        url = site_url.format(job_title, location)
        driver.get(url)
        time.sleep(5)  # Allow time for page load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs = []

        # Identify job listing containers dynamically
        job_cards = soup.find_all(["div", "li", "article"], class_=lambda x: x and "job" in x.lower())

        for job_card in job_cards:
            try:
                # Extract job title dynamically
                title_elem = job_card.find(["h2", "h3", "a"], class_=lambda x: x and "title" in x.lower())
                title = title_elem.text.strip() if title_elem else "N/A"

                # Extract company name dynamically
                company_elem = job_card.find(["h4", "span", "div"], class_=lambda x: x and "company" in x.lower())
                company = company_elem.text.strip() if company_elem else "N/A"

                # Extract job location dynamically
                location_elem = job_card.find(["span", "div"], class_=lambda x: x and "location" in x.lower())
                location = location_elem.text.strip() if location_elem else "N/A"

                # Extract job link dynamically
                link_elem = job_card.find("a", href=True)
                link = link_elem["href"] if link_elem else "N/A"

                # Ensure full link
                if link.startswith("/"):
                    link = site_url.split("/jobs")[0] + link  # Append base URL if needed

                # Store in standardized format
                jobs.append({"Title": title, "Company": company, "Location": location, "Link": link})

            except Exception as e:
                print(f"⚠️ Error parsing job card: {e}")
                continue  # Skip to the next job posting

        print(f"✅ Found {len(jobs)} jobs on {site_name}")
        all_jobs.extend(jobs)

    driver.quit()
    return all_jobs

