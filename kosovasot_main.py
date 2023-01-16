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

tech_allowed_keywords = ["telefon", "post", "operator", "internet", "siguri kiberbetike", "sulm kibernetik", "kibernetik","teknologji","teknologjia","rrjet","wifi","rrjetet sociale"]

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

driver = webdriver.Chrome(executable_path=r"./chromedriver.exe--incognito")
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

def getData():
    ## the tech section on Telegraf
    tech_section_url = "https://www.kosova-sot.info/auto-tech/"

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
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn-primary').click()

    for i in range(100):
        try:
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'more-ajax').click()
        except:
            print("Error, load more could not be found!")
            break
    articles = driver.find_elements(By.CLASS_NAME, 'news-md')
    articles_titles = driver.find_elements(By.CLASS_NAME, 'news-md')
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
        article_title = driver.find_element(By.CLASS_NAME, 'main-title')
        article_title = article_title.text
        article_category = ""
        article_main_photo = driver.find_element(By.CLASS_NAME, 'main-img').find_element(By.TAG_NAME, 'img').get_attribute("src")
        article_content_list = driver.find_elements(By.CSS_SELECTOR, ".news-content > p")
        article_content = ""
        for paragraph in article_content_list:
            article_content += paragraph.text + "\n"
        
        article_content = article_content.replace("\n", " ")
        article_video = ""
        article_keywords = ""
        article_tags = ""
        #for tag in article_tags:
            #article_keywords += tag.text + ", "
        article_comments = ""
        article_posted_at = article_posted_at = date_element = driver.find_element(By.CSS_SELECTOR, "ul.published-info li:nth-of-type(2)").text
        
        date_time_obj = datetime.strptime(article_posted_at, '%d %B %Y - %H:%M')
        formatted_date_string = date_time_obj.strftime("%d.%m.%Y %H:%M:%S")
        print(formatted_date_string)
        

        article_posted_at = formatted_date_string
        # article_posted_at = article_posted_at if "orë" not in article_posted_at else (article_posted_at + " më parë")
        article_author_name = ""
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
    with open('kosova.csv', 'w', encoding='utf-8') as file:
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
        with open('kosova.csv', 'r', encoding='utf-8') as file:
            # data = file.read()
            data = csv.reader(file, delimiter = ',')
            for row in data:
                if len(row) <= 0 or "posted_at" in row: continue
                posted_at_datetimes.append(row[9])
    except:
        return None
    if len(posted_at_datetimes) > 0:
        return posted_at_datetimes[0]
    return None

def writeToFile(data): 
    file_exists = os.path.exists('kosova.csv')
    if file_exists:
        with open('kosova.csv', 'a', encoding='utf-8') as file:
            try:
                writer = csv.writer(file)
                for article in data:
                    article = [id(article), article.title, article.url, article.category, article.main_photo, article.content, 
                                article.video, article.keywords, article.comments, article.posted_at, article.author_name, article.author_photo]
                    writer.writerow(article)
            except:
                print('Error - updating to csv file')
    else:
        with open('kosova.csv', 'w', encoding='utf-8') as file:
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

