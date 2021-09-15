import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
  }

def get_last_page(url):

  response = requests.get(url, headers = HEADERS )

  soup = BeautifulSoup(response.text , "html.parser")

  hh_paginator = soup.find_all("span", {'class': 'pager-item-not-in-short-range'});
  pages = []

  for page in hh_paginator:
    pages.append(int(page.find('a').text))

  if len(pages) > 0:
    return pages[-1]
  else:
    return 0

def parse_job(html):
  title = html.find("a");
  company = html.find("div", {"class": "vacancy-serp-item__meta-info-company"}).text
  location = html.find("span", {"data-qa": "vacancy-serp__vacancy-address"}).text
  compensation = html.find("span", {'data-qa': "vacancy-serp__vacancy-compensation"})

  if (compensation):
    compensation = compensation.text
  else:
    compensation = ""

  return {
    'link': title['href'].partition("?")[0],
    'title': title.text,
    'company': company.strip(),
    'location': location.strip(),
    'salary': compensation
  }

def load_jobs(url, last_page):
  jobs = []
  for page in range(last_page):
    print(f"HH parsing {page} page.")
    response = requests.get(f"{url}&page={page}", headers = HEADERS)
    soup = BeautifulSoup(response.text , "html.parser")
    vacancies = soup.find_all("div", {'class': "vacancy-serp-item"})
    for vacancy in vacancies:
      jobs.append(parse_job(vacancy))

  return jobs

def get_jobs(keyword):
  url = f"https://hh.ru/search/vacancy?st=searchVacancy&text={keyword}&area=1&schedule=remote&order_by=publication_time&search_period=30&items_on_page=100"
  last_page = get_last_page(url)
  return load_jobs(url, last_page)