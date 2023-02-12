import pyodbc
import re 
from ArticleService import dbClass
# Connect to the database
# cnxn = pyodbc.connect('DRIVER={SQL Server};'
#                       'SERVER=Ndriqa\SQLEXPRESS;'
#                       'PORT=1433;'
#                       'DATABASE=News_Site;'
#                       'Trusted_Connection=yes')
cnxn = dbClass.cnxn

def GetAllTargetKeywords():
    result = []
    cursor = cnxn.cursor()

    query = f"SELECT Name FROM TargetKeywords;"

    cursor.execute(query)
    all_rows = cursor.fetchall()
    for row in all_rows:
        row = re.sub(",|\)|\(| ", '', str(row))
        row = re.sub("'", '', str(row))
        result.append(row)

    cursor.close()
    cnxn.close()

    return result

test = GetAllTargetKeywords()
print("asda")