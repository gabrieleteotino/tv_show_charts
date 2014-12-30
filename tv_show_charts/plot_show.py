'''
Created on 29/dic/2014

@author: gabriele
'''
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots_adjust
import numpy

class PlotShow(object):
    '''
    classdocs
    '''
    def plot_show_multi(self, show):
        """
        Each season color-coded 
        best-fit linear regression line to show the season's trend
        """
        
        print "plot_show_multi - " + str(show)
        
        title = "IMDb ratings for " + show.name + " (" + str(show.year) + ")"
        seasons = show.get_seasons()
        
        # Create the chart
        fig, axes = plt.subplots(1, len(seasons), sharex=True)
        axes_twin = []
        
        # Add a title
        fig.suptitle(title, fontsize=16)

        subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.90, wspace=0, hspace=0)
        
        def clean_axis(axis):
            #remove labels
            axis.get_xaxis().set_visible(False)
            axis.set_yticklabels([])
            #axis.get_yaxis().set_visible(False)
            # remove vertical axis line
            axis.spines['right'].set_visible(False)
            axis.spines['left'].set_visible(False)
        
        def calculate_trend_line_poly(x, y):
            z = numpy.polyfit(x, y, 1)
            p = numpy.poly1d(z)
            return p
        
        max_votes = max(ep.votes for ep in show.episodes)
        #max_ratings = max(ep.rating for ep in show.episodes)
        
        for i in range(len(seasons)):
            season = seasons[i]
            # Prepare data to plot
            x = range(len(season.episodes))
            ratings = [ep.rating for ep in season.episodes]
            ratings_trend = calculate_trend_line_poly(x, ratings)
            votes = [ep.votes for ep in season.episodes]
            votes_trend = calculate_trend_line_poly(x, votes)
            
            # Plot ratings
            axes[i].plot(x, ratings, "-o")
            # Plot the trendline
            axes[i].plot(x, ratings_trend(x), "-")
            axes[i].set_title("Season {}".format(season.number), fontsize=12)
            # Configure the axis
            axes[i].set_ylim(5, 10)
            axes[i].set_xlim(0, len(season.episodes))
            axes[i].yaxis.grid(True)
            
            # Clone axis
            axis_twin = axes[i].twinx()
            axes_twin.append(axis_twin)
            
            # Plot votes
            axis_twin.plot(x, votes, ":")
            axis_twin.set_ylim(0, max_votes)
            
            # Plot the trendline
            axis_twin.plot(x, votes_trend(x), ":")
            
            axis_twin.get_yaxis().set_visible(False)
            
            clean_axis(axes[i])
            clean_axis(axis_twin)
        
        # Put back the labels and vertical line for the first and the last plot
        axes[0].get_yaxis().set_visible(True)
        axes[0].spines['left'].set_visible(True)
        axes[0].set_ylabel('Ratings')
        
        axes[-1].spines['right'].set_visible(True)
        axes_twin[-1].get_yaxis().set_visible(True)
        axes_twin[-1].set_ylabel('Number of votes')
        
        plt.show()
        