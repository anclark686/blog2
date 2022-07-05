from flask import Flask, render_template, request, redirect, url_for
from utils import db
import sqlite3

app = Flask(__name__)

db.connect_db()

@app.route('/')
def home():
    posts = db.get_posts()
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = db.get_posts()
    post = ""
    for i in posts:
        if post_id == i[0]:
            post = i
    if not post:
        return render_template('404.html', message=f'A post with id {post_id} was not found.')
    return render_template('post.html', post=post)


@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO posts (title,content) VALUES (?,?)", (title, content))

                con.commit()
                msg = "Record Successfully added"
                print(msg)
        except:
            con.rollback()
            msg = "Error in insert operation"
            print(msg)

        finally:
            return redirect(url_for('post', post_id=cur.lastrowid))
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
