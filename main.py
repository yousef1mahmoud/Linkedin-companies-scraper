from bs4 import BeautifulSoup
import time
from itertools import zip_longest
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user = {
        "email": "yousef.dev9@gmail.com",
        "password": "You!@#sef123"
    }
data = []

browser = webdriver.Chrome(executable_path="driver/chromedriver.exe")
options = Options()
options.headless = False

browser.get("https://www.linkedin.com/login")

email_field = browser.find_element_by_id('username')
email_field.send_keys(user['email'])

password_field = browser.find_element_by_id('password')
password_field.send_keys(user['password'])

submit_button = browser.find_element_by_css_selector('button[aria-label="Sign in"]')
submit_button.click()

time.sleep(2)

for i in range(1, 48):
    URL = "https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22106155005%22%5D&industry=%5B%2243%22%5D&origin=FACETED_SEARCH&page=" + str(i)
    browser.get(URL)

    source = BeautifulSoup(browser.page_source, 'lxml')

    companies = source.find_all('li', class_='reusable-search__result-container')

    for company in companies:
        link = company.find('span', class_='entity-result__title-text').find('a', class_='app-aware-link').attrs['href']
        browser.get(link + 'about')
        company_src = BeautifulSoup(browser.page_source, 'lxml')

        try:

            name = company_src.find('h1', class_='org-top-card-summary__title').text.strip()

            try:
                overview = company_src.find('p',
                                            class_='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal').text
            except Exception as e:
                overview = 'NON'

            company_data = {
                "name": name,
                "link": link,
                "overview": overview
            }

            data.append(company_data)

        except Exception as e:
            pass


print(data)
with open('data.txt', 'w') as file:
    file.write(str(data))