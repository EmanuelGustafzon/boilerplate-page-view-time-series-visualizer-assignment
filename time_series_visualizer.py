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
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    df_line = df.copy()
    fig, ax = plt.subplots(figsize=(24, 8))
    plt.plot(df_line.index, df_line['value'], linestyle='-', color='red')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Draw bar plot
    df_bar = df.copy()
    gb = df_bar.groupby([(df_bar.index.year), (df_bar.index.month)]).sum().reset_index(names=['year','month'])
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

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    if df_box.index.name == 'date':
        df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box.sort_values(by='date',inplace=True)
    
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box.rename(columns={'value': 'Page Views'}, inplace=True)
    df_box['Page Views'] = df_box['Page Views'].apply(lambda x: np.float64(x))
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(16, 6), layout='constrained')

    palette = sns.color_palette("pastel")
    sns.boxplot(x='year', y='Page Views', ax=ax[0], data=df_box, hue='year', legend=False).set(title='Year-wise Box Plot (Trend)', xlabel = 'Year')

    sns.boxplot(x='month', y='Page Views', 
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  
        ax= ax[1], 
        data=df_box,
        hue='month',
        legend=False).set(title='Month-wise Box Plot (Seasonality)', xlabel = 'Month')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
