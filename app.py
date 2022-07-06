from flask import Flask, render_template, request, redirect, url_for, session, g
from utils import db
import sqlite3
import time
# from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "somesecretkeythatonlyIshouldknow"


db.connect_db()
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = db.retrieve_user_by_id(int(str(session)[32:-2]))
        g.user = user
    print(g.user)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username'].lower()
        password = request.form['password']
        msg, user_id = db.insert_user(name, username, password)
        if not msg:
            session.pop('user_id', None)
            session['user_id'] = user_id
            user = db.retrieve_user_by_id(user_id)
            g.user = user
            return home(from_logreg=True)
        else:
            return render_template('register.html',
                                   msg=msg,
                                   name=name,
                                   username=username,
                                   password=password)
    else:
        return render_template('register.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        msg, user_id = db.retrieve_user(username, password)
        session.pop('user_id', None)
        if msg == "success":
            session['user_id'] = user_id
            user = db.retrieve_user_by_id(user_id)
            g.user = user

            return home(from_logreg=True)
        else:
            return render_template('login.html', msg=msg, username=username, password=password)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    g.user = None
    return render_template('welcome.html')


@app.route('/home',  methods=['GET', 'POST'])
def home(from_logreg=False):
    if 'user_id' not in session:
        return render_template('welcome.html')
    if request.method == 'POST' and not from_logreg:
        try:
            posts = db.get_posts(g.user[0])
            search_input = request.form.get('search_input')
            search_posts = db.get_posts(search_input)
            return render_template('home.html', posts=search_posts)
        except Exception as e:
            return str(e)
    posts = db.get_posts(g.user[0])
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = db.get_posts(g.user[0])
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
                cur.execute("INSERT INTO posts (title,content, user) VALUES (?,?,?)", (title, content, g.user[0]))

                con.commit()
                msg = "Record Successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            return redirect(url_for('post', post_id=cur.lastrowid))
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
