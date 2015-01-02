"""
Created on 27/dic/2014

@author: Gabriele Teotino
"""
import re
from models import Show
from models import Episode


class RatingsParser(object):
    """
    Parse a ratings.list obtained from IMDb
    Example of a valid line for a show
        0000011101    4204   6.3  "$#*! My Dad Says" (2010)
    Example of a valid line for an episode
        00.0112201      66   6.9  "$#*! My Dad Says" (2010) {Code Ed (#1.4)}
    Example of an episode without season nor number
        0000000123     295   8.4  "Doctor Who" (2005) {Last Christmas}
    Example of an episode without title
        ..00.02301      31   7.4  "Doctor Who: Dreamland" (2009) {(#1.1)}
    """
    _re_valid_show = re.compile(r'\s*((\d|\.){10})\s*(\d*)\s*(\d*\.\d*)\s*"(.*)"\s\((\d\d\d\d)\)')
    _re_valid_episode = re.compile(r'\s*((\d|\.){10})\s*(\d*)\s*(\d*\.\d*)\s*"(.*)"\s\((\d\d\d\d)\)\s\{(.*)\}')
    _re_episode_season_and_number = re.compile(r'\(#(\d+.*\d*)\)')

    def parse_episode(self, text):
        """
        return a dictionary with title, season and number
        
        Episode text can be:
        - title season and number 
            re.split('\(#(\d+.*\d*)\)', "episode_title(#2.3)")
            ['episode_title', '2.3', '']
        
        - title and number, without season
            re.split('\(#(\d+.*\d*)\)', "episode_title(#3)")
            ['episode_title', '3', '']

        - title only
            re.split('\(#(\d+.*\d*)\)', "episode_title")
            ['episode_title']
            
        - no title, only season and number
            re.split('\(#(\d+.*\d*)\)', "(#2.3)")
            ['', '2.3', '']

        - no title, no season, only number
            re.split('\(#(\d+.*\d*)\)', "(#3)")
            ['', '3', '']

        """
        results = {}
        split_results = self._re_episode_season_and_number.split(text)
        if len(split_results) == 1:
            # We have only the title
            results['title'] = split_results[0]
            results['season'] = 0
            results['number'] = 0
        elif len(split_results) == 3:
            results["title"] = split_results[0]
            
            dot_split_result = split_results[1].split('.')
            if len(dot_split_result) == 2:
                results['season'] = dot_split_result[0]
                results['number'] = dot_split_result[1]
            else:
                results['season'] = 1
                results['number'] = dot_split_result[0]
        else:
            print "parse_episode unexpected split results, original text is: " + text
        
        return results
    
    def parse_line(self, text):
        """
        Return None if the line is not a valid match, Show or Episode (without id) if the match is valid
        """
        result = None
        
        show_matches = self._re_valid_show.match(text)
        episode_matches = self._re_valid_episode.match(text)
        
        if not episode_matches is None:
            distribution = episode_matches.group(1)
            votes = int(episode_matches.group(3))
            ratings = float(episode_matches.group(4))
            
            episode_details = self.parse_episode(episode_matches.group(7))
            
            # The id  will be created by the db
            result = Episode(0, 0,
                            episode_details['title'], episode_details['season'], episode_details['number'],
                            ratings, votes, distribution)
        
        elif not show_matches is None:
            distribution = show_matches.group(1)
            votes = int(show_matches.group(3))
            ratings = float(show_matches.group(4))
            
            show_name = show_matches.group(5)
            show_year = show_matches.group(6)
            
            # The id  will be created by the db
            result = Show(0, show_name, show_year, ratings, votes, distribution)
        
        return result