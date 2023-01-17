import pyodbc

# Connect to the database
cnxn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=.\;'
                      'DATABASE=News_Site;'
                      'Trusted_Connection=yes')

def InsertArticle(article): 
    # Create a cursor
    cursor = cnxn.cursor()

    # Use the cursor to execute an INSERT statement to save the object
    cursor.execute("INSERT INTO Articles (Title, Url, Category, Main_Photo, Content, Keywords, Posted_At, Rank) ", 
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                            article["Title"], 
                            article["Url"],
                            article["Category"],
                            article["Main_Photo"],
                            article["Content"],
                            article["Keywords"],
                            article["Posted_At"],
                            article["Rank"])

    # Commit the transaction
    cnxn.commit()

    # Close the cursor and connection
    cursor.close()
    cnxn.close()

