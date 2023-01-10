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

tech_allowed_keywords = ["telefon", "post", "operator", "internet", "siguri kiberbetike", "sulm kibernetik", "kibernetik"]

class Article:
    def __init__(self, article_no, id, title, url, category, main_photo, content, video, keywords, comments, posted_at, author_name, author_photo):
        self.article_no = article_no
        self.id = id
        self.title = title
        self.url = url
        self.category = category
        self.main_photo = main_photo
        self.content = content
        self.video = video
        self.keywords = keywords
        self.comments = comments
        self.posted_at = posted_at
        self.author_name = author_name
        self.author_photo = author_photo

driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

def getData():
    ## the tech section on Telegraf
    tech_section_url = "https://kallxo.com/teknologji/"

    delay = 10 # timeout (seconds)

    driver.get(tech_section_url)

    ## redirect to the technology section
    # driver.find_element(By.CLASS_NAME, 'go-to-category').click()

    # try:
    #     WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'lineClamp')))
    #     print ("Page is ready!")
    # except TimeoutException:
    #     print ("Loading took too much time!")

    # load more articles (10 times)
    for i in range(200):
        try:
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'loadmore-inf').click()
        except:
            print("Error, load more could not be found!")
            break
    articles = driver.find_elements(By.CLASS_NAME, 'post_item__thumb')
    articles_titles = driver.find_elements(By.CLASS_NAME, 'post_item__content')
    articles_list = []
    articles_urls = []

    for article, title in zip(articles, articles_titles):
        url = article.find_element(By.TAG_NAME, 'a').get_attribute("href")
        articles_urls.append(url)

    for url in articles_urls:
        try:
            if(url == ""):
                continue
            article_detail = getArticleDetails(url)
            latest_existing_article_datetime = getLatestArticleDateTime()
            if latest_existing_article_datetime is not None:
                latest_existing_article_datetime = datetime.strptime(latest_existing_article_datetime, '%d.%m.%Y %H:%M:%S')
                article_posted_at = datetime.strptime(article_detail.posted_at, '%d.%m.%Y %H:%M:%S')
                if (article_posted_at <= latest_existing_article_datetime):
                    break
            if not checkIfTheArticleContainsKeywords(article_detail.title):
                continue
            if(article_detail is None):
                continue
            articles_list.append(article_detail)
        except Exception as e:
            print("An error has occured, ", e)

    return articles_list

def checkTheLatestExistingArticle(latest_article_datetime):
    pass

def checkIfTheArticleContainsKeywords(title):
    article_title = title.lower()
    for keyword in tech_allowed_keywords:
        if keyword in article_title:
            return True
        else:
            continue
    return False

def getArticleDetails(article_url):
    try:
        driver.get(article_url)
        id = ""
        article_id = ""
        article_title = driver.find_element(By.CLASS_NAME, 'single_article').find_element(By.CLASS_NAME, 'single_article__header').find_element(By.TAG_NAME, "h1").text
        article_category = ""
        article_main_photo = driver.find_element(By.CLASS_NAME, 'single_article__thumb').find_element(By.TAG_NAME, "img").get_attribute("src")
        article_content_list = driver.find_element(By.CLASS_NAME, "single_article__main").find_elements(By.TAG_NAME, "p")
        article_content = ""
        for paragraph in article_content_list:
            article_content += paragraph.text + "\n"
        article_video = ""
        article_keywords = ""
        article_tags = driver.find_element(By.CLASS_NAME, 'post_item__tags').find_elements(By.TAG_NAME, "a")
        for tag in article_tags:
            article_keywords += tag.text + ", "
        article_comments = ""
        article_posted_at = driver.find_element(By.CLASS_NAME, 'post_date').text
        _date = article_posted_at.split("-")[0]
        _day = _date.split(".")[0]
        _month = _date.split(".")[1]
        _year = _date.split(".")[2]

        _time = article_posted_at.split("-")[1]
        _hour = _time.split(":")[0]
        _minute = _time.split(":")[1]

        article_posted_at = datetime(int(_year), int(_month), int(_day), int(_hour), int(_minute), 0).strftime('%d.%m.%Y %H:%M:%S')
        # article_posted_at = article_posted_at if "orë" not in article_posted_at else (article_posted_at + " më parë")
        article_author_name = driver.find_element(By.CLASS_NAME, 'single_article__author__name').text
        # article_author_photo = driver.find_element(By.CLASS_NAME, 'single_article__author__thumb').find_element(By.TAG_NAME, "img").get_attribute("src")
        article_author_photo = ""
        article = Article(id, article_id, article_title, article_url, article_category,
                        article_main_photo, article_content, article_video,  
                        article_keywords, article_comments, article_posted_at, article_author_name, article_author_photo)

        return article
    except:
        print("Error!")
        return None

def writeUrlsToFile(urls):
    with open('kallxo_tech_articles_urls.csv', 'w', encoding='utf-8') as file:
            try:                
                writer = csv.writer(file)
                writer.writerow(url_column)
                for url in urls:
                    row = [url]
                    writer.writerow(row)
            except:
                print("Error - writing url to csv file")

def getLatestArticleDateTime():
    posted_at_datetimes = []
    try:
        with open('kallxo_tech_articles.csv', 'r', encoding='utf-8') as file:
            # data = file.read()
            data = csv.reader(file, delimiter = ',')
            for row in data:
                if len(row) <= 0 or "posted_at" in row: continue
                posted_at_datetimes.append(row[9])
    except:
        return None
    return posted_at_datetimes[0]

def writeToFile(data): 
    file_exists = os.path.exists('kallxo_tech_articles.csv')
    if file_exists:
        with open('kallxo_tech_articles.csv', 'a', encoding='utf-8') as file:
            try:
                writer = csv.writer(file)
                for article in data:
                    article = [id(article), article.title, article.url, article.category, article.main_photo, article.content, 
                                article.video, article.keywords, article.comments, article.posted_at, article.author_name, article.author_photo]
                    writer.writerow(article)
            except:
                print('Error - updating to csv file')
    else:
        with open('kallxo_tech_articles.csv', 'w', encoding='utf-8') as file:
            try:                
                writer = csv.writer(file)
                writer.writerow(columns)
                for article in data:
                    article = [id(article), article.title, article.url, article.category, article.main_photo, article.content, 
                                article.video, article.keywords, article.comments, article.posted_at, article.author_name, article.author_photo]
                    writer.writerow(article)
            except:
                print("Error - writing to csv file")

# Columns of the dataset
columns = ['id', 'title', 'url', 'category', 'main_photo', 'content', 'video', 'keywords', 'comments', 'posted_at', 'author_name', 'author_photo']
url_column = ['url']

# The actual data
data = getData()

# Writing the data to a csv file
writeToFile(data)

