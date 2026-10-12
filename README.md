
# Smart Task Scheduling & Resource Allocation System

A Python-based DSA application for exploring task prioritization, dependency-aware scheduling, deadline-based job selection, and resource allocation through an interactive Streamlit dashboard.

## Features

- Priority-based task ordering using a heap
- Dependency validation using a directed graph
- Topological sorting and cycle detection
- Dependency-aware schedule generation
- Greedy deadline scheduling for independent, unit-time jobs
- 0/1 knapsack optimization using dynamic programming
- Interactive task editing and resource-budget controls
- Automated unit tests

## Technology Stack

- Python
- Streamlit
- Pandas
- Heaps and priority queues
- Graph algorithms
- Greedy algorithms
- Dynamic programming
- Git and GitHub

## Project Structure

```text
smart-task-scheduler/
├── app.py
├── algorithms.py
├── tests.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup on Windows

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python -m streamlit run app.py
```

Run automated tests in a second terminal:

```powershell
python -m unittest tests.py
```

## Algorithms

| Algorithm | Purpose |
|---|---|
| Heap / priority queue | Rank tasks by priority |
| Topological sort | Respect task dependencies |
| Greedy deadline scheduling | Select valuable unit-time jobs |
| 0/1 knapsack | Maximize task value under a capacity limit |

## Complexity

Let n be the number of tasks, V the number of graph vertices, E the number of dependency edges, D the maximum deadline, and C the resource capacity.

- Priority ordering: O(n log n)
- Topological sorting: O(V + E)
- Greedy deadline scheduling: O(n log n + nD)
- 0/1 knapsack: O(nC) time and O(nC) space in this implementation

## Important Assumptions

The dependency-aware scheduler calculates earliest possible start times without modeling shared worker availability.

The greedy scheduler supports independent jobs that each occupy one time slot. It does not support arbitrary task durations or dependencies.

The knapsack optimizer respects a time budget but does not enforce deadlines or dependencies.

## Future Improvements

- Gantt chart visualization
- Multiple-worker scheduling
- Resource conflict detection
- Persistent task storage
- Larger benchmark datasets and performance analysis

## Author

Om Pande

Academic DSA and software development project.
