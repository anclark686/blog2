import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("database.db")

cur = con.cursor()
cur.execute("INSERT INTO posts (title,content) VALUES (?,?)", ("Hello", "something"))
search = '%' + 'app' + '%'
print(search)
# The result of a "cursor.execute" can be iterated over by row
cur.execute('SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?;', (search, search))
posts = list(cur.fetchall())
print("youre here right?")
print(posts)

# Be sure to close the connection
con.close()

# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
