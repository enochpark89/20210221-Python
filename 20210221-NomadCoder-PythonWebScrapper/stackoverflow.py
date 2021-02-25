import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=software+engineer&sort=i"

# Get 'pagination' there are many titles by "1 of something; 2 of something etc"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_pages = pages[-2].get_text(strip=True)
    return int(last_pages)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find(
        "h3", {"class": "fc-black-700"}).find_all("span", recursive=0)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\n")
    # 0=False, 1 = True
    return {'title': title, 'company': company, 'location': location}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")
        # print(result.status_code) - to test the success rate of the request code.
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs


get_jobs()