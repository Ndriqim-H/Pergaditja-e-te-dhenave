import pyodbc
import datetime
import re
# Connect to the database
cnxn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=Ndriqa\SQLEXPRESS;'
                      'PORT=1433;'
                      'DATABASE=News_Site;'
                      'Trusted_Connection=yes')

def InsertArticle(article): 
    try:
        cursor = cnxn.cursor()
        query = f"INSERT INTO Articles (Title, Url, Category, Main_Photo, Content, Keywords, Posted_At, Rank, Website) VALUES('{article.title}', '{article.url}', '{article.category}', '{article.main_photo}', '{article.content}', '{article.keywords}', '{article.posted_at}', {article.rank}, '{article.website}');"

        cursor.execute(query)

        cnxn.commit()
        cursor.close()
        print("An article has been successfully inserted in the DB!")
    except Exception as e:
        print("Error - ", e)
        
def GetLatestArticleDateTime(website):
    cursor = cnxn.cursor()
    query = f"SELECT TOP 1 Posted_at FROM Articles WHERE Website = '{website}' ORDER BY Posted_At DESC;"
          
    cursor.execute(query)

    result = cursor.fetchone()
    if result is None:
        return None

    date_params = re.sub("\)|\(| ", '', str(result))
    date_params = date_params.replace("datetime.datetime", "").split(",")

    year = int(date_params[0])
    month = int(date_params[1])
    day = int(date_params[2])
    hour = int(date_params[3])
    minute = int(date_params[4])
    second = 0

    result = datetime.datetime(year, month, day, hour, minute, second)

    cnxn.commit()
    cursor.close()

    return result

def CloseConnection():
    cnxn.close()

