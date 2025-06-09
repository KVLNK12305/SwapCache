# streamer.py
import streamlit as st
import random
from plotter import plot_hit_miss_ratio, plot_hit_rate_over_time
from Structures import dynamic_Switcher
import matplotlib.pyplot as plt
import numpy as np

# Set up the page
st.set_page_config(layout="centered", page_title="Dynamic Cache Visualizer")
st.title("🔁 Dynamic Cache Strategy Visualizer")
st.markdown("""
This interactive tool demonstrates how LRU and LFU cache strategies perform
in different scenarios, and when it's best to switch dynamically between them.
""")
def plot_real_world_comparison():
    companies = ["Amazon", "Flipkart", "Alibaba"]
    lru = [75, 68, 60]
    lfu = [72, 73, 66]
    dynamic = [80, 78, 73]

    x = np.arange(len(companies))
    width = 0.2
    fig, ax = plt.subplots()
    ax.bar(x - width, lru, width, label="LRU")
    ax.bar(x, lfu, width, label="LFU")
    ax.bar(x + width, dynamic, width, label="LRU+LFU")

    ax.set_xticks(x)
    ax.set_xticklabels(companies)
    ax.set_ylabel("Efficiency %")
    ax.set_title("Cache Strategy Comparison in E-Commerce")
    ax.legend()
    st.pyplot(fig)

st.subheader("📥 Input Simulation")
capacity = st.number_input("Cache Capacity", min_value=1, value=5)
mode = st.radio("Input Mode", ["Random", "Manual"], horizontal=True)

operation_count = 0
ops = []

if mode == "Random":
    operation_count = st.slider("Number of Operations", min_value=10, max_value=100, value=30)
    keys_range = st.slider("Range of Key Values", min_value=1, max_value=100, value=20)
    if st.button("Generate Random Access Sequence"):
        ops = [random.randint(1, keys_range) for _ in range(operation_count)]
        st.session_state["generated_ops"] = ops

    if "generated_ops" in st.session_state:
        st.write("### 🔄 Generated Access Sequence")
        ops = st.session_state["generated_ops"]
        st.code(f"{ops}")

else:  # Manual
    manual_input = st.text_area("Enter comma-separated keys (e.g., 1,2,3,2,1)")
    if manual_input:
        try:
            ops = [int(x.strip()) for x in manual_input.split(",") if x.strip().isdigit()]
            st.write("### 🔄 Provided Access Sequence")
            st.code(f"{ops}")
        except ValueError:
            st.error("Please enter valid integers separated by commas.")

