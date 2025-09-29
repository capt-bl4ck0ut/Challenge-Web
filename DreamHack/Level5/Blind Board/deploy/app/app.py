#!/usr/bin/env python3
import os
import pymysql
from flask import Flask, abort, redirect, render_template, request, session
from threading import RLock

PAGINATION_SIZE = 10
DATABASE_SIZE_THRESHOLD = 10 * 1024 * 1024
SQL_BAN_LIST = [
    'alter', 'create', 'cursor', 'delete', 'drop', 'exec', 'fetch', '!', '"',
    '$', '%', '&', '+', '.', ':', '<', '>', '?', '@', '[', '\\', ']', '^', '_',
    '`', '|', '~', 'sleep', 'table', 'delay', 'wait', 'union', 'describe',
    'database', 'declare', 'set', 'count', 'benchmark', 'extract', 'update',
    'insert'
]

app = Flask(__name__)
app.secret_key = os.urandom(32)

def connect_mysql():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user=os.environ['MYSQL_USER'],
                         passwd=os.environ['MYSQL_PASSWORD'],
                         db='blind_board_db',
                         charset='utf8')
    cursor = db.cursor()
    return db, cursor

def check_session():
    if not session:
        abort(403)

def check_database_size_threshold():
    file_size = 0
    file_size += os.path.getsize('/var/lib/mysql/blind_board_db/users.ibd')
    file_size += os.path.getsize('/var/lib/mysql/blind_board_db/articles.ibd')
    if file_size <= DATABASE_SIZE_THRESHOLD:
        return True
    return False

def check_query_ban_list(query):
    for banned in SQL_BAN_LIST:
        if banned in query.lower():
            return False
    return True

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global cursor, db

    if request.method == 'GET':
        return render_template('login.html')

    # POST
    username = request.form['username']
    password = request.form['password']

    # Query the user account.
    try:
        query = 'SELECT * FROM users WHERE uid = %s AND upw = %s'
        with lock:
            cursor.execute(query, (username, password, ))
            ret = cursor.fetchone()
    except:
        db.close()
        db, cursor = connect_mysql()
        query = 'SELECT * FROM users WHERE uid = %s AND upw = %s'
        with lock:
            cursor.execute(query, (username, password, ))
            ret = cursor.fetchone()

    # Set session and redirect if success; 401 if failure.
    if ret:
        session['logged_in'] = True
        session['username'] = username
        return redirect('/board')
    abort(401)

@app.route('/board', methods=['GET'])
def board():

    check_session()

    # Validate query argument 'page'.
    page = request.args.get('page')
    page = int(page) if page and page.isdigit() and int(page) > 0 else 1

    # Show unrecognizable board for non-admin users.
    if session['username'] != 'admin':
        ret = [(i, '*' * 39) for i in range(10, 0, -1)]
        return render_template('board.html', page=page, ret=ret)

    # Show the board by pagination.
    query = 'SELECT idx, title FROM articles ORDER BY idx DESC LIMIT %s, %s'
    with lock:
        cursor.execute(query, ((page - 1) * PAGINATION_SIZE, PAGINATION_SIZE, ))
        ret = cursor.fetchall()
    return render_template('board.html', page=page, ret=ret)

@app.route('/board/<article_id>', methods=['GET'])
def board_article(article_id):

    check_session()

    # Show unrecognizable article for non-admin users.
    if session['username'] != 'admin':
        return render_template('article.html',
                               article_id=article_id,
                               content='*' * 1390,
                               title='*' * 39)

    # Validate path argument 'article_id'.
    if not article_id or not article_id.isdigit() or int(article_id) < 1:
        abort(400)

    # Query the article.
    query = 'SELECT title, content FROM articles WHERE idx = %s'
    with lock:
        cursor.execute(query, (article_id, ))
        ret = cursor.fetchone()

    # Show the article if exists; 404 if not exist.
    if ret:
        return render_template('article.html',
                               article_id=article_id,
                               content=ret[1],
                               title=ret[0])
    abort(404)

@app.route('/write_article', methods=['POST'])
def write_article():

    check_session()

    # Show article writing page if title or content are not given.
    if 'title' not in request.form or 'content' not in request.form:
        return render_template('write_article.html')

    if not check_database_size_threshold():
        return render_template('error.html',
                               error=500,
                               msg='database size exceeded xd'), 500

    # Create a article.
    title = request.form['title']
    content = request.form['content']

    try:
        query = 'INSERT INTO articles (title, content) VALUES (\'{0}\', \'{1}\')'
        query = query.format(title, content)
        if check_query_ban_list(title) and check_query_ban_list(content):
            with lock:
                cursor.execute(query)
                db.commit()
    except:
        pass

    # Go back to the board.
    return redirect('/board')

@app.route('/modify_article', methods=['POST'])
def modify_article():

    check_session()

    article_id = request.form['article_id']

    # Show unrecognizable article edit page for non-admin users.
    if session['username'] != 'admin':
        if 'title' not in request.form or 'content' not in request.form:
            return render_template('modify_article.html',
                                   article_id=article_id,
                                   content='*' * 1390,
                                   title='*' * 39)

        return redirect('/board/{0}'.format(article_id))

    # Validate path argument 'article_id'.
    if not article_id or not article_id.isdigit() or int(article_id) < 1:
        abort(400)

    # Show article edit page if title or content are not given.
    if 'title' not in request.form or 'content' not in request.form:
        query = 'SELECT title, content FROM articles WHERE idx = %s'
        with lock:
            cursor.execute(query, (article_id, ))
            ret = cursor.fetchone()
        if ret:
            return render_template('modify_article.html',
                                   article_id=article_id,
                                   content=ret[1],
                                   title=ret[0])
        abort(404)

    # Update the article.
    query = 'UPDATE articles SET title=\'{0}\', content=\'{1}\' WHERE idx = {2}'
    query = query.format(request.form['title'],
                         request.form['content'],
                         article_id)
    with lock:
        cursor.execute(query)
        db.commit()
    return redirect('/board/{0}'.format(article_id))


@app.route('/delete_article', methods=['POST'])
def delete_article():

    check_session()

    # Validate path argument 'article_id'.
    article_id = request.form['article_id']
    if not article_id or not article_id.isdigit() or int(article_id) < 1:
        abort(400)

    # Ask user to confirm article deletion if answer is not given.
    if 'answer' not in request.form:
        return render_template('delete_article.html', article_id=article_id)

    # Delete the article if answer is yes.
    if request.form['answer'] == 'y':
        query = 'DELETE FROM articles WHERE idx = %s'
        with lock:
            cursor.execute(query, (article_id, ))
            db.commit()
        query = 'OPTIMIZE TABLE articles'
        with lock:
            cursor.execute(query)
            db.commit()
        return redirect('/board')

    # Go back to the article if answer is no.
    redirect('/board/{0}'.format(article_id))

@app.errorhandler(400)
def something_wrong(error):
    return render_template('error.html',
                           error=400,
                           msg='something wrong xd'), 400

@app.errorhandler(401)
def failed(error):
    return render_template('error.html',
                           error=401,
                           msg='failed xd'), 401

@app.errorhandler(403)
def required_to_login(error):
    return render_template('error.html',
                           error=403,
                           msg='required to login xd'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',
                           error=404,
                           msg='page not found xd'), 404

if __name__ == '__main__':
    lock = RLock()
    db, cursor = connect_mysql()
    app.run(host='0.0.0.0', port=8000)
    db.close()
