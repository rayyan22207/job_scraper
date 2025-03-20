# 🏰️ Job Scraper - Web Automation for Job Listings

This project is a **Python-based web scraper** that collects job listings from multiple job websites dynamically. It supports **LinkedIn, Indeed, Glassdoor, and any other job site** that can be added manually.

## 🔹 **Features**
✅ Scrapes job listings dynamically from **multiple job sites**  
✅ Uses **Selenium & BeautifulSoup** for web automation  
✅ Stores job site URLs in a **database** for flexibility  
✅ Supports **adding and removing job sites dynamically**  
✅ Saves jobs in **CSV & PDF formats** with **unique filenames**  
✅ Works even if no job site is provided (defaults to database)

---

## 🛠 **Setup Instructions**

### 🔹 1️⃣ Create a Virtual Environment
Open your terminal and run:
```bash
python -m venv venv
```

### 🔹 2️⃣ Activate the Virtual Environment
#### **Windows (CMD)**
```bash
venv\Scripts\activate
```
#### **Mac/Linux**
```bash
source venv/bin/activate
```

### 🔹 3️⃣ Install Required Packages
After activating the virtual environment, install the dependencies using:
```bash
pip install -r requirements.txt
```

### 🔹 4️⃣ Run the Script
To start scraping jobs, run:
```bash
python main.py
```

---

## 🏗 **How It Works**
1. **Checks for the Database (`job_scraper.db`)**  
   - If missing, it **creates** a new database.
   - If no job sites exist, it **asks the user to add some** (up to 5 attempts).

2. **Asks the user for job details**  
   - Prompts for **Job Title** & **Location**.

3. **Uses stored job sites for scraping**  
   - If the user provides a job search URL, it **uses that**.
   - If no URL is given, it **fetches from the database**.

4. **Scrapes jobs dynamically from multiple sites**  
   - Uses **Selenium** to load job listings.  
   - Uses **BeautifulSoup** to extract job details.  

5. **Saves results with a unique filename**  
   - Output is saved as:
     - `Python_Developer_20240320_214500.csv`
     - `Python_Developer_20240320_214500.pdf`

---

## 📌 **Adding More Features (Coming Soon!)**
This is the **basic version**. More advanced features will be added, such as:
- **Web API Support** for remote job search.
- **UI-based control panel** to manage job sites easily.
- **AI-based job matching** using NLP techniques.

🚀 **Stay tuned for updates!**

---

## 🛠 **Troubleshooting**
If you face issues:
- Ensure **Google Chrome is installed**.
- If ChromeDriver errors appear, manually install ChromeDriver.
- Run `python main.py` **inside the virtual environment**.

---

## 🌟 **License**
MIT License. Feel free to modify and enhance it!

---

