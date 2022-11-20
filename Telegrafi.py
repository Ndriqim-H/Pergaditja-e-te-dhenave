import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



def writeToFile():

    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://telegrafi.com"
    delay = 3 # seconds
    

    browser = webdriver.Chrome(executable_path=r"./chromedriver.exe")
    browser.get(url)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'lineClamp')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
        
    # html = browser.page_source
    # url = "https://old.reddit.com/r/"+subreddit+"/"+sort_by.lower()
    # page = requests.get(url)

    # soup = BeautifulSoup(page.content, 'html.parser')
    
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    html = list(soup.children)[0]
    body = list(html.children)[2]

    posts = (body.find_all(True, {'class': ['aktualeInfo']}))
    strongs = body.find_all("strong")


    aktuale_more = body.find_all("a", {'class': "aktualeMore"})

    aktuale_more_titles = []
    for a in aktuale_more:
        aktuale_more_titles.append(a.get_text())


    # aktuale_strongs = aktuale[0].find_all("strong")

    strong_titles = []
    for strong in strongs:
        if(strong.get("data-vr-headline")==""):
            strong_titles.append(strong.get_text())
    
    span_titles = []
    spans = body.find_all("span")
    for span in spans:
        if(span.get("data-vr-headline")==""):
            span_titles.append(span.get_text())
    
    latest_news = body.find_all("div", {'class': "tfunditBallina"})[1]
    latest_news_list = latest_news.find_all("ul")[0]
    latest_news_links = latest_news_list.find_all("a")
    
    most_read = body.find_all("div", {'class': "mostRead-balline"})[1]
    most_read_list = most_read.find_all("ul")[0]
    most_read_links = most_read_list.find_all("a")

    opinions = body.find_all("div", {'class': "opinione-balline"})[0]
    opinions_list = opinions.find_all("ul")[0]
    opinions_links = opinions_list.find_all("a")


    interviews = body.find_all("div", {'class': "intervista-balline"})[0]
    interviews_list = interviews.find_all("ul")[0]
    interviews_links = interviews_list.find_all("a")


    videos = body.find_all("div", {'class': "video-widget"})[0]
    videos_list = videos.find_all("ul")[0]
    videos_links = videos_list.find_all("a")


    arr =[]
    for list1 in [latest_news_links,most_read_links,opinions_links,interviews_links,videos_links]:
        for i in list1:
            j = i.get_text().replace("\n", "")
            arr.append(re.sub("\d+ min ", "",j))
    
    all_titles = strong_titles + span_titles + arr
    if not posts:
        return {}

    titles = []
    authors = []
    comments = []
    likes = []

    for post in posts:
        titles.append(post.find(class_='title').get_text())
        authors.append(post.find(class_='author').get_text())

        if not(post.find(class_='comments') is None):

            comment_count = (post.find(class_='comments').text).split(" ")[0]
            if (comment_count == 'comment'):
                comment_count = '0'
        else:
            comment_count = '0'

        comments.append(comment_count)
        if (post.find("div", attrs={"class": "score likes"}) is None):
            like_count = 0
            likes.append(like_count)
        else:
            like_count = post.find(
                "div", attrs={"class": "score likes"}).text.lower()

            if like_count == "•":
                likes.append(0)
            elif(like_count.islower()):
                like_count = like_count.replace('k', '')
                likes.append(int(float(like_count)*1000))
            else:
                likes.append(int(like_count))

    return {"Titles": titles, "Authors": authors, "Comments": comments, "Likes": likes}

print(writeToFile())