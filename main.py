import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("database.db")

cur = con.cursor()
cur.execute("INSERT INTO posts (title,content) VALUES (?,?)", ("Hello", "something"))

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM posts;'):
    print(row)

# Be sure to close the connection
con.close()

# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
