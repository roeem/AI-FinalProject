import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file into a DataFrame
file_path = 'results.xlsx'  # Replace with the actual file path of your Excel file
df = pd.read_excel(file_path, sheet_name='Astar')  # Assuming the sheet name is 'Astar'


# Function to add labels on bars
def add_value_labels(ax):
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')


# Get the upper bound for the Avg across all data sets and loads for consistent y-axis scaling
upper_bound = df['Avg'].max() + 5  # Adding a little padding to the max value

# List of unique data sets
data_sets = df['Data set'].unique()

# Code to create the required plots
# for data_set in data_sets:
#     plt.figure(figsize=(10, 6))
#     subset = df[df['Data set'] == data_set]
#     subset_grouped = subset.groupby(['Load', 'Algorithm'])['Avg'].mean().unstack()
#     ax = subset_grouped.plot(kind='bar', ax=plt.gca())
#
#     # Calculate dynamic upper and lower bounds based on the data
#     upper_bound = subset['Avg'].max()   # Add a buffer to the upper bound
#     lower_bound = subset['Avg'].min() - 5
#
#     if not (0 <= upper_bound <= 100):
#         lower_bound = 60  # Set the lower bound to 0 if it's less than 0
#     if not (0 <= lower_bound <= 100):
#         lower_bound = 60  # Set the lower bound to 0 if it's less than 0
#
#     plt.title(f'Bar Plot of Avg for {data_set} by Load and Algorithm')
#     plt.ylabel('Average (Avg)')
#     plt.ylim(lower_bound, upper_bound)
#     plt.grid(True)
#     plt.legend(title='Algorithm', bbox_to_anchor=(1.0, 1), loc='upper left', borderaxespad=1.5)
#
#     # Adding value labels on each bar
#     add_value_labels(ax)
#
#     plt.show()


for data_set in data_sets:
    plt.figure(figsize=(12, 6))  # Increase the figure size to allow more space for the legend

    # Filter the data for the current data set
    subset = df[df['Data set'] == data_set]

    # Ensure 'Avg' is numeric
    subset['Avg'] = pd.to_numeric(subset['Avg'], errors='coerce')

    # Calculate dynamic lower bound based on the data
    lower_bound = max(40, subset['Avg'].min() - 5)  # Set lower bound to the minimum value of Avg or 40

    # Get the "upper bound" from the data (assuming it's the maximum Avg in this case)
    upper_bound = subset['Avg'].max()  # Retrieve the upper bound value from the data set

    # Remove the row(s) that match the upper bound to avoid plotting them as bars
    subset_without_upper_bound = subset[subset['Avg'] < upper_bound]

    # Check if there's any data left after filtering
    if subset_without_upper_bound.empty:
        print(f"No data to plot for {data_set} after filtering out the upper bound.")
        continue  # Skip this plot if no data is left

    # Group the remaining data (without the upper bound) for plotting
    subset_grouped = subset_without_upper_bound.groupby(['Load', 'Algorithm'])['Avg'].mean().unstack()

    # Plot the bar plot (excluding the upper bound)
    ax = subset_grouped.plot(kind='bar', ax=plt.gca())

    plt.title(f'Bar Plot of Avg for {data_set} by Load and Algorithm')
    plt.ylabel('Average (Avg)')

    # Set the dynamic y-axis limits (only setting lower bound here)
    plt.ylim(lower_bound, None)  # No upper limit for the y-axis

    # Adding a horizontal line to indicate the "upper bound" from the data
    plt.axhline(y=upper_bound, color='red', linestyle='--', label=f'Upper Bound ({upper_bound:.2f})')  # Dashed red line

    plt.grid(True)

    # Adding value labels on each bar
    add_value_labels(ax)

    # Positioning the legend outside the plot area
    plt.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Show the plot
    plt.show()

