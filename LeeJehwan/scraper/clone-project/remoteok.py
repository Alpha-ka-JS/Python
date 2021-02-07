import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


def extract_job(html):
    company = html["data-company"]
    title = html.find_all("td", {"class": "company"})[1].find("h2").get_text()
    href = html["data-url"]
    return {
        "title": title,
        "company": company,
        "link": f"https://remoteok.io{href}",
    }


def extract_jobs(URL):
    jobs = []
    print(f"Scrapping from remote ok...")
    response = requests.get(f"{URL}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        results = soup.find("table", {"id": "jobsboard"}).find_all("tr", {"class": "job"})
    except:
        return []
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs(term):
    URL = f"https://remoteok.io/remote-dev+{term}-jobs"
    jobs = extract_jobs(URL)
    if len(jobs) == 0:
        print("remote ok: no result!")
    return jobs
