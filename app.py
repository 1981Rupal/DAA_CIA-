import streamlit as st
import time
from utils import gen_points, euclidean_distances, plot_route, length_of_route
from algorithms import greedy_nearest_neighbor, held_karp, divide_and_conquer_tsp, tsp_backtracking, tsp_branch_and_bound

st.set_page_config(page_title="Delivery Dash (DAA algorithms)", layout="wide")
st.title("🚚 Delivery Dash — TSP using DAA Algorithms")
st.write("Compare Divide & Conquer, Greedy, Dynamic Programming, Backtracking, and Branch & Bound (syllabus-friendly).")

with st.sidebar:
    n = st.slider("Number of locations", 4, 20, 10)
    seed = st.number_input("Random seed", value=42)
    time_limit = st.number_input("Time limit for heavy solvers (seconds, 0 = no limit)", value=5, min_value=0)
    algos = st.multiselect("Algorithms to run", ["Greedy (Nearest Neighbor)","Held-Karp (DP Exact)","Backtracking (pruned)","Branch & Bound","Divide & Conquer (approx)"], default=["Greedy (Nearest Neighbor)"])
    run = st.button("Generate & Solve")

col1, col2 = st.columns([1,1])

if run:
    pts = gen_points(n=n, seed=int(seed))
    dist = euclidean_distances(pts)
    results = []
    def add(name, route, t0):
        L = length_of_route(route, dist)
        results.append((name, route, L, time.time()-t0))

    with col1:
        st.subheader("Map")
        st.pyplot(plot_route(pts, list(range(n)), title="Locations (indices shown)"))

    with col2:
        st.subheader("Solver outputs")
        if "Greedy (Nearest Neighbor)" in algos:
            t0 = time.time()
            r = greedy_nearest_neighbor(dist, start=0)
            add("Greedy (Nearest Neighbor)", r, t0)
        if "Held-Karp (DP Exact)" in algos:
            if n>20:
                st.warning("Held-Karp is expensive; reduce n to <=20 to run exact DP.")
            else:
                t0 = time.time()
                r = held_karp(dist)
                add("Held-Karp (DP Exact)", r, t0)
        if "Backtracking (pruned)" in algos:
            t0 = time.time()
            tl = None if time_limit==0 else float(time_limit)
            r = tsp_backtracking(dist, time_limit=tl)
            add("Backtracking (pruned)", r, t0)
        if "Branch & Bound" in algos:
            t0 = time.time()
            tl = None if time_limit==0 else float(time_limit)
            r = tsp_branch_and_bound(dist, time_limit=tl)
            add("Branch & Bound", r, t0)
        if "Divide & Conquer (approx)" in algos:
            t0 = time.time()
            r = divide_and_conquer_tsp(pts)
            add("Divide & Conquer (approx)", r, t0)

        if results:
            best = min(results, key=lambda x: x[2])
            st.success(f"Best: **{best[0]}** — length={best[2]:.2f}, time={best[3]:.3f}s")
            for name, route, L, dur in results:
                st.markdown(f"**{name}** — length={L:.2f}, time={dur:.3f}s")
                st.pyplot(plot_route(pts, route, title=f"{name} (L={L:.2f})"))
else:
    st.info("Configure parameters and click Generate & Solve.")