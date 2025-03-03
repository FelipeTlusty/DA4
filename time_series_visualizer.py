import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('./fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (15, 5))
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    sns.lineplot(data = df, legend = False, palette = ['r']).set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019").figure

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(["Years", "Months"], sort=False)["value"].mean().round().astype(int)).reset_index()

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data = df_bar, x = 'Years', y = 'value', hue = 'Months', palette = 'tab10', width = 0.5, hue_order = month_order).figure
    ax.set_ylabel("Average Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Draw box plots (using Seaborn)
    # plot 1
    fig, (ax1, ax2) = plt.subplots(figsize=(20, 8), ncols= 2)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_ylim([0, 200000])
    ax1.set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])
    ax1 = sns.boxplot(data = df_box, x = 'year', hue = 'year', y = 'value', ax = ax1, legend = False, palette='bright', flierprops={"marker": "."}).figure

    # plot 2
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_ylim([0, 200000])
    ax2.set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])
    ax2 = sns.boxplot(data = df_box, x = 'month', y = 'value', hue = 'month', ax = ax2, legend = False, palette = 'muted', flierprops={"marker": "."}, order = month_order).figure

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

# draw_line_plot()
# draw_box_plot()
draw_bar_plot()