"""
Created on 23/dic/2014

@author: Gabriele Teotino
"""

import os.path
import codecs
import argparse
import sys
import ftplib
import gzip

from tv_show_charts.orm import Manager
from tv_show_charts.models import Show
from tv_show_charts.models import Episode
from tv_show_charts.ratings_parser import RatingsParser
from tv_show_charts.plot_show import PlotShow
from tv_show_charts.scatter import Scatter


RESOURCE_FILES_PATH = os.path.join(os.path.expanduser('~'), "tv_shows_chart")
DB_FILE_NAME = os.path.join(RESOURCE_FILES_PATH, "imdb_shows.sqlite")
RATINGS_FILE_NAME = os.path.join(RESOURCE_FILES_PATH, "ratings.list")
RATINGS_FILE_NAME_GZ = os.path.join(RESOURCE_FILES_PATH, "ratings.list.gz")


def populate_db():
    if not os.path.isfile(RATINGS_FILE_NAME):
        print("Ratings file not found, aborting")
        return False
    
    if os.path.isfile(DB_FILE_NAME):
        os.remove(DB_FILE_NAME)
        print("Previous database deleted")
    
    with Manager(DB_FILE_NAME) as db_manager:
        with codecs.open(RATINGS_FILE_NAME, encoding="latin-1") as ratings_file:
            parser = RatingsParser() 
            print("Populating data")
            inserted_shows = 0
            show = None
            shows = []
            for line in ratings_file:
                parsed = parser.parse_line(line)
                if 'type' in parsed:
                    if parsed['type'] == "Show":
                        # Check if we have too many show in the array
                        if len(shows) >= 10000:
                            db_manager.insert_show_and_episodes(shows)
                            inserted_shows += len(shows)
                            print ("{} lines loaded...".format(inserted_shows))
                            shows = []
                        show = Show(0,
                                    parsed['show_title'],
                                    parsed['year'],
                                    parsed['ratings'],
                                    parsed['votes'],
                                    parsed['distribution'])
                        shows.append(show)
                    if parsed['type'] == "Episode":
                        #Check if the Episode is part of the show
                        if parsed['show_title'] == show.name and parsed['year'] == show.year:
                            episode = Episode(0, 0,
                                              parsed['episode_title'],
                                              parsed['season'],
                                              parsed['number'],
                                              parsed['ratings'],
                                              parsed['votes'],
                                              parsed['distribution'])
                            show.episodes.append(episode)
                        else:
                            print("Detected orphan episode: " + line + "\n" + str(parsed))
        # After reaching the EOF we save the remaining shows
        db_manager.insert_show_and_episodes(shows)
        print("Insert complete, indexing data")
        db_manager.reindex_full_text_search()
        print("Populate complete")
        db_manager.print_table_stats()


def search_shows(text_to_search):
    print("Searching " + text_to_search)
    with Manager(DB_FILE_NAME) as db_manager:
        show_search_results = db_manager.search_shows(text_to_search)
        for show_search in show_search_results:
            print(show_search)


def print_tv_show_stats(show_id, save_file=False):
    print(show_id)
    with Manager(DB_FILE_NAME) as db_manager:
        show = db_manager.load_show_by_id(show_id)
        if show:
            PlotShow().plot_show_all_season(show, save_file)
        else:
            print("TV Show not found. ID:{}".format(show_id))


def download_ratings():
    print("Connecting to ftp server")
    ftp = ftplib.FTP("ftp.fu-berlin.de")
    ftp.login()
    print("Connected")
    ftp.cwd("/pub/misc/movies/database/")
    print("Downloading file...")
    ratings_file_gz = open(RATINGS_FILE_NAME_GZ, "wb")
    ftp.retrbinary("RETR ratings.list.gz", ratings_file_gz.write)
    ratings_file_gz.close()
    ftp.close()
    print("Download complete")
    print("Extracting file...")
    
    ratings_file_gz = gzip.open(RATINGS_FILE_NAME_GZ, 'rb')
    ratings_file = open(RATINGS_FILE_NAME, 'wb')
    ratings_file.write( ratings_file_gz.read() )
    ratings_file_gz.close()
    ratings_file.close()
    print("Extraction complete, have fun!")


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="tv_show_charts",
        description="TV Show Charts does some fantastic stuff."
    )
    
    # Store_true sets the argument to true only if the value is specified, this way the parameter is a flag
    parser.add_argument("--populate", action="store_true", help="Clean and reload the database from the ratings.list")
    parser.add_argument("--search_shows", help="Search for a TV show in the database")
    parser.add_argument("--download", action="store_true", help="Download the ratings file from IMDb servers")
    parser.add_argument("--db_stats", action="store_true", help="Show some statistic from the db")
    parser.add_argument("--view", help="Show some statistic for the show. Use the id obtained with --search_shows")
    parser.add_argument("--save", help="Save a png file with the chart for the selected show. Use the id obtained with --search_shows")
    parser.add_argument("--scatter", action="store_true", help="Create various scatter plots")
    return parser.parse_args(args)


def print_scatter():
    with Scatter(DB_FILE_NAME) as scatter:
        scatter.show_episode_ratings_per_year()


def main():
    if not os.path.exists(RESOURCE_FILES_PATH):
        os.makedirs(RESOURCE_FILES_PATH)
        
    args = parse_args(sys.argv[1:])

    if args.populate:
        populate_db()
    elif args.download:
        download_ratings()
    elif args.search_shows:
        search_shows(args.search_shows)
    elif args.db_stats:
        with Manager(DB_FILE_NAME) as db_manager:
            db_manager.print_table_stats()
    elif args.view:
        print_tv_show_stats(args.view)
    elif args.save:
        print_tv_show_stats(args.save, True)
    elif args.scatter:
        print_scatter()
    else:
        print("Use -h to get help")
        
if __name__ == '__main__':
    main()