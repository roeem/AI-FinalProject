import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file into a DataFrame
file_path = 'results.xlsx'  # Replace with the actual file path of your Excel file
df = pd.read_excel(file_path)

# Function to add labels on bars
def add_value_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        if not pd.isna(height):
            ax.annotate(f'{int(height):,}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')

load_order = ['Low', 'Medium', 'High']
algorithm_order = ['DFS', 'UCS', 'Astar']  # Adjusted to match the 'Algorithm' names in your data

# Convert 'Load' and 'Algorithm' to categorical types with the specified ordering
df['Load'] = pd.Categorical(df['Load'], categories=load_order, ordered=True)
df['Algorithm'] = pd.Categorical(df['Algorithm'], categories=algorithm_order, ordered=True)

# List of unique data sets
data_sets = df['Data set'].unique()

for data_set in data_sets:
    plt.figure(figsize=(12, 8))

    # Filter the data for the current data set
    subset = df[df['Data set'] == data_set].copy()

    # Ensure 'Expanded' is numeric
    subset['Expanded'] = pd.to_numeric(subset['Expanded'], errors='coerce')

    # Remove rows where 'Expanded' is NaN (e.g., rows with '-')
    subset = subset.dropna(subset=['Expanded'])

    # Check if there's any data left to plot
    if subset.empty:
        print(f"No data to plot for {data_set}.")
        continue

    # Group the data for plotting
    subset_grouped = subset.groupby(['Load', 'Algorithm'])['Expanded'].mean().unstack()

    # Plot the bar plot
    ax = subset_grouped.plot(kind='bar', ax=plt.gca())

    plt.title(f'Number of Expanded Nodes for {data_set} by Semester Load and Algorithm')
    plt.ylabel('Number of Expanded Nodes')
    plt.xlabel('Semester Load')

    plt.grid(True)

    # Adding value labels on each bar
    add_value_labels(ax)

    # Positioning the legend
    plt.legend(title='Algorithm', loc='upper right', borderaxespad=0.1)

    # Show the plot
    plt.show()
