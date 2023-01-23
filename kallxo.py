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

web_portal = "Kallxo"

def getData():

    ## The tech section on Kallxo
    tech_section_url = "https://kallxo.com/teknologji/"

    delay = 10 # timeout (seconds)

    driver.get(tech_section_url)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'loadmore-inf')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    ## Load more articles
    for i in range(1):
        try:
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'loadmore-inf').click()
        except:
            print("Error, load more could not be found!")
            break
    
    articles_urls = []
    articles = driver.find_elements(By.CLASS_NAME, 'post_item__thumb')
    # articles_titles = driver.find_elements(By.CLASS_NAME, 'post_item__content')

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
                latest_datetime_of_existing_article = datetime.strptime(latest_datetime_of_existing_article, '%Y-%m-%d %H:%M:%S')
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
        article_title = driver.find_element(By.CLASS_NAME, 'single_article').find_element(By.CLASS_NAME, 'single_article__header').find_element(By.TAG_NAME, "h1").text
        article_category = "TEKNOLOGJI / LAJME TEKNOLOGJI"
        article_main_photo = driver.find_element(By.CLASS_NAME, 'single_article__thumb').find_element(By.TAG_NAME, "img").get_attribute("src")
        
        article_content_list = driver.find_element(By.CLASS_NAME, "single_article__main").find_elements(By.TAG_NAME, "p")
        article_content = ""
        for paragraph in article_content_list:
            article_content += paragraph.text + "\n"

        article_keywords = ""
        article_tags = driver.find_element(By.CLASS_NAME, 'post_item__tags').find_elements(By.TAG_NAME, "a")
        for tag in article_tags:
            article_keywords += tag.text + ", "

        article_posted_at = driver.find_element(By.CLASS_NAME, 'post_date').text
        article_posted_at = utils.formatTheDateTime_Kallxo(article_posted_at)

        # article_author_name = driver.find_element(By.CLASS_NAME, 'single_article__author__name').text

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
