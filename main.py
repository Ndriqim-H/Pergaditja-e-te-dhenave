## import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv
import time
import undetected_chromedriver as uc
from selenium import webdriver



class Article:

    def __init__(self, article_no, id, title, category, main_photo, content, video, keywords, comments, posted_at):
        self.article_no = article_no
        self.id = id
        self.title = title
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

    ## load more articles (50 times)
    for i in range(1):
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'load-more').click()

    ## BeautifulSoup 
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # html = list(soup.children)[0]
    # body = list(html.children)[2]
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
            articles_list.append(article_detail)
        except Exception as e:
            print("An error has occured, ", e)

    return articles_list

def getArticleDetails(article_url):
    try:
        driver.get(article_url)
        id = ""
        article_id = ""
        article_title = driver.find_element(By.CLASS_NAME, 'article-heading').find_element(By.TAG_NAME, "h1").text
        article_category = driver.find_element(By.CLASS_NAME, 'article-category').text
        article_main_photo = ""
        # article_main_photo = driver.find_element(By.CLASS_NAME, 'featured-image')
        # article_main_photo = body.find_all({"class":"featured-image"})
        article_content = driver.find_element(By.CLASS_NAME, "article-body").text
        article_video = ""
        article_keywords = driver.find_element(By.CLASS_NAME, "article-tags").text
        article_comments = ""
        article_posted_at = driver.find_element(By.CLASS_NAME, 'article-posted').text

        article = Article(id, article_id, article_title, article_category,
                        article_main_photo, article_content, article_video,  
                        article_keywords, article_comments, article_posted_at)

        return article
    except:
        print("Error!")

def writeToFile(data): 
    with open('tech_articles.csv', 'w', encoding='utf-8') as file:
        try:                
            writer = csv.writer(file)
            writer.writerow(columns)
            article_no = 0
            for article in data:
                article_no += 1
                article = [article_no, id(article), article.title, article.category, article.main_photo, article.content, 
                            article.video, article.keywords, article.comments, article.posted_at]
                writer.writerow(article)
        except:
            print("Error - writing to file")

# Columns of the dataset
columns = ['article_no', 'id', 'title', 'category', 'main_photo', 'content', 'video', 'keywords', 'comments', 'posted_at']

# The actual data
data = getData()

writeToFile(data)

