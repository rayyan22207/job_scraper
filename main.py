import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from fpdf import FPDF

def init_driver():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-software-rasterizer")  # Prevents GPU-related issues
    options.add_argument("--no-sandbox")  # Required for some environments
    options.add_argument("--disable-dev-shm-usage")  # Fixes shared memory issues
    options.add_argument("--log-level=3")  # Suppresses ChromeDriver logs

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# Function to scrape LinkedIn jobs using Selenium
def scrape_linkedin(keyword, location):
    driver = init_driver()
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
    driver.get(url)
    time.sleep(5)  # Allow time for page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = []

    for job_card in soup.find_all("div", class_="base-card"):
        title = job_card.find("h3", class_="base-search-card__title").text.strip()
        company = job_card.find("h4", class_="base-search-card__subtitle").text.strip()
        location = job_card.find("span", class_="job-search-card__location").text.strip()
        link = job_card.find("a", class_="base-card__full-link")["href"]

        jobs.append({"Title": title, "Company": company, "Location": location, "Link": link})

    driver.quit()
    return jobs

def scrape_indeed(keyword, location):
    driver = init_driver()
    url = f"https://www.indeed.com/jobs?q={keyword}&l={location}"
    driver.get(url)

    time.sleep(5)  # Let the page load

    # Scroll down to load more jobs
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(3):  # Scroll multiple times
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = []

    for job_card in soup.find_all("div", class_="job_seen_beacon"):  # Updated class name
        try:
            title = job_card.find("h2", class_="jobTitle").text.strip()
            company = job_card.find("span", class_="companyName").text.strip()
            location = job_card.find("div", class_="companyLocation").text.strip()
            link = "https://www.indeed.com" + job_card.find("a", class_="jcs-JobTitle")["href"]

            jobs.append({"Title": title, "Company": company, "Location": location, "Link": link})
        except AttributeError as e:
            print(f'Problem at indeed: {e}')
            continue  # Skip job cards with missing data

    driver.quit()
    return jobs

def scrape_glassdoor(keyword, location):
    driver = init_driver()
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keyword}&locT=C&locId={location}"
    driver.get(url)

    time.sleep(5)  # Let page load

    # Scroll down to load more jobs
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(3):  # Scroll multiple times
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = []

    for job_card in soup.find_all("li", class_="react-job-listing"):  # Updated class name
        try:
            title = job_card.find("a", class_="jobLink").text.strip()
            company = job_card.find("div", class_="d-flex justify-content-between align-items-start").text.strip()
            location = job_card.find("span", class_="pr-xxsm").text.strip()
            link = "https://www.glassdoor.com" + job_card.find("a", class_="jobLink")["href"]

            jobs.append({"Title": title, "Company": company, "Location": location, "Link": link})
        except AttributeError as e:
            print(f'Problem at indeed: {e}')
            continue  # Skip job cards with missing data

    driver.quit()
    return jobs

# Function to save jobs to CSV
def save_to_csv(jobs, filename="jobs.csv"):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Jobs saved to {filename}")

# Function to save jobs to PDF
def save_to_pdf(jobs, filename="jobs.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Use a Unicode-compatible font (FreeSans)
    pdf.add_font("FreeSans", "", "FreeSans.ttf", uni=True)
    pdf.set_font("FreeSans", size=12)

    pdf.cell(200, 10, txt="Job Listings", ln=True, align="C")

    for job in jobs:
        pdf.cell(200, 10, txt=f"Title: {job['Title']}", ln=True)
        pdf.cell(200, 10, txt=f"Company: {job['Company']}", ln=True)
        pdf.cell(200, 10, txt=f"Location: {job['Location']}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Link: {job['Link']}")  # Wrap long links
        pdf.cell(200, 10, txt="---------------------------------------", ln=True)

    pdf.output(filename, "F")
    print(f"Jobs saved to {filename}")



# Run the scraper
if __name__ == "__main__":
    keyword = input("Enter job title: ")
    location = input("Enter job location: ")

    print("Fetching jobs from LinkedIn...")
    linkedin_jobs = scrape_linkedin(keyword, location)
    print(f"Found {len(linkedin_jobs)} jobs on Linkedin")

    print("Fetching jobs from Indeed...")
    indeed_jobs = scrape_indeed(keyword, location)
    print(f"Found {len(indeed_jobs)} jobs on Indeed")


    print("Fetching jobs from Glassdoor...")
    glassdoor_jobs = scrape_glassdoor(keyword, location)
    print(f"Found {len(glassdoor_jobs)} jobs on Glassdoor")

    all_jobs = (linkedin_jobs if linkedin_jobs else []) + \
           (indeed_jobs if indeed_jobs else []) + \
           (glassdoor_jobs if glassdoor_jobs else [])
    if all_jobs:
        save_to_csv(all_jobs)
        save_to_pdf(all_jobs)
    else:
        print("No jobs found!")
