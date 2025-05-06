import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Clean data
df = df[df['value'] >= df['value'].quantile(0.025)]
df = df[df['value'] <= df['value'].quantile(0.975)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(24, 8))
    plt.plot(df.index, df['value'], linestyle='-', color='red')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Draw bar plot
    gb = df.groupby([(df.index.year), (df.index.month)]).sum().reset_index(names=['year','month'])
    gb['average'] = gb['value'] / pd.DatetimeIndex(pd.to_datetime(gb[['year', 'month']].assign(day=1))).days_in_month

    years = pd.Series(gb['year'].unique()).sort_values()
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    width = 0.8 / len(months) 
    x = np.arange(len(years))

    fig, ax = plt.subplots(figsize=(8, 6), layout='constrained')

    for m in range(12):
        avg_month_views = []
        for year in years:
            if not gb[(gb['year'] == year) & (gb['month'] == m + 1)].empty:
                avg_month_views.append(gb[(gb['year'] == year) & (gb['month'] == m + 1)]['average'].mean())
            else:
                avg_month_views.append(0)
        ax.bar(x + m * width, avg_month_views, width=width, label=months[m])
        
    plt.xticks(x + width * (x / 2), years)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
draw_bar_plot()


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
