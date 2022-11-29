## import libraries
import csv
import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Article:
    def __init__(self, article_no, id, title, url, category, main_photo, content, video, keywords, comments, posted_at):
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

driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

def getData():
    ## the tech section on Telegraf
    tech_section_url = "https://telegrafi.com/teknologji/"

    delay = 10 # timeout (seconds)

    driver.get(tech_section_url)

    ## redirect to the technology section
    driver.find_element(By.CLASS_NAME, 'go-to-category').click()

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'lineClamp')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    ## load more articles (10 times)
    for i in range(10):
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'load-more').click()

    articles = driver.find_elements(By.CLASS_NAME, 'fcArticle')
    articles_list = []
    articles_urls = []
    for article in articles:
        url = article.find_element(By.TAG_NAME, 'a').get_attribute("href")
        articles_urls.append(url)

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
        driver.get(article_url)
        time.sleep(1)
        id = ""
        article_id = ""
        article_title = driver.find_element(By.CLASS_NAME, 'article-heading').find_element(By.TAG_NAME, "h1").text
        article_category = driver.find_element(By.CLASS_NAME, 'article-category').text
        article_main_photo = driver.find_element(By.CLASS_NAME, 'featured-image').find_element(By.TAG_NAME, "figure").find_element(By.TAG_NAME, "img").get_attribute("src")
        article_content = driver.find_element(By.CLASS_NAME, "article-body").text
        article_video = ""
        article_keywords = driver.find_element(By.CLASS_NAME, "article-tags").text
        article_comments = ""
        article_posted_at = driver.find_element(By.CLASS_NAME, 'article-posted').text
        article_posted_at = article_posted_at if "orë" not in article_posted_at else (article_posted_at + " më parë")

        article = Article(id, article_id, article_title, article_url, article_category,
                        article_main_photo, article_content, article_video,  
                        article_keywords, article_comments, article_posted_at)

        return article
    except:
        print("Error!")
        return None

def writeToFile(data): 
    with open('tech_articles.csv', 'w', encoding='utf-8') as file:
        try:                
            writer = csv.writer(file)
            writer.writerow(columns)
            article_no = 0
            for article in data:
                article_no += 1
                article = [article_no, id(article), article.title, article.url, article.category, article.main_photo, article.content, 
                            article.video, article.keywords, article.comments, article.posted_at]
                writer.writerow(article)
        except:
            print("Error - writing to file")

# -------------------------------------------------------------- M A I N ---------------------------------------------------------

# Columns of the dataset
columns = ['article_no', 'id', 'title', 'url', 'category', 'main_photo', 'content', 'video', 'keywords', 'comments', 'posted_at']

# The actual data
data = getData()

# Writing the data to a csv file
writeToFile(data)

# -------------------------------------------------------------------------------------------------------------------------------- 