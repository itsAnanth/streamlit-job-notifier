import requests, time, json, smtplib, re
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.preprocessing import normalize
import joblib
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import quote

def fetch_latest_jobs():
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


def fetch_jobs(keyword="Data Science", pages=2):
    root_dir = Path(__file__).parents[1]
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = f"https://www.karkidi.com/Find-Jobs"
    jobs_list = []

    for page in range(1, pages + 1):
        url = f"{base_url}/{page}/all/India?search={quote(keyword)}"
        print(f"Scraping page: {page}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        job_blocks = soup.find_all("div", class_="ads-details")
        for job in job_blocks:
            try:
                title = job.find("h4").get_text(strip=True)
                company = job.find("a", href=lambda x: x and "Employer-Profile" in x).get_text(strip=True)
                location = job.find("p").get_text(strip=True)
                experience = job.find("p", class_="emp-exp").get_text(strip=True)
                key_skills_tag = job.find("span", string="Key Skills")
                skills = key_skills_tag.find_next("p").get_text(strip=True) if key_skills_tag else ""
                summary_tag = job.find("span", string="Summary")
                summary = summary_tag.find_next("p").get_text(strip=True) if summary_tag else ""

                jobs_list.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Experience": experience,
                    "Summary": summary,
                    "Skills": skills
                })
            except Exception as e:
                print(f"Error parsing job block: {e}")
                continue
            
    df = pd.DataFrame(jobs_list)
    print(f"Scraped {len(df)} jobs.")
    df.to_csv(f"{root_dir}/data/jobs.csv", index=False)
    return df

def clean_skills(text):
    skills = re.split(r'[|,/\n]+', text)
    return ' '.join([re.sub(r'[^a-zA-Z\s]', '', s).lower().strip() for s in skills if s.strip()])


if __name__ == "__main__":
    fetch_jobs(pages=10)