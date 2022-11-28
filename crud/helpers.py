import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.



def is_movie(conn, tt):
    '''Returns the title, release date, director and addedby of a chosen movie in
    the movie table, as a list of dictionaries.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select title, `release`, director, addedby
        from movie
        where tt = %s''', (tt))
    return curs.fetchall()

def insert_movie(conn, tt, title, release):
    '''Inserts a movie into the movie table 
    with the specified values of tt, title, release date, director.
    Commits changes to the database. 
     '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        insert into movie(tt, title, `release`)
        values (%s, %s, %s)''', [tt, title, release]
    ) 
    conn.commit()
    return

def update_movie(conn, tt, newtt, title, release, director, addedby):
    '''Updates a movie in the movie table 
    with the specified values of tt, title, release date, director and addedby.
    Commits changes to the database. 
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        update movie set tt = %s, title = %s, `release` = %s, director = %s, addedby = %s
        where tt = %s''', (newtt, title, release, director, addedby, tt))
    conn.commit()
    return

def delete_movie(conn, tt):
    '''Deletes a movie from the movie table 
    with the specified values of tt. 
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        delete from movie where tt = %s''', (tt))
    conn.commit()
    return

def select_movie(conn):
    '''Returns the name of a movie in
    the movie table, as a list of dictionaries.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select tt, title
        from movie
        where director is null or `release` is null''')
    return curs.fetchall()

# ==========================================================
# This starts the ball rolling, *if* the file is run as a
# script, rather than just being imported.    

if __name__ == '__main__':
    dbi.cache_cnf()   # defaults to ~/.my.cnf
    dbi.use('zy1_db')
    conn = dbi.connect()