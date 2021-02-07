import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
        last_pages = int(pages[-2].get_text(strip=True))
    except:
        return -1
    return last_pages


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company = html.find("h3").find_all("span", recursive=True)[0].get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "link": f"https://stackoverflow.com/jobs/{job_id}",
    }


def extract_jobs(last_pages, URL):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping from Stackoverflow: page {page+1}")
        response = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(term):
    URL = f"https://stackoverflow.com/jobs?r=true&q={term}"
    last_page = get_last_page(URL)
    if last_page == -1:
        print("Stackoverflow: no result!")
        return []
    jobs = extract_jobs(last_page, URL)
    return jobs
