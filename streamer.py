# streamer.py
import streamlit as st
import random
from plotter import plot_hit_miss_ratio, plot_real_world_comparison, plot_hit_rate_over_time
from Structures import dynamic_Switcher

# Set up the page
st.set_page_config(layout="centered", page_title="Dynamic Cache Visualizer")
st.title("🔁 Dynamic Cache Strategy Visualizer")
st.markdown("""
This interactive tool demonstrates how LRU and LFU cache strategies perform
in different scenarios, and when it's best to switch dynamically between them.
""")

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

if ops and st.button("Run Simulation"):
    cache = dynamic_Switcher(capacity)
    hits = 0
    misses = 0
    switch_log = []
    hit_log = []

    for i, key in enumerate(ops):
        value = key * 10
        result, switched = cache.access(key, value)
        hits += result == "HIT"
        misses += result == "MISS"
        hit_log.append((i, hits / (i + 1)))
        if switched:
            switch_log.append((i, cache.strategy))

    st.success(f"✅ Simulation Complete: {hits} Hits / {misses} Misses")

    st.subheader("📊 Performance Graphs")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_hit_miss_ratio(hits, misses))
    with col2:
        st.pyplot(plot_real_world_comparison())

    st.pyplot(plot_hit_rate_over_time(hit_log))

    if switch_log:
        st.subheader("🔁 Strategy Switching Log")
        for step, strat in switch_log:
            st.markdown(f"- Switched to **{strat}** at operation #{step}")
    else:
        st.info("No switching occurred during this simulation.")
