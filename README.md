# MOWWO Medical Supply Scheduling

## Overview
This project implements a Multi-Objective Water Wave Optimization (MOWWO) algorithm to address a bi-objective constrained integer programming problem related to medical supply scheduling during epidemics. The goal is to optimize the allocation of medical supplies to various healthcare facilities while considering multiple objectives such as minimizing costs and maximizing service coverage.

## Problem Definition
The medical supply scheduling problem involves determining the optimal distribution of medical supplies to healthcare facilities during an epidemic. The problem is modeled as a bi-objective optimization task, where the objectives may include:
1. Minimizing the total cost of supplies.
2. Maximizing the coverage of medical services provided to patients.

## MOWWO Algorithm
The MOWWO algorithm is inspired by the natural phenomenon of water waves and is designed to find a set of optimal solutions that balance the trade-offs between the conflicting objectives. The algorithm includes:
- Initialization of a diverse population of solutions.
- Evolution of solutions through iterative processes.
- Non-dominated sorting to identify Pareto-optimal solutions.

## Project Structure
- `src/algorithms/mowwo.py`: Implementation of the MOWWO algorithm.
- `src/problems/medical_supply_scheduling.py`: Definition of the medical supply scheduling problem.
- `src/utils/constraints.py`: Utility functions for constraint handling.
- `src/data/sample_instance.csv`: Sample dataset for testing.
- `src/main.py`: Entry point for running the application.
- `src/test_streamlit.py`: Only for testing purpose of Streamlit, not vital.


## Requirements
To run this project, you will need the following Python packages:
- numpy
- pandas
- scipy

You can install the required packages using the following command:
```
pip install -r requirements.txt
```

## Running the Project

You can use this project in two ways:

### 1. Command-Line Mode (Basic Output)
To execute the MOWWO algorithm and see the results in the terminal, run:
```
python src/main.py
```
This will print the optimization results and basic output to the console.

---

### 2. Interactive Visualization (Recommended)
For a richer, interactive experience, use the Streamlit GUI. This allows you to:
- Select and run different problem instances
- Visualize the Pareto front and solution details
- Explore allocations, transfers, and download solutions

**To launch the GUI:**
```
streamlit run src/visualization_app.py
```

** To use Live Tool , Go to https://huggingface.co/spaces/t2codes/medical_MoWWO_APP

Then open the provided local URL (usually [http://localhost:8501](http://localhost:8501)) in your browser.

---

## About `visualization_app.py`

The `visualization_app.py` file provides an interactive dashboard for exploring the results of the MOWWO algorithm. Features include:
- Instance selection and optimization run
- Pareto front visualization
- Solution summary and allocation heatmaps
- Downloadable solution reports
- Network diagrams of supply and patient flows

This is the recommended way to demonstrate and analyze the tool, especially for presentations or stakeholder engagement.

---

# Input Variables

Instance Variable Reference

| Column | Meaning |
|--------|---------|
| m | Number of civilian medical services (hospitals/clinics) |
| n | Number of military medical services |
| K | Number of supply types (total) |
| K1 | Number of non-fixed supply types |
| K2 | Number of fixed supply types |
| wk | List of weights for each supply type (length K) |
| ro | List: resource requirement per normal resident for each supply type (length K) |
| rs | List: resource requirement per suspected case for each supply type (length K) |
| rm | List: resource requirement per mild case for each supply type (length K) |
| rv | List: resource requirement per severe case for each supply type (length K) |
| aik | Initial amount of each supply at each civilian medical service (m x K array) |
| ajk | Initial amount of each supply at each military medical service (n x K array) |
| cijk | Cost to deliver one unit of non-fixed supply from military to civilian (m x n x K1 array) |
| cjjk | Cost to deliver one unit of non-fixed supply from closed to open military (n x n x K1 array) |
| coij | Cost to deliver one normal resident from civilian to military (m x n array) |
| csij | Cost to deliver one suspected case from civilian to military (m x n array) |
| cmij | Cost to deliver one mild case from civilian to military (m x n array) |
| cvij | Cost to deliver one severe case from civilian to military (m x n array) |
| bjk | Minimum amount of each supply to reserve at each military medical service (n x K1 array) |
| no_i | List: number of normal residents at each civilian medical service (length m) |
| ns_i | List: number of suspected cases at each civilian medical service (length m) |
| nm_i | List: number of mild cases at each civilian medical service (length m) |
| nv_i | List: number of severe cases at each civilian medical service (length m) |
| no_j | List: number of normal residents at each military medical service (length n) |
| ns_j | List: number of suspected cases at each military medical service (length n) |
| nm_j | List: number of mild cases at each military medical service (length n) |
| nv_j | List: number of severe cases at each military medical service (length n) |
| C | Upper bound for total scheduling cost |
| S | Lower bound for overall supply satisfaction rate |

---

## Conclusion
This project provides a framework for optimizing medical supply scheduling during epidemics using a multi-objective approach. The MOWWO algorithm offers a robust method for exploring trade-offs between conflicting objectives, ultimately aiding in effective decision-making in healthcare logistics. The included Streamlit app makes it easy to demonstrate and communicate the value of the optimization results to stakeholders through interactive visualizations.


