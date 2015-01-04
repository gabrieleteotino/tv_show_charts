import re

__author__ = "Gabriele Teotino"
__license__ = "MIT"

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
    _re_valid_episode = re.compile(r'.*?\{(.*)\}')
    _re_episode_season_and_number = re.compile(r'\(#(\d+.*\d*)\)')

    def parse_line(self, text):
        """
        Returns a dictionary containing the parsing results
        if text is not valid
            return {}
        if text is a show
            return {'type': "Show", ...}
        if text is an Episode
            return {'type': "Episode", ...}
        """
        result = {}

        # Using _re_valid_show we will match both the Show and Episode
        show_matches = self._re_valid_show.match(text)
        if show_matches:
            distribution = show_matches.group(1)
            votes = int(show_matches.group(3))
            ratings = float(show_matches.group(4))

            show_title = show_matches.group(5)
            show_year = show_matches.group(6)

            result = {
                'type': "Show",
                'show_title': show_title,
                'year': int(show_year),
                'ratings': float(ratings),
                'votes': int(votes),
                'distribution': distribution
            }
        else:
            # Nothing more to do here
            return {}

        # If _re_valid_episode is a match we will add episode information
        episode_matches = self._re_valid_episode.match(text)
        if episode_matches:
            # Change the type from Show to Episode
            result['type'] = "Episode"

            #episode_details = self.parse_episode(episode_matches.group(1))
            """
            The string containing episode details is not nicely formatted by IMDb
            It can be:
            "episode_title"
            "episode_title(#2.3)"
            "episode_title(#3)"
            "(#2.3)"
            "(#3)"
            """

            split_results = self._re_episode_season_and_number.split(episode_matches.group(1))
            if len(split_results) == 1:
                # We have only the title
                result['episode_title'] = split_results[0]
                result['season'] = 0
                result['number'] = 0
            elif len(split_results) == 3:
                result["episode_title"] = split_results[0]

                dot_split_result = split_results[1].split('.')
                if len(dot_split_result) == 2:
                    result['season'] = int(dot_split_result[0])
                    result['number'] = int(dot_split_result[1])
                else:
                    result['season'] = 1
                    result['number'] = int(dot_split_result[0])
            else:
                print("parse_episode unexpected split results, original text is: " + text)

        return result