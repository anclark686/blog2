import sqlite3
from passlib.hash import sha256_crypt


def connect_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users '
                 '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                 'name TEXT NOT NULL, '
                 'username TEXT NOT NULL UNIQUE, '
                 'password TEXT NOT NULL);')
    print("User Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS posts '
                 '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                 'title TEXT NOT NULL, '
                 'content TEXT NOT NULL,'
                 'user INTEGER, FOREIGN KEY(user) REFERENCES users(id));')
    print("Posts Table created successfully")


def insert_user(name, username, password):
    user_id = 0
    msg = ""
    password = sha256_crypt.encrypt(password)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO users (name, username, password) VALUES (?,?,?)", (name, username, password))
        con.commit()
        user_id = cur.lastrowid
        print("User entered successfully")
    except sqlite3.IntegrityError:
        msg = "Username already exists"
    finally:
        con.close()

        return msg, user_id


def retrieve_user(username, password):
    status = ""
    user_id = 0
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    try:
        user = cur.fetchone()
        if sha256_crypt.verify(password, user[3]):
            status = "success"
            user_id = user[0]
        else:
            status = "Invalid Password, please try again"
    except TypeError as err:
        status = "User not found. Please check your username and try again."
    finally:
        con.close()
        return status, user_id


def retrieve_user_by_id(user_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    try:
        user = cur.fetchone()
        return user
    except TypeError as err:
        return None


def get_posts(user_id, search=""):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if search == "":
        cur.execute("SELECT * FROM posts WHERE user = ?", (user_id,))
        posts = list(cur.fetchall())
    else:
        search = '%' + search + '%'
        cur.execute('SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?;',
                    (search, search))
        posts = list(cur.fetchall())

    return posts

