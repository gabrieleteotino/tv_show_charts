tv_show_charts
==============

TV Shows Charting imports all the TV series from IMDb and create charts


Installation
------------
    python setup.py install

If you have problems with the installer on Windows try to download the required packages manually from

[http://matplotlib.org/downloads.html](http://matplotlib.org/downloads.html)

[http://sourceforge.net/projects/numpy/files/NumPy/1.9.1/](http://sourceforge.net/projects/numpy/files/NumPy/1.9.1/)

Just find the correct exe for your system and install them.
After the requirements are met launch the install

    python setup.py install
    
Database configuration
----------------------
On the first run launch the program with the download option

    tv_show_charts --download

This will download an updated version of the file ratings.list from IMDb. Please be patient, the file is about 10MB.

Then create the database

    tv_show_charts --populate

If you receive this message on Windows:

    Insert complete, indexing data
    Traceback (most recent call last):
      File "C:\Python34\Scripts\tv_show_charts-script.py", line 9, in <module>
        load_entry_point('tv-show-charts==0.1', 'console_scripts', 'tv_show_charts')()
      File "c:\users\gabriele\pycharmprojects\tv_show_charts\tv_show_charts\command_line.py", line 134, in main
        populate_db()
      File "c:\users\gabriele\pycharmprojects\tv_show_charts\tv_show_charts\command_line.py", line 60, in populate_db
        db_manager.reindex_full_text_search()
      File "c:\users\gabriele\pycharmprojects\tv_show_charts\tv_show_charts\orm.py", line 70, in reindex_full_text_search
        self._cursor.execute(self._shows_search_create)
    sqlite3.OperationalError: no such module: fts4
    
1. Download the latest [sql dll](http://www.sqlite.org/download.html).
2. Replace sqlite.dll in your python/dll folder.    

Usage
-----

Search the ID of the show you want to plot

    tv_show_charts --search="Star Trek"

The output will be

    Searching Star Trek  
    ID:6940 - Title: Star Trek Continues  Year:2013  
    ID:6941 - Title: Star Trek  Year:1966  
    ID:6942 - Title: Star Trek: Deep Space Nine  Year:1993  
    ID:6943 - Title: Star Trek: Intrepid  Year:2009  
    ID:6944 - Title: Star Trek: New Voyages  Year:2004  
    ID:6945 - Title: Star Trek: The Animated Series  Year:1973  
    ID:6946 - Title: Star Trek: The Next Generation  Year:1987  
    ID:6947 - Title: Star Trek: Voyager  Year:1995  

Now you can plot the chart in the interactive window using the id 6947 (Voyager)

    tv_show_charts --view 6947

Or you can save a png file in the local folder

    tv_show_charts --save 6947