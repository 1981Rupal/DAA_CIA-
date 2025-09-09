Delivery Dash — TSP using DAA algorithms

How to run:
1. Create a virtualenv and install requirements:
   pip install -r requirements.txt
2. Run the Streamlit app:
   streamlit run app.py

Algorithms included:
- Greedy (Nearest Neighbor)
- Held-Karp (Dynamic Programming exact)
- Backtracking (with pruning; optional time limit)
- Branch & Bound (with simple lower bound; optional time limit)
- Divide & Conquer (approximate merge by spatial split)
