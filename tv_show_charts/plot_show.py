'''
Created on 29/dic/2014

@author: gabriele
'''
import itertools
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots_adjust
import matplotlib as mpl
import numpy

class PlotShow(object):
    '''
    classdocs
    '''
    def plot_show_multi(self, show, save_file):
        """
        A chart with each season color-coded
        Plot "Ratings", "Number of votes" and a best-fit linear regression line to show the season's trend
        """

        print "plot_show_multi - " + str(show)

        plt.style.use("ggplot")
        # Set the plot background a bit lighter
        mpl.rcParams['axes.facecolor'] = 'F0F0F0'

        # These are the "Tableau 20" colors as RGB
        tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts
        for i in range(len(tableau20)):
            r, g, b = tableau20[i]
            tableau20[i] = (r / 255., g / 255., b / 255.)

        title = "IMDb ratings for " + show.name + " (" + str(show.year) + ")"
        seasons = show.get_seasons()
        
        # Create the chart
        # squeeze=False enforce the returning of an array even if only one season is present
        fig, axes = plt.subplots(1, len(seasons), sharex=True, squeeze=False)

        # We use only one row of axes, so we only need the first row
        axes = axes[0]
        axes_twin = []

        # Add a title
        fig.suptitle(title, fontsize=16)

        subplots_adjust(left=0.05, bottom=0.05, right=0.90, top=0.90, wspace=0.05, hspace=0)
        
        def calculate_trend_line_poly(x, y):
            z = numpy.polyfit(x, y, 1)
            p = numpy.poly1d(z)
            return p
        
        max_votes = max(ep.votes for ep in show.episodes)

        for i in range(len(seasons)):
            season = seasons[i]
            # Prepare data to plot
            x = range(len(season.episodes))
            ratings = [ep.rating for ep in season.episodes]
            ratings_trend = calculate_trend_line_poly(x, ratings)
            votes = [ep.votes for ep in season.episodes]
            #votes_trend = calculate_trend_line_poly(x, votes)

            label = "Season {}".format(season.number)

            # Plot ratings
            axis = axes[i]
            color = tableau20[i%20]
            axis.plot(x, ratings, "-8", color=color, linewidth=2.0)

            # Plot the trend line
            axis.plot(x, ratings_trend(x), "-", color=color)
            axis.set_title(label, fontsize=12, color=color)
            # Configure the axis
            axis.set_ylim(5, 10)
            axis.yaxis.grid(True)

            # Clone axis
            axis_twin = axis.twinx()
            axes_twin.append(axis_twin)
            
            # Plot votes
            axis_twin.plot(x, votes, "--", color=color)
            axis_twin.set_ylim(0, max_votes)
            # Plot the trend line
            #axis_twin.plot(x, votes_trend(x), ":")

            # Only after the last plot we can set the xbounds
            axis.set_xbound(-1)

        # Remove the Grid for the x axis
        for axis in axes:
            axis.get_xaxis().set_visible(False)

        # Clear the "Ratings" axis for all except the first one
        for axis in axes[1:]:
            axis.set_yticklabels([])

        # Clear the "Votes" axis for all except the last one
        for axis in axes_twin[:-1]:
            axis.get_yaxis().set_visible(False)
        axes_twin[-1].get_yaxis().grid(False)

        axes[0].set_ylabel('Ratings')
        axes_twin[-1].set_ylabel('Number of votes')

        if save_file:
            filename = "{}_{}({}).png".format(show.show_id, show.name, show.year)
            fig.set_size_inches(15, 10)
            fig.savefig(filename)
            print "Saved to " + filename
        else:
            plt.show()
        