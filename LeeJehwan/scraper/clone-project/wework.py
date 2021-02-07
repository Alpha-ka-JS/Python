import requests
from bs4 import BeautifulSoup


def extract_job(html):
    anchor = html.find("a", recursive=False)
    company = anchor.find("span", {"class": "company"}).get_text()
    title = anchor.find("span", {"class": "title"}).get_text()
    href = anchor["href"]
    return {
        "title": title,
        "company": company,
        "link": f"https://weworkremotely.com{href}",
    }


def extract_jobs(URL):
    jobs = []
    print(f"Scrapping from wework...")
    response = requests.get(f"{URL}")
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all("section", {"class": "jobs"})

    for section in sections:
        results = section.find_all("li")[:-1]
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(term):
    URL = f"https://weworkremotely.com/remote-jobs/search?term={term}"
    jobs = extract_jobs(URL)
    if len(jobs) == 0:
        print("Wework: no result!")
    return jobs
