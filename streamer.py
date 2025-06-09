# streamer.py
import streamlit as st
import random
from plotter import plot_hit_miss_ratio, plot_hit_rate_over_time, plot_real_world_comparison, plot_benchmarks
from Structures import dynamic_Switcher
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(layout="wide", page_title="Dynamic Cache Visualizer")

# Header
st.title("🔁 Dynamic Cache Strategy Visualizer")
st.markdown(""" 
This interactive tool demonstrates how LRU and LFU cache strategies perform in different scenarios, 
and when it's best to switch dynamically between them.
""")


col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Real-World Performance Comparison")
    fig = plot_real_world_comparison()
    st.pyplot(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Benchmark Results")
    fig1 = plot_benchmarks()
    st.pyplot(fig1, use_container_width=True)


st.divider()


st.subheader("📥 Cache Simulation Configuration")

config_col1, config_col2, config_col3 = st.columns([1, 1, 1])

with config_col1:
    capacity = st.number_input("Cache Capacity", min_value=1, value=5, help="Maximum number of items the cache can hold")

with config_col2:
    mode = st.radio("Input Mode", ["Random", "Manual"], horizontal=True, 
                   help="Choose how to generate the access sequence")

with config_col3:
    if mode == "Random":
        st.metric("Mode", "Random Generation", "🎲")
    else:
        st.metric("Mode", "Manual Input", "✍️")


if mode == "Random":
    st.markdown("#### 🎲 Random Sequence Generation")
    
    rand_col1, rand_col2, rand_col3 = st.columns([1, 1, 1])
    
    with rand_col1:
        operation_count = st.slider("Number of Operations", min_value=10, max_value=100, value=30)
    
    with rand_col2:
        keys_range = st.slider("Range of Key Values", min_value=1, max_value=100, value=20)
    
    with rand_col3:
        st.write("")
        generate_btn = st.button("🎯 Generate Random Sequence", type="primary", use_container_width=True)
    
    if generate_btn:
        ops = [random.randint(1, keys_range) for _ in range(operation_count)]
        st.session_state["generated_ops"] = ops
        st.success(f"Generated {len(ops)} operations with keys ranging from 1 to {keys_range}")
    
    if "generated_ops" in st.session_state:
        ops = st.session_state["generated_ops"]
        with st.expander("🔄 View Generated Access Sequence", expanded=False):
            formatted_ops = ", ".join(map(str, ops))
            st.code(formatted_ops, language="text")
            
            # Show some statistics
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            with stats_col1:
                st.metric("Total Operations", len(ops))
            with stats_col2:
                st.metric("Unique Keys", len(set(ops)))
            with stats_col3:
                st.metric("Most Frequent", max(set(ops), key=ops.count))
            with stats_col4:
                st.metric("Key Range", f"{min(ops)}-{max(ops)}")

else: 
    st.markdown("#### ✍️ Manual Sequence Input")
    
    manual_input = st.text_area(
        "Enter comma-separated keys", 
        placeholder="Example: 1,2,3,2,1,4,3,2,5,1",
        help="Enter integers separated by commas. Spaces are automatically handled.",
        height=100
    )
    
    if manual_input:
        try:
            ops = [int(x.strip()) for x in manual_input.split(",") if x.strip() and x.strip().isdigit()]
            
            if ops:
                st.success(f"✅ Successfully parsed {len(ops)} operations")
                preview_col, stats_col = st.columns([2, 1])
                
                with preview_col:
                    with st.expander("🔄 Preview Access Sequence", expanded=True):
                        formatted_ops = ", ".join(map(str, ops))
                        st.code(formatted_ops, language="text")
                
                with stats_col:
                    st.markdown("**📈 Sequence Statistics**")
                    st.metric("Total Operations", len(ops))
                    st.metric("Unique Keys", len(set(ops)))
                    st.metric("Key Range", f"{min(ops)}-{max(ops)}")
            else:
                st.warning("No valid integers found. Please check your input.")
                
        except ValueError:
            st.error("❌ Please enter valid integers separated by commas.")


if 'ops' in locals() and ops:
    st.divider()
    st.markdown("#### 🚀 Ready to Simulate!")
    
    sim_col1, sim_col2 = st.columns([1, 1])
    
    with sim_col1:
        st.info(f"**Cache Capacity:** {capacity} items")
        st.info(f"**Sequence Length:** {len(ops)} operations")
    
    with sim_col2:
        if st.button("▶️ Start Cache Simulation", type="primary", use_container_width=True):
            st.balloons()
            st.success("Simulation started! (Connect to your simulation logic here)")