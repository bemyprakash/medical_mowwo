import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import sys
import os
import json

st.set_page_config(page_title="Medical Supply Scheduling Optimization", layout="centered")

def to_serializable(obj):
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    elif hasattr(obj, "tolist"):
        return obj.tolist()
    else:
        return obj

# Ensure src is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import run_optimization  # Make sure main.py has run_optimization()

# Sidebar with help
st.sidebar.title("About")
st.sidebar.info(
    "This tool demonstrates the Multi-Objective Water Wave Optimization (MOWWO) algorithm for integrated civilian-military scheduling of medical supplies. "
    "You can select an instance, run the optimizer, and explore the Pareto-optimal solutions."
)

st.title("Medical Supply Scheduling Optimization Demo")
st.write("""
This app demonstrates the results of the Multi-Objective Water Wave Optimization (MOWWO) algorithm for integrated civilian-military scheduling of medical supplies.
""")

# Optionally, let user pick an instance
instance_idx = st.number_input("Instance index (0 for first):", min_value=0, value=0, step=1)

if st.button("Run Optimization"):
    with st.spinner("Running optimization..."):
        satisfaction, cost_obj, results = run_optimization(instance_idx)
        st.session_state['satisfaction'] = satisfaction
        st.session_state['cost_obj'] = cost_obj
        st.session_state['results'] = results

# Use session state for all downstream widgets
if 'results' in st.session_state:
    satisfaction = st.session_state['satisfaction']
    cost_obj = st.session_state['cost_obj']
    results = st.session_state['results']

    # Table of all solutions
    st.subheader("Pareto Front Table")
    st.dataframe({
        "Satisfaction Rate (%)": satisfaction,
        "Scaled Cost Objective": cost_obj
    })

    # Pareto front plot
    fig, ax = plt.subplots()
    ax.scatter(satisfaction, cost_obj, c='blue')
    ax.set_xlabel("Supply Satisfaction Rate (%)")
    ax.set_ylabel("Scaled Cost Objective")
    ax.set_title("Pareto Front of Solutions")
    st.pyplot(fig)
    st.success("Optimization complete!")

    # Solution details
    st.write("Select a solution to view details:")
    selected = st.selectbox("Solution", range(len(results)))
    sol = results[selected]
    sol_serializable = to_serializable(sol)
    st.json(sol_serializable)

    # 1. Solution Summary Table
    st.subheader("Solution Summary")
    summary = {
        "Total Supply Delivered": int(sol['xijk'].sum() + sol['xjjk'].sum()),
        "Total Patients Transferred": int(sol['yo'].sum() + sol['ys'].sum() + sol['ym'].sum() + sol['yv'].sum()),
        "Overall Satisfaction Rate (%)": satisfaction[selected],
        "Scaled Cost Objective": cost_obj[selected]
    }
    st.table(summary)

    # 2. Allocation Heatmaps
    st.subheader("Supply Allocation Heatmap (xijk: Military to Civilian)")
    fig, ax = plt.subplots()
    sns.heatmap(sol['xijk'].sum(axis=2), annot=True, fmt=".0f", ax=ax, cmap="Blues")
    ax.set_xlabel("Military Facility")
    ax.set_ylabel("Civilian Facility")
    st.pyplot(fig)

    st.subheader("Normal Residents Transferred (yo)")
    fig, ax = plt.subplots()
    sns.heatmap(sol['yo'], annot=True, fmt=".0f", ax=ax, cmap="Greens")
    ax.set_xlabel("Military Facility")
    ax.set_ylabel("Civilian Facility")
    st.pyplot(fig)

    st.subheader("Suspected Cases Transferred (ys)")
    fig, ax = plt.subplots()
    sns.heatmap(sol['ys'], annot=True, fmt=".0f", ax=ax, cmap="YlOrBr")
    ax.set_xlabel("Military Facility")
    ax.set_ylabel("Civilian Facility")
    st.pyplot(fig)

    st.subheader("Mild Cases Transferred (ym)")
    fig, ax = plt.subplots()
    sns.heatmap(sol['ym'], annot=True, fmt=".0f", ax=ax, cmap="Purples")
    ax.set_xlabel("Military Facility")
    ax.set_ylabel("Civilian Facility")
    st.pyplot(fig)

    st.subheader("Severe Cases Transferred (yv)")
    fig, ax = plt.subplots()
    sns.heatmap(sol['yv'], annot=True, fmt=".0f", ax=ax, cmap="Reds")
    ax.set_xlabel("Military Facility")
    ax.set_ylabel("Civilian Facility")
    st.pyplot(fig)

    # 4. Downloadable Reports (already included above)
    st.download_button(
        label="Download this solution as JSON",
        data=json.dumps(sol_serializable, indent=2),
        file_name=f"solution_{selected+1}.json",
        mime="application/json"
    )

    # 5. Interactive Network Graph (static version)
    st.subheader("Supply/Patient Flow Network")
    G = nx.DiGraph()
    m, n = sol['xijk'].shape[0], sol['xijk'].shape[1]
    for i in range(m):
        for j in range(n):
            flow = sol['xijk'][i][j].sum()
            if flow > 0:
                G.add_edge(f"Civilian {i+1}", f"Military {j+1}", weight=flow)
    for i in range(m):
        for j in range(n):
            flow = sol['yo'][i][j]
            if flow > 0:
                G.add_edge(f"Civilian {i+1}", f"Military {j+1}", weight=flow, color='green')
    pos = nx.spring_layout(G, seed=42)
    edge_colors = [G[u][v].get('color', 'blue') for u, v in G.edges()]
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color=edge_colors, width=[w/5 for w in edge_weights], ax=ax)
    st.pyplot(fig)

else:
    st.info("Click 'Run Optimization' to start.")

