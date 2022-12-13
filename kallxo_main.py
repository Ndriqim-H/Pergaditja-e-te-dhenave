## import libraries
import csv
import time
import os.path
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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
    # for i in range(100):
    #     time.sleep(2)
    #     driver.find_element(By.CLASS_NAME, 'loadmore-inf').click()

    # articles = driver.find_elements(By.CLASS_NAME, 'post_item__thumb')
    articles_list = []
    # articles_urls = []

    # for article in articles:
    #     url = article.find_element(By.TAG_NAME, 'a').get_attribute("href")
    #     articles_urls.append(url)

    # writeUrlsToFile(articles_urls)

    articles_urls = getArticlesUrls()
    for url in articles_urls:
        try:
            if(url == ""):
                continue
            article_detail = getArticleDetails(url)
            if(article_detail is None):
                continue
            articles_list.append(article_detail)
        except Exception as e:
            print("An error has occured, ", e)

    return articles_list

def getArticleDetails(article_url):
    try:
        driver.get(article_url[0])
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

def getArticlesUrls():
    urls = []
    try:
        with open('kallxo_tech_articles_urls.csv', 'r', encoding='utf-8') as file:
            # data = file.read()
            data = csv.reader(file, delimiter = ',')
            for row in data:
                if len(row) <= 0 or row == ['url']: continue
                urls.append(row)
    except:
        print('Error - reading the articles urls')
    return urls

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

