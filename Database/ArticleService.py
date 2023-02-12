import pyodbc
import datetime
import re
# Connect to the database
# cnxn = pyodbc.connect('DRIVER={SQL Server};'
#                       'SERVER=DaBeast;'
#                       'PORT=1433;'
#                       'DATABASE=News_Site;'
#                       'Trusted_Connection=yes')

class dbClass:
    cnxn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=DaBeast;'
                        'PORT=1433;'
                        'DATABASE=News_Site;'
                        'Trusted_Connection=yes')
           

    def InsertArticle(self, article):
        # dbClass.cnxn = dbClass.OpenConnection()
        try:
            cursor = dbClass.cnxn.cursor()
            query = f"INSERT INTO Articles (Title, Url, Category, Main_Photo, Content, Keywords, Posted_At, Rank, Website) VALUES('{article.title}', '{article.url}', '{article.category}', '{article.main_photo}', '{article.content}', '{article.keywords}', '{article.posted_at}', {article.rank}, '{article.website}');"

            cursor.execute(query)

            dbClass.cnxn.commit()
            cursor.close()
            print("An article has been successfully inserted in the DB!")
        except Exception as e:
            print("Error - ", e)
            
    def GetLatestArticleDateTime(self, website):
        try:
            dbClass.cnxn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=DaBeast;'
                        'PORT=1433;'
                        'DATABASE=News_Site;'
                        'Trusted_Connection=yes')
        except Exception as e:
            print("Connection Already exists")
        
        cursor = dbClass.cnxn.cursor()
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

        dbClass.cnxn.commit()
        cursor.close()

        return result

    def OpenConnection(self):
        dbClass.cnxn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=DaBeast;'
                        'PORT=1433;'
                        'DATABASE=News_Site;'
                        'Trusted_Connection=yes')
        # return cnxn


    def GetAllTargetKeywords(self):
        result = []
        cursor = dbClass.cnxn.cursor()

        query = f"SELECT Name FROM TargetKeywords;"

        cursor.execute(query)
        all_rows = cursor.fetchall()
        for row in all_rows:
            row = re.sub(",|\)|\(| ", '', str(row))
            row = re.sub("'", '', str(row))
            result.append(row)

        cursor.close()
        dbClass.cnxn.close()

        return result

    def CloseConnection(self):
        dbClass.cnxn.close()


