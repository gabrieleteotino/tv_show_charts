'''
Created on 24/dic/2014

@author: Gabriele Teotino
'''
from itertools import groupby

class Show(object):
    def __init__(self, show_id, name, year, rating, votes, distribution):
        self._seasons = None

        self.show_id = show_id
        self.name = name
        self.year = int(year)
        
        self.rating = float(rating)
        self.votes = int(votes)
        self.distribution = distribution
        self.episodes = []

    def __str__(self):
        return self.name.encode("utf-8") + " (" + str(self.year) + ")"

    def __eq__(self, other):
        if other is None: return False
        return self.name == other.name and self.year == other.year

    @property
    def seasons(self):
        if self._seasons is None:
            self._seasons = []
            # Sort the episodes (they should already be sorted, but better safe than sorry)
            self.episodes.sort(key = lambda x: (x.season, x.number))
            for key, group in groupby(self.episodes, lambda ep: ep.season):
                if key != 0:#ignore season zero episodes
                    season = Season(key, list(group))
                    self._seasons.append(season)
        return self._seasons

class ShowSearch(object):
    def __init__(self, show_id, name, year):
        self.show_id = show_id
        self.name = name
        self.year = year
        
class Episode(object):
    def __init__(self, episode_id, show_id, title, season, number, rating, votes, distribution):
        try:
            self.episode_id = int(episode_id)
            self.show_id = int(show_id)
            self.title = title
            self.season = int(season)
            self.number = int(number)
            
            self.rating = float(rating)
            self.votes = int(votes)
            self.distribution = distribution
        except :
            print "Unexpected error"
            print (title, season, number, rating, votes, distribution)
            raise
    def __str__(self):
        return self.title.encode("utf-8") + " #" + str(self.season) + "." + str(self.number) + " " + \
            str(self.rating) + " " + str(self.votes) + " " + self.distribution.encode("utf-8")

class Season(object):
    def __init__(self, number, episodes):
        self.number = number
        self.episodes = episodes
        