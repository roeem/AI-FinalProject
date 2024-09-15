import matplotlib.pyplot as plt
import pandas as pd

# Assuming 'df' is your dataframe already loaded from the file
# List of unique data sets
data_sets = df['Data set'].unique()


# Function to add labels on bars
def add_value_labels(ax):
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')


# Get the upper bound for the Avg across all data sets and loads for consistent y-axis scaling
upper_bound = df['Avg'].max() + 5  # Adding a little padding to the max value

# Code to create the required plots
for data_set in data_sets:
    plt.figure(figsize=(10, 6))
    subset = df[df['Data set'] == data_set]
    subset_grouped = subset.groupby(['Load', 'Algorithm'])['Avg'].mean().unstack()
    ax = subset_grouped.plot(kind='bar', ax=plt.gca())

    plt.title(f'Bar Plot of Avg for {data_set} by Load and Algorithm')
    plt.ylabel('Average (Avg)')
    plt.ylim(0, upper_bound)  # Set the upper bound for y-axis to be consistent across all plots
    plt.grid(True)
    plt.legend(title='Algorithm')

    # Adding value labels on each bar
    add_value_labels(ax)

    plt.show()
