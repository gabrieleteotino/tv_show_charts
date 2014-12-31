'''
Created on 29/dic/2014

@author: gabriele
'''
import itertools
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots_adjust
import numpy

class PlotShow(object):
    '''
    classdocs
    '''
    def plot_show_multi(self, show, save_file):
        """
        Each season color-coded 
        best-fit linear regression line to show the season's trend
        """

        plt.style.use("ggplot")

        print "plot_show_multi - " + str(show)
        
        title = "IMDb ratings for " + show.name + " (" + str(show.year) + ")"
        seasons = show.get_seasons()
        
        # Create the chart
        # squeeze=False enforce the returning of an array even if only one season is present
        fig, axes = plt.subplots(1, len(seasons), sharex=True, squeeze=False)
        # We use only one row of axes, so we only the first dimension
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
            votes_trend = calculate_trend_line_poly(x, votes)
            
            # Plot ratings
            axis = axes[i]
            axis.plot(x, ratings, "-8")
            # Plot the trend line
            axis.plot(x, ratings_trend(x), "-")
            axis.set_title("Season {}".format(season.number), fontsize=12)
            # Configure the axis
            axis.set_ylim(5, 10)
            axis.yaxis.grid(True)

            # Clone axis
            axis_twin = axis.twinx()
            axes_twin.append(axis_twin)
            
            # Plot votes
            axis_twin.plot(x, votes, "--")
            axis_twin.set_ylim(0, max_votes)
            # Plot the trend line
            axis_twin.plot(x, votes_trend(x), ":")

        for axis in axes:
            axis.get_xaxis().set_visible(False)

        # Clear the "Ratings" axis for all except the first one
        for axis in axes[1:]:
            axis.set_yticklabels([])
            # remove vertical axis line
            #axis.spines['right'].set_visible(False)
            #axis.spines['left'].set_visible(False)

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
        