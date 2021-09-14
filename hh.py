import requests
from bs4 import BeautifulSoup

URL = 'https://hh.ru/search/vacancy?st=searchVacancy&text=React&area=1&schedule=remote&order_by=publication_time&search_period=30&items_on_page=100'

HEADERS = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
  }

def get_last_page():

  response = requests.get(URL, headers = HEADERS )

  soup = BeautifulSoup(response.text , "html.parser")

  hh_paginator = soup.find_all("span", {'class': 'pager-item-not-in-short-range'});
  pages = []

  for page in hh_paginator:
    pages.append(int(page.find('a').text))

  return pages[-1];

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

def load_jobs(last_page):
  jobs = []
  for page in range(last_page):
    response = requests.get(f"{URL}&page={page}", headers = HEADERS)
    soup = BeautifulSoup(response.text , "html.parser")
    vacancies = soup.find_all("div", {'class': "vacancy-serp-item"})
    for vacancy in vacancies:
      jobs.append(parse_job(vacancy))

  return jobs

def get_jobs():
  last_page = get_last_page()
  return load_jobs(last_page)