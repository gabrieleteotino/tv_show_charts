import sqlite3
import matplotlib.pyplot as plt

__author__ = "Gabriele Teotino"
__license__ = "MIT"

class Scatter(object):
    _select_show_vs_episode_votes = """
        SELECT
            S.show_votes,
            E.episode_votes
        FROM
            (SELECT show_id, votes AS show_votes
            FROM Shows) AS S
        JOIN
            (SELECT show_id, SUM(votes) AS episode_votes
            FROM Episodes
            GROUP BY show_id) AS E
        ON S.show_id = E.show_id
        """
    _select_show_vs_episode_ratings = """
        SELECT
            S.show_rating,
            E.episode_rating
        FROM
            (SELECT show_id, rating AS show_rating
            FROM Shows) AS S
        JOIN
            (SELECT show_id, AVG(rating) AS episode_rating
            FROM Episodes
            GROUP BY show_id) AS E
        ON S.show_id = E.show_id
        """

    _select_show_ratings_per_year = """
        SELECT
            rating,
            year
        FROM Shows
        """

    _select_show_episode_ratings_per_year = """
        SELECT
            E.episode_rating,
            S.year
        FROM
            (SELECT show_id, year
            FROM Shows) AS S
        JOIN
            (SELECT show_id, AVG(rating) AS episode_rating
            FROM Episodes
            GROUP BY show_id) AS E
        ON S.show_id = E.show_id
        """

    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        self._connection = sqlite3.connect(db_file_name)
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        if not self._connection is None:
            self._connection.close()

    def votes(self):
        self._cursor.execute(self._select_show_vs_episode_votes)
        rows = self._cursor.fetchall()

        sv, ev = zip(*rows)

        ax = plt.figure().add_subplot(111)
        ax.scatter(sv, ev, 1)
        ax.set_xlim(0, 2000)
        ax.set_ylim(0, 2000)

        plt.show()

    def ratings(self):
        self._cursor.execute(self._select_show_vs_episode_ratings)
        rows = self._cursor.fetchall()

        sr, er = zip(*rows)
        # Round the episodes rating to 1 decimal so it's similar to the season rating
        er = [round(r, 1) for r in er]

        ax = plt.figure().add_subplot(111)
        ax.scatter(sr, er, alpha=0.05)
        ax.set_xlim(6, 10)
        ax.set_ylim(6, 10)

        plt.show()

    def show_ratings_per_year(self):
        self._cursor.execute(self._select_show_ratings_per_year)
        rows = self._cursor.fetchall()

        sr, sy = zip(*rows)
        ax = plt.figure().add_subplot(111)
        ax.scatter(sy, sr, alpha=0.05)
        ax.set_ylim(1, 10)

        plt.show()

    def show_episode_ratings_per_year(self):
        self._cursor.execute(self._select_show_episode_ratings_per_year)
        rows = self._cursor.fetchall()

        sr, sy = zip(*rows)
        ax = plt.figure().add_subplot(111)
        ax.scatter(sy, sr, alpha=0.05)
        ax.set_ylim(1, 10)

        plt.show()