"""
Created on 24/dic/2014

@author: Gabriele Teotino
"""
import sqlite3
from tv_show_charts.models import *


class Manager():
    _shows_create = '''
        CREATE TABLE if not exists Shows (
            show_id INTEGER PRIMARY KEY,
            name NOT NULL, 
            year NOT NULL,
            rating NOT NULL,
            votes NOT NULL,
            distribution NOT NULL
        )
    '''
    _show_insert = 'INSERT INTO Shows (name, year, rating, votes, distribution) VALUES (?, ?, ?, ?, ?)'
    _show_by_id_select = 'SELECT show_id, name, year, rating, votes, distribution FROM Shows WHERE show_id = ?'
    
    _episodes_create = '''
        CREATE TABLE if not exists Episodes (
            episode_id INTEGER PRIMARY KEY,
            show_id INTEGER NOT NULL,
            title NOT NULL,
            season NOT NULL,
            number NOT NULL,
            rating NOT NULL,
            votes NOT NULL,
            distribution NOT NULL, 
            FOREIGN KEY(show_id) REFERENCES Shows(id)
        )
    '''
    _episode_insert = '''
        INSERT INTO Episodes (show_id, title, season, number, rating, votes, distribution) VALUES (?,?,?,?,?,?,?)
    '''
    _episodes_for_show_select = '''
        SELECT episode_id, show_id, title, season, number, rating, votes, distribution
        FROM Episodes WHERE show_id = ? ORDER BY season, number
    '''
    
    _shows_search_drop = 'DROP TABLE IF EXISTS ShowsSearch'
    _shows_search_create = 'CREATE VIRTUAL TABLE ShowsSearch USING fts4(show_id, name, year);'
    _shows_search_populate = 'INSERT INTO ShowsSearch SELECT show_id, name, year FROM Shows;'
    _shows_search_select = 'SELECT show_id, name, year FROM ShowsSearch WHERE name MATCH ?;'
    
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name        
        self._connection = sqlite3.connect(db_file_name)
        self._cursor = self._connection.cursor()
        self.create_tables()
        
    def __enter__(self):
        return self
    
    def __exit__(self, type_, value, traceback):
        if not self._connection is None:
            self._connection.close()
        
    def create_tables(self):
        self._cursor.execute(self._shows_create)
        self._cursor.execute(self._episodes_create)
        return True
    
    def reindex_full_text_search(self):
        self._cursor.execute(self._shows_search_drop)
        self._cursor.execute(self._shows_search_create)
        self._cursor.execute(self._shows_search_populate)
        self._connection.commit()
            
    def insert_show_and_episodes(self, shows):
        for show in shows:
            # if no episode the it is a move and we don't want them
            if len(show.episodes) > 0:
                self._cursor.execute(self._show_insert,
                                     [show.name, show.year, show.rating, show.votes, show.distribution])
                show_id = self._cursor.lastrowid
                for episode in show.episodes:
                    self._cursor.execute(
                        self._episode_insert,
                        [show_id, episode.title, episode.season, episode.number,
                         episode.rating, episode.votes, episode.distribution]
                    )
        self._connection.commit()
        
    def search_shows(self, text_to_search):
        """ Returns a ShowSearch object not a Show """
        show_search_results = []
        for row in self._cursor.execute(self._shows_search_select, (text_to_search,)):
            show_search = ShowSearch(row[0], row[1], row[2])
            show_search_results.append(show_search)
        return show_search_results
    
    def load_show_by_id(self, show_id):
        self._cursor.execute(self._show_by_id_select, (show_id, ))
        row = self._cursor.fetchone()
        show = Show(row[0], row[1], row[2], row[3], row[4], row[5])
        self.load_episodes_for_show(show)
        return show
    
    def load_episodes_for_show(self, show):
        for row in self._cursor.execute(self._episodes_for_show_select, (show.show_id, )):
            episode = Episode(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            show.episodes.append(episode)
        return show
    
    def print_table_stats(self):
        """ Print some count statistic from the shows and the episodes table """
        self._cursor.execute('SELECT count(*) FROM Shows')
        (number_of_shows,) = self._cursor.fetchone()
        
        self._cursor.execute('SELECT count(*) FROM Episodes')
        (number_of_episodes,) = self._cursor.fetchone()
        
        self._cursor.execute('''
            SELECT AVG(episode_count) FROM (SELECT count(show_id) AS episode_count FROM Episodes AS e GROUP BY show_id)
        ''')
        (avg_number_of_episodes,) = self._cursor.fetchone()
        
        print("The database contains {} tv shows, {} episodes with an average of {} episodes for show".format(
            number_of_shows, number_of_episodes, avg_number_of_episodes))