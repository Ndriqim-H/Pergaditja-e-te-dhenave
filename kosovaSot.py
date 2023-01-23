## import libraries
import csv
import time
import os.path
from datetime import datetime
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

## Import the other modules
import Database.ArticleService as _articleService
import Models.Article as Article
import Helpers.utils as utils

## Configure the Selenium module
driver = webdriver.Chrome(executable_path=r"C:\webdrivers.exe")
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

web_portal = "Kosova Sot"

def getData():

    ## the tech section on KosovaSot
    tech_section_url = "https://www.kosova-sot.info/auto-tech/"

    driver.get(tech_section_url)

    delay = 10 # timeout (seconds)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'more-ajax')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn-primary').click()
    
    ## Load more articles
    for i in range(50):
        try:
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'more-ajax').click()
        except Exception as e:
            print("Error, load more could not be found!\n", e)
            break
    
    articles_urls = []
    articles = driver.find_elements(By.CLASS_NAME, 'news-md')

    ## Fill in the articles_url list with urls
    for article in articles:
        url = article.find_element(By.TAG_NAME, 'a').get_attribute("href")
        articles_urls.append(url)

    ## Get the latest article's datetime
    latest_datetime_of_existing_article = _articleService.GetLatestArticleDateTime(web_portal)

    for url in articles_urls:
        try:
            if(url == ""):
                continue

            article_details = getArticleDetails(url)

            if latest_datetime_of_existing_article is not None:
                latest_datetime_of_existing_article = datetime.strptime(str(latest_datetime_of_existing_article), '%Y-%m-%d %H:%M:%S')
                article_posted_at = datetime.strptime(article_details.posted_at, '%Y-%m-%d %H:%M:%S')
                if (article_posted_at <= latest_datetime_of_existing_article):
                    break

            rank = utils.checkIfTheArticleContainsKeywords(article_details)
            if rank == 0:
                print("An article has been skipped. Not a target!")
                continue
            
            if(article_details is None):
                print("An article has been skipped. Probblem with setting the article details!")
                continue

            article_details.rank = rank

            ## Insert the Article in the DB
            _articleService.InsertArticle(article_details)

        except Exception as e:
            print("An error has occured, ", e)

    ## Close the connection with the DB
    _articleService.CloseConnection()

def getArticleDetails(article_url):
    try:
        driver.get(article_url)
        time.sleep(2)
        article_title = driver.find_element(By.CLASS_NAME, 'main-title')
        article_title = article_title.text
        article_category = "TECH"
        article_main_photo = driver.find_element(By.CLASS_NAME, 'main-img').find_element(By.TAG_NAME, 'img').get_attribute("src")
        
        article_content_list = driver.find_elements(By.CSS_SELECTOR, ".news-content > p")
        article_content = ""
        for paragraph in article_content_list:
            article_content += paragraph.text + "\n"
        
        article_content = article_content.replace("\n", " ")

        article_keywords = ""
        # article_tags = ""
        #for tag in article_tags:
            #article_keywords += tag.text + ", "
        
        article_posted_at = driver.find_element(By.CSS_SELECTOR, "ul.published-info li:nth-of-type(2)").text
        
        article_posted_at = utils.formatTheDateTime_KosovaSot(article_posted_at)
        
        
        article_rank = 0
        article = Article.Article(article_title, article_url, article_category,
                                         article_main_photo, article_content,  
                                         article_keywords, article_posted_at, article_rank, web_portal)

        return article

    except Exception as e: 
        print("Error - ", e)
        return None

# ------------------------------------------------------------ M A I N ---------------------------------------------------------

data = getData()

# ------------------------------------------------------------------------------------------------------------------------------ 

