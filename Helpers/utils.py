import re
from datetime import timedelta, datetime
import Database.TargetKeywordsService as _targetKeywordService

## Get the target keywords from DB
target_keywords = _targetKeywordService.GetAllTargetKeywords()

def checkIfTheArticleContainsKeywords(article):
    rank = 0
    priorityCoefficient = 10
    article_title = article.title.lower()
    article_content = article.content.lower()
    for keyword in target_keywords:
        ## 1. if the keyword is neither on title and body
        if keyword not in article_title or keyword not in article_content:
            continue

        ## 2. If the keyword is in title but not in body
        elif keyword in article_title and keyword not in article_content:
            rank += len(re.findall(keyword, article_title))/len(article_title)
            rank *= priorityCoefficient

        ## 3. If the keyword is not in title but is in body
        elif keyword not in article_title and keyword in article_content:
            rank += len(re.findall(keyword, article_content))/len(article_content)

        ## 4. If the keyword is in both title and body
        elif keyword in article_title and keyword in article_content:
            rank += len(re.findall(keyword, article_title))
            rank += len(re.findall(keyword, article_content))
            rank *= priorityCoefficient

    return rank

def formatTheDateTime_Telegrafi(posted_at):

    if "orë" in posted_at:
        hours_ = posted_at.split(" ")[0]
        date_ = datetime.today() - timedelta(hours = int(hours_))
        date_ = date_.strftime('%Y-%m-%d %H:%M:%S')

        posted_at = date_
    else:
        _date = posted_at.split("•")[0]
        _day = _date.split(".")[0]
        _month = _date.split(".")[1]
        _year = _date.split(".")[2]
        _time = posted_at.split("•")[1]
        _hour = _time.split(":")[0]
        _minute = _time.split(":")[1]

        posted_at = datetime(int(_year), int(_month), int(_day), int(_hour), int(_minute), 0).strftime('%Y-%m-%d %H:%M:%S')
    
    return posted_at

def formatTheDateTime_Kallxo(posted_at):

    _date = posted_at.split("-")[0]
    _day = _date.split(".")[0]
    _month = _date.split(".")[1]
    _year = _date.split(".")[2]
    _time = posted_at.split("-")[1]
    _hour = _time.split(":")[0]
    _minute = _time.split(":")[1]

    posted_at = datetime(int(_year), int(_month), int(_day), int(_hour), int(_minute), 0).strftime('%Y-%m-%d %H:%M:%S')

    return posted_at

def formatTheDateTime_Koha(posted_at):
        
    date = posted_at.split(",")[0]
    
    _day = date.split(" ")[0]
    _month = date.split(" ")[1]
    if _month == "janar":
        _month = 1
    elif _month == "shkurt":
        _month = 2
    elif _month == "mars":
        _month = 3
    elif _month == "prill":
        _month = 4
    elif _month == "maj":
        _month = 5
    elif _month == "qershor":
        _month = 6
    elif _month == "korrik":
        _month = 7
    elif _month == "gusht":
        _month = 8
    elif _month == "shtator":
        _month = 9
    elif _month == "tetor":
        _month = 10
    elif _month == "nëntor":
        _month = 11
    elif _month == "dhjetor":
        _month = 12
    _year = date.split(" ")[2]

    hours = posted_at.split(",")[1]

    _hour = hours.split(":")[0]
    _minute = hours.split(":")[1]

    posted_at = datetime(int(_year), int(_month), int(_day), int(_hour), int(_minute), 0).strftime('%Y-%m-%d %H:%M:%S')

    return posted_at

def formatTheDateTime_KosovaSot(posted_at):
        
    date = posted_at.split("-")[0]
    
    _day = date.split(" ")[0]
    _month = date.split(" ")[1]
    if _month == "January":
        _month = 1
    elif _month == "February":
        _month = 2
    elif _month == "March":
        _month = 3
    elif _month == "April":
        _month = 4
    elif _month == "May":
        _month = 5
    elif _month == "June":
        _month = 6
    elif _month == "July":
        _month = 7
    elif _month == "August":
        _month = 8
    elif _month == "September":
        _month = 9
    elif _month == "October":
        _month = 10
    elif _month == "November":
        _month = 11
    elif _month == "December":
        _month = 12
    _year = date.split(" ")[2]

    hours = posted_at.split("-")[1]

    _hour = hours.split(":")[0]
    _minute = hours.split(":")[1]

    posted_at = datetime(int(_year), int(_month), int(_day), int(_hour), int(_minute), 0).strftime('%Y-%m-%d %H:%M:%S')

    return posted_at