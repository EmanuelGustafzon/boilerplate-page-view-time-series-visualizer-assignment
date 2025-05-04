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
    # Copy and modify data for monthly bar plot
    df_bar = None

    # Draw bar plot
    gb = df.groupby([(df.index.year), (df.index.month)]).sum().reset_index(names=['year','month'])
    gb['average'] = round(gb['value'] / pd.DatetimeIndex(pd.to_datetime(gb[['year', 'month']].assign(day=1))).days_in_month)

    fig, ax = plt.subplots(layout='constrained')

    years = np.sort(gb['year'].unique())
    full_year_range = np.arange(gb['year'].min(), gb['year'].max() + 1)
    months = np.sort(gb['month'].unique())

    x = np.arange(len(gb['month'].unique()))
    width = 0.8 / len(months) 

    for i, month in enumerate(months):
        data = gb.loc[(gb['month'] == month)].sort_values(by='year')
        plt.bar(x + i * width, data['average'], width, label=month)

    plt.xticks(np.arange(len(gb['year'].unique())), years)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(x, title='Months')
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
