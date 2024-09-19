# Degree Planning Project (DPP)

Welcome to the Degree Planning Project! This repository provides tools for optimizing degree planning using
various local search and graph search algorithms.

## Getting Started

### 1. Clone the Repository

Start by cloning the repository and navigating to the project directory:

```bash
git clone https://github.com/roeem/AI-FinalProject.git
cd AI-FinalProject
```

### 2. Checkout the Correct Branch

Ensure you are on the correct branch:

```bash
git checkout MainBranch
```

### 3. Install Required Dependencies

Install the necessary Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Input Files

Place your input files in the `input_files` directory. 
Example input files are already provided in this directory. 
The files should be in JSON format. 
You can refer to these example files to understand the required format. The JSON files should follow a schema that includes course details, prerequisites, and other degree requirements.


## Running Algorithms
This project includes several algorithms for optimizing degree planning. The available algorithms are:

- **DFS (Depth-First Search):** Explores as far as possible along each branch before backtracking.
- **UCS (Uniform Cost Search):** Expands the least costly node first.
- **A\* (A-star Search):** Uses both cost and heuristic to find the optimal path.
- **Hill Climbing:** Continuously moves towards the direction of increasing elevation or value.
- **Simulated Annealing:** Uses probabilistic decisions to escape local optima and find a global optimum.
- **Stochastic Beam Search:** Uses a beam width to explore a subset of neighbors in each iteration.

To run an algorithm, use the following command format:
```
python dpp.py <algorithm> <input file> <semester load>
```
Where:

- `<algorithm>` is one of the available algorithms:
  - `dfs` for Depth-First Search. 
  - `ucs` for Uniform Cost Search.
  - `astar` for A* Search. 
  - `hill` for Hill Climbing
  - `sa` for Simulated Annealing.
  - `beam` for Stochastic Beam Search
- `<input file>` is the name of the JSON file located in the `input_files` directory.
- `<semester load>` can be one of the following options: `low`, `medium`, `high`.

### Example
To run the A* Search algorithm with the input file cs2.json and a medium semester load:
```bash
python dpp.py astar cs2.json medium
```

### Viewing Results

Once you've run the program, you can view the results in two ways:

1. **Console/Terminal Output**:  
   After executing the program, you'll see the results displayed directly in the console, command-line, or terminal. This includes detailed information about the selected degree plan, courses taken each semester, and overall statistics like total credits and average grade.

2. **DegreePlan.html File**:  
   In addition to the console output, the program generates an HTML file called `DegreePlan.html`. You can open this file in any web browser (e.g., Chrome, Firefox) to view a more user-friendly, formatted version of your degree plan. Simply double-click the file or right-click and choose **Open with** to select your preferred browser.
