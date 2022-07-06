import sqlite3


def connect_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)')
    print("Table created successfully")


def get_posts(search=""):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if search == "":
        cur.execute("SELECT * FROM posts")
        posts = list(cur.fetchall())
    else:
        search = '%' + search + '%'
        cur.execute('SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?;', (search, search))
        posts = list(cur.fetchall())

    return posts

