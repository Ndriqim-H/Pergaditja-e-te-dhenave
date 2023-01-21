## import libraries
import time
import re
from datetime import timedelta, datetime
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

## import the other modules
import Database.ArticleService as ArticleService
import Database.TargetKeywordsService as TargetKeywordService
import Models.Article as Article


tech_allowed_keywords = TargetKeywordService.GetAllTargetKeywords()

driver = webdriver.Chrome(executable_path=r"C:\webdrivers.exe")
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

def getData():
    ## the tech section on Telegraf
    tech_section_url = "https://www.koha.net/arkivi/?acid=tech"
    website = "Koha"
    latest_existing_article_datetime = ArticleService.GetLatestArticleDateTime(website)

    delay = 10 # timeout (seconds)

    driver.get(tech_section_url)

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    # select the datetime range
    driver.find_element(By.CLASS_NAME, 'form-control').click()

    # load more articles
    for i in range(3):
        time.sleep(2)
        try:
            driver.find_element(By.CLASS_NAME, 'load-more').click()
        except:
            print("Error, load more could not be found!")
            break

    articles = driver.find_elements(By.CLASS_NAME, 'fcArticle')
    articles_urls = []

    for article in articles:
        url = article.find_element(By.TAG_NAME, 'a').get_attribute("href")
        articles_urls.append(url)
    

    for url in articles_urls:
        try:    
            if(url == ""):
                continue

            article_detail = getArticleDetails(url)

            if latest_existing_article_datetime is not None:
                latest_existing_article_datetime = datetime.strptime(str(latest_existing_article_datetime), '%Y-%m-%d %H:%M:%S')
                article_posted_at = datetime.strptime(article_detail.posted_at, '%Y-%m-%d %H:%M:%S')
                if (article_posted_at <= latest_existing_article_datetime):
                    break
            rank = checkIfTheArticleContainsKeywords(article_detail)
            if rank == 0:
                print("An article has been skipped. Not a target!")
                continue
            if(article_detail is None):
                print("An article has been skipped. Probblem with setting the article details!")
                continue

            article_detail.rank = rank
            ArticleService.InsertArticle(article_detail)

        except Exception as e:
            print("An error has occured, ", e)

    ArticleService.CloseConnection()


def checkIfTheArticleContainsKeywords(article):
    rank = 0
    priorityCoefficient = 10
    article_title = article.title.lower()
    article_content = article.content.lower()
    for keyword in tech_allowed_keywords:
        ## 1. if the keyword is neither on title and body
        if keyword not in article_title or keyword not in article_content:
            continue

        ## 2. If the keyword is in title but not in body
        elif keyword in article_title and keyword not in article_content:
            rank += len(re.findall(keyword, article_title))
            rank *= priorityCoefficient

        ## 3. If the keyword is not in title but is in body
        elif keyword not in article_title and keyword in article_content:
            rank += len(re.findall(keyword, article_content))

        ## 4. If the keyword is in both title and body
        elif keyword in article_title and keyword in article_content:
            rank += len(re.findall(keyword, article_title))
            rank += len(re.findall(keyword, article_content))
            rank *= priorityCoefficient

    return rank

def getArticleDetails(article_url):
    try:
        driver.get(article_url)
        time.sleep(2)
        article_title = driver.find_element(By.CLASS_NAME, 'article-heading').find_element(By.TAG_NAME, "h1").text
        article_category = driver.find_element(By.CLASS_NAME, 'article-category').text
        article_main_photo = driver.find_element(By.CLASS_NAME, 'featured-image').find_element(By.TAG_NAME, "figure").find_element(By.TAG_NAME, "img").get_attribute("src")
        article_content = driver.find_element(By.CLASS_NAME, "article-body").text
        article_keywords = driver.find_element(By.CLASS_NAME, "article-tags").text
        article_posted_at = driver.find_element(By.CLASS_NAME, 'article-posted').text
        if "orë" in article_posted_at:
            hours_ = article_posted_at.split(" ")[0]
            date_ = datetime.today() - timedelta(hours = int(hours_))
            date_ = date_.strftime('%Y-%m-%d %H:%M:%S')
            article_posted_at = date_
        else:
            _date = article_posted_at.split("•")[0]
            _day = _date.split(".")[0]
            _month = _date.split(".")[1]
            _year = _date.split(".")[2]

            _time = article_posted_at.split("•")[1]
            _hour = _time.split(":")[0]
            _minute = _time.split(":")[1]

            article_posted_at = datetime(int(_year), int(_month), int(_day), int(_hour), int(_minute), 0).strftime('%Y-%m-%d %H:%M:%S')
        article_rank = 0
        website = "Telegrafi"
        article = Article.Article(article_title, article_url, article_category,
                                         article_main_photo, article_content,  
                                         article_keywords, article_posted_at, article_rank, website)

        return article
    except Exception as e: 
        print("Error - ", e)
        return None

# ------------------------------------------------------------ M A I N ---------------------------------------------------------

data = getData()

# ------------------------------------------------------------------------------------------------------------------------------ 