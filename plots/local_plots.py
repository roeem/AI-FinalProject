import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file into a DataFrame
file_path = '../Documents/results.xlsx'  # Replace with the actual file path of your Excel file
df = pd.read_excel(file_path, sheet_name='local')
# Function to add labels on bars
def add_value_labels(ax):
    for p in ax.patches:
        if not pd.isna(p.get_height()):
            ax.annotate(f'{p.get_height():.2f}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', xytext=(0, 10), textcoords='offset points')

load_order = ['Low', 'Medium', 'High']
algorithm_order = ['Simulated Annealing', 'Hill Climbing', 'Stochastic Beam Search']  # Ensure these match the names in your data

# Convert 'Load' to a categorical type with the specified ordering
df['Load'] = pd.Categorical(df['Load'], categories=load_order, ordered=True)

# List of unique data sets
data_sets = df['Data set'].unique()

for data_set in data_sets:
    plt.figure(figsize=(12, 8))  # Increase the figure size to allow more space for the legend

    # Filter the data for the current data set
    subset = df[df['Data set'] == data_set].copy()  # Use copy to avoid SettingWithCopyWarning

    # Ensure 'Avg' is numeric
    subset['Time'] = pd.to_numeric(subset['Time'], errors='coerce')

    # Check if 'Upper Bound' row exists in the subset
    if 'Upper Bound' in subset['Algorithm'].values:
        # Extract the upper bound value
        upper_bound_row = subset[subset['Algorithm'] == 'Upper Bound']
        upper_bound = upper_bound_row['Time'].values[0]

        # Remove the 'Upper Bound' row from the subset
        subset_without_upper_bound = subset[subset['Algorithm'] != 'Upper Bound']
    else:
        # If no 'Upper Bound' row, proceed without removing any row
        upper_bound = subset['Time'].max()
        subset_without_upper_bound = subset

    # Check if there's any data left after removing the upper bound row
    if subset_without_upper_bound.empty:
        print(f"No data to plot for {data_set} after removing the upper bound row.")
        continue  # Skip this plot if no data is left

    # Calculate dynamic lower bound based on the data
    lower_bound = max(40, subset_without_upper_bound['Time'].min() - 5)  # Set lower bound to the minimum value of Avg or 40

    # Determine the algorithms present in this subset
    algorithms_present = subset_without_upper_bound['Algorithm'].unique()

    # Create ordered list of algorithms present, preserving the order specified in algorithm_order
    algorithms_present_ordered = [alg for alg in algorithm_order if alg in algorithms_present]

    # Set 'Algorithm' as categorical with the ordered categories
    subset_without_upper_bound['Algorithm'] = pd.Categorical(
        subset_without_upper_bound['Algorithm'],
        categories=algorithms_present_ordered,
        ordered=True
    )

    # Group the remaining data (without the upper bound row) for plotting
    subset_grouped = subset_without_upper_bound.groupby(['Load', 'Algorithm'])['Time'].mean().unstack()

    # Plot the bar plot (excluding the upper bound row)
    ax = subset_grouped.plot(kind='bar', ax=plt.gca())

    plt.title(f'Average execution time for "{data_set}" by semester load')
    plt.ylabel('Execution Time')
    plt.xlabel('Semester Load')
    plt.xticks(rotation=0)

    # Set the dynamic y-axis limits
    plt.ylim(0, 300)  # Set upper limit slightly above the upper bound

    # Adding a horizontal line to indicate the "upper bound" from the data
    # plt.axhline(y=upper_bound, color='red', linestyle='--', label=f'Upper Bound ({upper_bound:.2f})')  # Dashed red line

    plt.grid(True)

    # Adding value labels on each bar
    add_value_labels(ax)

    # Positioning the legend
    plt.legend(title='Algorithm', loc='upper right', borderaxespad=0.1)

    # Show the plot
    plt.show()
