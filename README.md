tv_show_charts
==============

TV Shows Charting imports all the TV series from IMDb and create charts


Installation
------------
    python setup.py install

Database configuration
----------------------
On the first run launch the program with the download option

    tv_show_charts --download

This will download an updated version of the file ratings.list from IMDb. Please be patient, the file is about 10MB.

Then create the database

    tv_show_charts --populate

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