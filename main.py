## import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv
import time

def getData():
    ## the tech section on Telegraf
    tech_section_url = "https://telegrafi.com/teknologji/"

    delay = 5 # timeout (seconds)

    driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")
    driver.get(tech_section_url)

    ## redirect to the technology section
    driver.find_element(By.CLASS_NAME, 'go-to-category').click()

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'lineClamp')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    ## load more articles (50 times)
    for i in range(50):
        time.sleep(4)
        driver.find_element(By.CLASS_NAME, 'load-more').click()

    tech_articles_headers = driver.find_elements(By.CLASS_NAME, 'lineClamp')

    tech_articles_headers_list = []
    for article in tech_articles_headers:
        if(article.text == ""):
            continue
        tech_articles_headers_list.append(article.text)

    all_titles = tech_articles_headers_list

    return all_titles


def writeToFile(data): 
    with open('/tech_articles.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        article_no = 0
        for row in data:
            article_no += 1
            row = [article_no, id(row), row]
            writer.writerow(row)

# Columns of the dataset
columns = ['article_no', 'id', 'title']

# The actual data
data = getData()

writeToFile(data)