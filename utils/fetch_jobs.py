import requests, time, json, smtplib, re
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.preprocessing import normalize
import joblib
from email.message import EmailMessage

def scrape_latest_jobs():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://www.karkidi.com/Find-Jobs/1/all/India?search=data%20science"
    jobs_list = []

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    job_blocks = soup.find_all("div", class_="ads-details")

    for job in job_blocks:
        try:
            title = job.find("h4").get_text(strip=True)
            company = job.find("a", href=lambda x: x and "Employer-Profile" in x).get_text(strip=True)
            location = job.find("p").get_text(strip=True)
            experience = job.find("p", class_="emp-exp").get_text(strip=True)
            skills = job.find("span", string="Key Skills")
            skills = skills.find_next("p").get_text(strip=True) if skills else ""

            jobs_list.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Experience": experience,
                "Skills": skills
            })
        except:
            continue
    return pd.DataFrame(jobs_list)

def clean_skills(text):
    skills = re.split(r'[|,/\n]+', text)
    return ' '.join([re.sub(r'[^a-zA-Z\s]', '', s).lower().strip() for s in skills if s.strip()])