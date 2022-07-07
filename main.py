import sqlite3
user_id = 3
# Create a SQL connection to our SQLite database
con = sqlite3.connect("database.db")

cur = con.cursor()

cur.execute("INSERT INTO posts (title,content,user) VALUES (?,?,?)", ("something", "hello", 2))

cur.execute("SELECT * FROM posts WHERE user = 1;")

try:
    posts = list(cur.fetchall())
except TypeError as err:
    posts = ""
    print("no user found 1")

if posts:
    print(posts)
else:
    print("no posts found 2")



# Be sure to close the connection
con.close()



# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
