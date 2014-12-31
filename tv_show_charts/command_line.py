'''
Created on 23/dic/2014

@author: Gabriele Teotino
'''

import os.path
import codecs
import argparse
import sys
import ftplib
import gzip
from orm import Manager
from models import Show
from models import Episode
from ratings_parser import RatingsParser
from tv_show_charts.plot_show import PlotShow

RESOURCE_FILES_PATH = os.path.join(os.path.expanduser('~'), "tv_shows_chart")
DB_FILE_NAME = os.path.join(RESOURCE_FILES_PATH, "imdb_shows.sqlite")
RATINGS_FILE_NAME = os.path.join(RESOURCE_FILES_PATH, "ratings.list")
RATINGS_FILE_NAME_GZ = os.path.join(RESOURCE_FILES_PATH, "ratings.list.gz")

def populate_db():
    if not os.path.isfile(RATINGS_FILE_NAME):
        print "Ratings file not found, aborting"
        return False
    
    if os.path.isfile(DB_FILE_NAME):
        os.remove(DB_FILE_NAME)
        print "Previous database deleted"
    
    with Manager(DB_FILE_NAME) as db_manager:
        with codecs.open(RATINGS_FILE_NAME, encoding="latin-1") as ratings_file:
            parser = RatingsParser() 
            print "Populating data"
            inserted_shows = 0
            show = None
            shows = []
            for line in ratings_file:
                parsed = parser.parse_line(line)
                if type(parsed) is Show:
                    # Check if we have too many show in the array
                    if len(shows) >= 10000:
                        db_manager.insert_show_and_episodes(shows)
                        inserted_shows += len(shows)
                        print "%s shows analized ..." % inserted_shows
                        shows = []
                    show = parsed
                    shows.append(show)
                if type(parsed) is Episode:
                    show.episodes.append(parsed)
        # After reaching the EOF we save the remaining shows
        db_manager.insert_show_and_episodes(shows)
        print "Insert complete, indexing data"
        db_manager.reindex_full_text_search()
        print "Populate complete"
        db_manager.print_table_stats()
        
def search_shows(text_to_search):
    print "Searching " + text_to_search
    with Manager(DB_FILE_NAME) as db_manager:
        show_search_results = db_manager.search_shows(text_to_search)
        for show_search in show_search_results:
            print "ID:{} - Title: {}  Year:{}".format(show_search.show_id, show_search.name, show_search.year)
        
def print_tv_show_stats(show_id, save_file=False):
    print show_id
    with Manager(DB_FILE_NAME) as db_manager:
        show = db_manager.load_show_by_id(show_id)
        if show:
            plotter = PlotShow()
            plotter.plot_show_multi(show, save_file)
        else:
            print "TV Show not found. ID:{}".format(show_id)
            
def download_ratings():
    print "Connecting to ftp server"
    ftp = ftplib.FTP("ftp.fu-berlin.de")
    ftp.login()
    print "Connected"
    ftp.cwd("/pub/misc/movies/database/")
    print "Downloading file..."
    ratings_file_gz = open(RATINGS_FILE_NAME_GZ, "wb")
    ftp.retrbinary("RETR ratings.list.gz", ratings_file_gz.write)
    ratings_file_gz.close()
    ftp.close()
    print "Download complete"
    print "Extracting file..."
    
    ratings_file_gz = gzip.open(RATINGS_FILE_NAME_GZ, 'rb')
    ratings_file = open(RATINGS_FILE_NAME, 'wb')
    ratings_file.write( ratings_file_gz.read() )
    ratings_file_gz.close()
    ratings_file.close()
    print "Extraction complete, have fun!"
    
def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='tv_show_charts',
        description='TV Show Charts does some fantastic stuff.'
    )
    
    #store_true sets the argument to true only if the value is specified, this way the parameter is a flag
    parser.add_argument("--populate", action="store_true", help="Clean and reload the database from the ratings.list")
    parser.add_argument("--search_shows", help="Search for a TV show in the database")
    parser.add_argument("--download", action="store_true", help="Download the ratings file from IMDB servers")
    parser.add_argument("--db_stats", action="store_true", help="Show some statistic from the db")
    parser.add_argument("--view", help="Show some statistic for the show. Use the id obtained with --search_shows")
    parser.add_argument("--save", help="Save a png file with the chart for the selected show. Use the id obtained with --search_shows")
    return parser.parse_args(args)
    
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
    else:
        print "Use -h to get help"
        
if __name__ == "__main__":
    main()