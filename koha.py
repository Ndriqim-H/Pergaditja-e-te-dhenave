## import libraries
import time
import re
from datetime import datetime
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

## import the other modules
import Database.ArticleService as articleService
import Models.Article as Article
import Helpers.utils as utils

## Configure the Selenium module
driver = webdriver.Chrome(executable_path=r"C:\webdrivers.exe")
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)
_articleService = articleService.dbClass()
web_portal = "Koha"

def getData():

    ## The tech section on Telegraf
    tech_section_url = "https://www.koha.net/arkivi/?acid=tech"

    driver.get(tech_section_url)

    delay = 10 # timeout (seconds)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    articles_urls = []

    ## Get the latest article's datetime
    latest_datetime_of_existing_article = _articleService.GetLatestArticleDateTime(web_portal)

    todays_date = str(datetime.today()).split(" ")[0]

    ## Select the datetime range
    if latest_datetime_of_existing_article is not None:
        _latest_datetime_of_existing_article = str(latest_datetime_of_existing_article).split(" ")[0]

        driver.execute_script(f"document.getElementById('from').value = '{_latest_datetime_of_existing_article}';")
        driver.execute_script(f"document.getElementById('until').value = '{todays_date}';")

        driver.find_element(By.CLASS_NAME, 'archive-holder').find_element(By.CLASS_NAME, 'btn').click()
        time.sleep(2)
        pagination_items = []
        try:  
            pagination_items = driver.find_element(By.CLASS_NAME, 'pagination-items').find_elements(By.CLASS_NAME, 'g-button')
            pagination_items = pagination_items[:-1]
            last_pagination_item = pagination_items.pop()
            last_page = int(last_pagination_item.text)
        except Exception as e:
            last_page = 1

        for page in range(last_page):
            try:
                articles = driver.find_element(By.TAG_NAME, 'main').find_elements(By.TAG_NAME, 'article')
                articles_no = len(articles)
                if(articles_no > 0):
                    for article in articles:
                        article_url = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        articles_urls.append(article_url)

                # click next page
                pagination_items = driver.find_element(By.CLASS_NAME, 'pagination-items').find_elements(By.CLASS_NAME, 'g-button')
                next_page = pagination_items.pop()
                next_page.click()
            except Exception as e:
                print("Error: ", e)     

    else:
        time.sleep(2)
        driver.execute_script("document.getElementById('from').value = '2022-11-01';")
        driver.execute_script(f"document.getElementById('until').value = '{todays_date}';")

        driver.find_element(By.CLASS_NAME, 'archive-holder').find_element(By.CLASS_NAME, 'btn').click()
        time.sleep(2)
        pagination_items = driver.find_element(By.CLASS_NAME, 'pagination-items').find_elements(By.CLASS_NAME, 'g-button')
        pagination_items = pagination_items[:-1]
        last_pagination_item = pagination_items.pop()
        last_page = int(last_pagination_item.text)
        for page in range(last_page):
            try:
                articles = driver.find_element(By.TAG_NAME, 'main').find_elements(By.TAG_NAME, 'article')
                articles_no = len(articles)
                if(articles_no > 0):
                    for article in articles:
                        article_url = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        articles_urls.append(article_url)

                # click next page
                pagination_items = driver.find_element(By.CLASS_NAME, 'pagination-items').find_elements(By.CLASS_NAME, 'g-button')
                next_page = pagination_items.pop()
                next_page.click()
            except Exception as e:
                print("Error: ", e)

    for url in articles_urls:
        try:    
            if(url == ""):
                continue

            article_detail = getArticleDetails(url)

            if latest_datetime_of_existing_article is not None:
                latest_datetime_of_existing_article = datetime.strptime(str(latest_datetime_of_existing_article), '%Y-%m-%d %H:%M:%S')
                article_posted_at = datetime.strptime(article_detail.posted_at, '%Y-%m-%d %H:%M:%S')
                if (article_posted_at <= latest_datetime_of_existing_article):
                    break

            rank = utils.checkIfTheArticleContainsKeywords(article_detail)
            if rank == 0:
                print("An article has been skipped. Not a target!")
                continue

            if(article_detail is None):
                print("An article has been skipped. Probblem with setting the article details!")
                continue

            article_detail.rank = rank
            _articleService.InsertArticle(article_detail)

        except Exception as e:
            print("An error has occured, ", e)

    _articleService.CloseConnection()

def getArticleDetails(article_url):
    try:
        driver.get(article_url)
        time.sleep(2)
        article_title = driver.find_element(By.TAG_NAME, 'main').find_element(By.CLASS_NAME, "non-premium").find_element(By.TAG_NAME, 'h1').text
        article_category = driver.find_element(By.TAG_NAME, 'main').find_element(By.CLASS_NAME, "non-premium").find_element(By.CLASS_NAME, 'categ-link').text        
        article_main_photo = driver.find_element(By.TAG_NAME, 'main').find_element(By.TAG_NAME, "figure").find_element(By.TAG_NAME, "img").get_attribute("src")
        article_content = driver.find_element(By.TAG_NAME, "main").find_element(By.TAG_NAME, 'article').text
        article_keywords = driver.find_element(By.TAG_NAME, 'main').find_element(By.CLASS_NAME, 'tags-holder').text
        article_posted_at = driver.find_element(By.CLASS_NAME, 'published-box').find_element(By.TAG_NAME, 'time').text

        article_posted_at = utils.formatTheDateTime_Koha(article_posted_at)

        article_rank = 0
        article = Article.Article(article_title, article_url, article_category,
                                         article_main_photo, article_content,  
                                         article_keywords, article_posted_at, article_rank, web_portal)

        return article
    except Exception as e: 
        print("Error - ", e)
        return None

# ------------------------------------------------------------ M A I N ---------------------------------------------------------

# data = getData()

# ------------------------------------------------------------------------------------------------------------------------------ 