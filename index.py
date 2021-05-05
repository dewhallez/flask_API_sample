import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, abort, jsonify
from contextlib import closing



#Config
DATABASE = '/tmp/api.db'
app = Flask(__name__)
app.config.from_object(__name__)



#Methods and routes below

# Connect to Database 
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# initialize database 
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# request connection to db
@app.before_request
def before_request():
    g.db = connect_db()

#close connection to db
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


#route into app
@app.route('/')
def get_posts():
    cur = g.db.execute('select title, text from posts order by id desc')
    posts = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_posts.html', posts=posts)


#API response to get posts
@app.route('/api/v1/posts/', methods=['GET'])
def show_entries():
    cur = g.db.execute('select title, text from posts order by id desc')
    posts = [dict(tittle=row[0], text=row[1])
    for row in cur.fetchall()]
    return jsonify({'count': len(posts), 'posts': posts})


#Get specific post from database
@app.route('/api/v1/posts/<int:post_id>', methods=['GET', 'DELETE'])
def single_post(post_id):
    method = request.method
    if method == 'GET':
        cur = g.db.execute('select title, text from posts where id=?', [post_id])
        post = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
        return jsonify({'count': len(posts), 'posts': posts})
    elif method == 'DELETE':
        g.db.execute('delete from posts where id=?', [post_id])
        return jsonify({'status': 'Post Deleted'})



if __name__ == '__main__':
    app.run(debug=True)

