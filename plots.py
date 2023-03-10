import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time

class Plots:

    def __init__(self, data, save="no", print_="yes"):
        self.data = data
        self.save = save
        self.print_ = print_

    def show_save(self, name):
        if self.save == "yes":
            plt.savefig(name)
        if self.print_ == 'yes':
            plt.show()
        else:
            plt.close()


class ElbowPlot(Plots):

    def elbow_plot(self, k_range, inertia):
        '''Use an elbow graph to find the optimal amount of clusters'''
        # Plot the elbow curve to determine the optimal number of clusters
        sns.set(style='whitegrid')
        plt.plot(k_range, inertia)
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.title('Elbow Curve')
        # Show or save
        self.show_save("elbowplot")

class ClusterPlots(Plots):

    def standard_plot(self, x, y, zoom=None):
        sns.scatterplot(data=self.data, x=x, y=y, hue='cluster', palette='Set1')
        plt.title(f'Customer Segmentation: {x} vs. {y}')
        plt.xlabel(x)
        plt.ylabel(y)

        if zoom:
            plt.xlim(0, zoom[0])
            plt.ylim(0, zoom[1])
      

    def total_vs_countries(self, zoom=None):
        # Scatter plot of Total Amount vs. Num Countries with color-coded clusters
        if zoom == "yes":
            zoom = [200000, 15]
        self.standard_plot(x='Total Amount', y='Num Countries', zoom=zoom)
        # Show or save
        self.show_save(f"total_vs_countries_zoom={zoom}.png")

    def mean_vs_counttrans(self, zoom=None):
        # Scatter plot of Mean Amount vs. Count Trans with color-coded clusters
        if zoom == "yes":
            zoom = [9000, 35]
        self.standard_plot(x='Mean Amount', y='Count Trans', zoom=zoom)
        # Show or save
        self.show_save(f"mean_vs_counttrans_zoom={zoom}.png")

    def max_vs_numcountries(self):
        # Scatter plot of Max Amount vs. Num Countries with color-coded clusters
        self.standard_plot(x='Max Amount', y='Num Countries')
        plt.title('Customer Segmentation: Max Amount vs. Num Countries')
        # Show or save
        self.show_save(f"max_vs_numcountries.png")

    def mean_vs_max(self, zoom=None):
        # Scatter plot of Mean Amount vs. Max Amount with color-coded clusters
        if zoom == "yes":
            zoom = [8500, 20000]
        self.standard_plot(x='Mean Amount', y='Max Amount', zoom=zoom)
        # Show or save
        self.show_save(f"mean_vs_max_zoom={zoom}.png")

    def show_all_plots(self):
        self.total_vs_countries()
        self.total_vs_countries(zoom="yes")
        self.mean_vs_counttrans()
        self.mean_vs_counttrans(zoom="yes")
        self.max_vs_numcountries()
        self.mean_vs_max()
        self.mean_vs_max(zoom="yes")



class CountryPlots(Plots):

    def create_lables_bins(self):
    # Group the transactions by amount range
        n = 2000
        amount_bins = [0]
        amount_labels = []
        while n < 19000:
            label = f"{str(int((n/1000))-2)}k-{str(int(n/1000))}k"
            amount_labels.append(label)
            amount_bins.append(n)
            n += 2000
        return amount_bins, amount_labels

    def split_data(self):
        amount_bins, amount_labels = self.create_lables_bins()
        self.data['Amount Range'] = pd.cut(self.data['amount'], bins=amount_bins, labels=amount_labels)
        # Create a bar chart of the transaction amounts by amount range
        amount_counts = self.data['Amount Range'].value_counts().sort_index()
        amount_counts.plot(kind='bar')
        plt.title('Distribution of Monthly Incoming Transaction Amounts from High-Risk Countries')
        plt.xlabel('Amount Range')
        plt.ylabel('Number of Transactions')
        self.show_save('CountryPlots.png')