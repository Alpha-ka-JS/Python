import requests
from bs4 import BeautifulSoup

URL = f"https://www.stackoverflow.com/jobs?q=python&sort=i"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_pages = int(pages[-2].get_text(strip=True))
    return last_pages


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company, *location = html.find("h3").find_all("span", recursive=True)
    company = company.get_text(strip=True)
    location = location[0].get_text(strip=True).strip("-").strip(" \r").strip("\n")
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}",
    }


def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping SO: page {page+1}")
        response = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
