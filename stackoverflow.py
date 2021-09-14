import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=react&r=true&sort=p"

HEADERS = HEADERS = {
    'Host': 'stackoverflow.com',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
  }

def get_last_page():
  response = requests.get(URL, headers = HEADERS)
  soup = BeautifulSoup(response.text , "html.parser")

  pages = soup.find_all("a", {"class": "s-pagination--item"})

  last_page = pages[-2].text.strip()
  
  return last_page

def parse_job(html):
  title = html.find("a", {'class': "s-link stretched-link"})
  company = html.find("h3")

  return {
    'link': title['href'],
    'title': title.text,
    'company': company.find('span').text.strip(),
    'location': company.find("span", {"class": "fc-black-500"}).text.strip(),
    'salary': "-"
  }

def load_jobs(last_page):
  jobs = []
  for page in range(last_page):
    response = requests.get(f"{URL}&pg={page}", headers = HEADERS)
    soup = BeautifulSoup(response.text , "html.parser")
    vacancies = soup.find("div", {"class": "listResults"}).find_all("div", {"class": "-job"})
    for vacancy in vacancies:
      jobs.append(parse_job(vacancy))
  return jobs

def get_jobs():
  last_page = get_last_page()
  return load_jobs(last_page)