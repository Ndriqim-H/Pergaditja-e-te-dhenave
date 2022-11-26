## import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv
import time
from Models import Article;

driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")

def getData():
    ## the tech section on Telegraf
    tech_section_url = "https://telegrafi.com/teknologji/"

    delay = 5 # timeout (seconds)

    driver.get(tech_section_url)

    ## redirect to the technology section
    driver.find_element(By.CLASS_NAME, 'go-to-category').click()

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'lineClamp')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    ## load more articles (50 times)
    for i in range(1):
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'load-more').click()

    ## BeautifulSoup 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    html = list(soup.children)[0]
    body = list(html.children)[2]

    article_urls = body.find_all("a",{"class":"lineClamp"})
    articles_list = []
    for article_header in article_urls:
        url = article_header.get("href")
        if(url == ""):
            continue
        article_detail = getArticleDetails(url)
        articles_list.append(article_detail)

    return articles_list

def getArticleDetails(article_url):
    # article = Article()
    driver.get(article_url)
    ## BeautifulSoup 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    html = list(soup.children)[0]
    body = list(html.children)[2]
    article_title    = driver.find_element(By.CLASS_NAME, 'article-heading').text
    article_category = driver.find_element(By.CLASS_NAME, 'article-category').text
    article_posted_at = driver.find_element(By.CLASS_NAME, 'article-posted').text
    article_main_photo = driver.find_element(By.CLASS_NAME, 'featured-image')
    # article_main_photo = body.find_all({"class":"featured-image"})
    article_excerpt = driver.find_element(By.CLASS_NAME, "article-body").text



def writeToFile(data): 
    with open('tech_articles.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        article_no = 0
        for row in data:
            article_no += 1
            row = [article_no, id(row), row]
            writer.writerow(row)

# Columns of the dataset
columns = ['article_no', 'id', 'title', 'category', 'main_photo', 'excerpt', 'content', 'video', 'keywords', 'comments', 'posted_at']

# The actual data
data = getData()

writeToFile(data)