from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi

import helpers 
import random

my_id= 8664

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html', page_title= "Hello")

@app.route('/insert/', methods=['GET','POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html', page_title = 'Insert')
    else:
        tt = request.form.get('movie-tt')
        title = request.form.get('movie-title')
        release = request.form.get('movie-release')
        if not tt or not title or not release:
            flash('You are missing an input')
        else:
            try:
                int(tt)
            except:
                flash('The tt you have entered must be an integer')
                return redirect(url_for('insert'))        
            if len(release) > 4:
                flash('The correct date format is: yyyy')
                return redirect(url_for('insert'))
            conn = dbi.connect()
            if len(release) < 4:
                flash('The correct date format is: yyyy')
                return redirect(url_for('insert'))
            conn = dbi.connect()
            if len(helpers.is_movie(conn, tt)) == 0:
                flash('The tt you have entered is a new one, movie has been inserted!')
                helpers.insert_movie(conn, tt, title, release)
                session['title'] = title
                session['release'] = release
                return redirect(url_for('insert', tt = tt))
            else: flash('The tt you entered already exists')
    return redirect(url_for('insert'))

@app.route('/update/<int:tt>', methods=['GET','POST'])
def update(tt):
    if request.method == 'GET':
        title = session.get('title')
        release = session.get('release')
        if session.get('director'):
            director = session.get('director')
        else:
            director = None
        if session.get('addedby'):
            addedby = session.get('addedby')
        else:
            addedby = my_id
        return render_template('update.html', page_title = 'Update', tt = tt, title = title, release = release, director = director, addedby = addedby)
    else:
        new_tt = request.form.get('movie-tt')
        conn = dbi.connect()
        if request.form.get('submit') == 'update':
            title = request.form.get('movie-title')
            release = request.form.get('movie-release')
            director = request.form.get('movie-director')
            addedby = request.form.get('movie-addedby')
            if int(new_tt) != int(tt) and len(helpers.is_movie(conn, new_tt)) != 0:
                flash('Movie already exists')
                return render_template('update.html', page_title = 'Update', tt = tt)
            else:
                helpers.update_movie(conn, tt, new_tt, title, release, director, addedby)
                flash('The movie has been updated successfully')
                return render_template('update.html', tt = new_tt, title = title, release = release, director = director, addedby = addedby)
        elif request.form.get('submit') == 'delete':
            helpers.delete_movie(conn, new_tt)
            flash('The movie has been deleted successfully')
            return redirect(url_for('index')) 

@app.route('/select/', methods=['GET','POST'])
def select():
    if request.method == 'GET':
        conn = dbi.connect()
        movies = helpers.select_movie(conn)
        return render_template('select.html', page_title = 'Incomplete', movies = movies)
    else:
        tt = int(request.form.get('menu-tt'))
        conn = dbi.connect()
        info = helpers.is_movie(conn, tt)[0]
        session['title'] = info['title']
        session['release'] = info['release']
        session['director'] = info['director']
        session['addedby'] = info['addedby']
        return redirect(url_for('update', tt = tt)) 


@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'zy1_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
