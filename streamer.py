# streamer.py
import streamlit as st
import random
from plotter import plot_hit_miss_ratio, plot_hit_rate_over_time, plot_real_world_comparison, plot_benchmarks, plot_strategy_switches, plot_cache_state_evolution
from structures import DynamicCache  
import matplotlib.pyplot as plt
import numpy as np

# Set up the pag
st.set_page_config(layout="wide", page_title="Dynamic Cache Visualizer")

# Header
st.title("Dynamic Cache Strategy Visualizer")
st.markdown(""" 
This interactive tool demonstrates how LRU and LFU cache strategies perform in different scenarios, 
and when it's best to switch dynamically between them.
""")


col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Real-World Performance Comparison")
    try:
        fig = plot_real_world_comparison()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)  # Free memory
    except Exception as e:
        st.error(f"Error loading real-world comparison: {str(e)}")

with col2:
    st.subheader("🏆 Benchmark Results")
    try:
        fig1 = plot_benchmarks()
        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)  # Free memory
    except Exception as e:
        st.error(f"Error loading benchmarks: {str(e)}")

# Divider
st.divider()

# Input simulation section
st.subheader("Cache Simulation Configuration")

# Configuration in columns
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

# Input section based on mode
if mode == "Random":
    st.markdown("#### 🎲 Random Sequence Generation")
    
    # Random mode controls in columns
    rand_col1, rand_col2, rand_col3 = st.columns([1, 1, 1])
    
    with rand_col1:
        operation_count = st.slider("Number of Operations", min_value=10, max_value=100, value=30)
    
    with rand_col2:
        keys_range = st.slider("Range of Key Values", min_value=1, max_value=100, value=20)
    
    with rand_col3:
        st.write("")  # Spacer
        generate_btn = st.button("🎯 Generate Random Sequence", type="primary", use_container_width=True)
    
    if generate_btn:
        ops = [random.randint(1, keys_range) for _ in range(operation_count)]
        st.session_state["generated_ops"] = ops
        st.success(f"Generated {len(ops)} operations with keys ranging from 1 to {keys_range}")
    
    if "generated_ops" in st.session_state:
        ops = st.session_state["generated_ops"]
        
        # Display sequence in an expandable section
        with st.expander("🔄 View Generated Access Sequence", expanded=False):
            # Format the sequence nicely
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

else:  # Manual mode
    st.markdown("#### ✍️ Manual Sequence Input")
    
    manual_input = st.text_area(
        "Enter comma-separated keys", 
        placeholder="Example: 1,2,3,2,1,4,3,2,5,1",
        help="Enter integers separated by commas. Spaces are automatically handled.",
        height=100
    )
    
    if manual_input:
        try:
            ops = [int(x.strip()) for x in manual_input.split(",") if x.strip() and x.strip().lstrip('-').isdigit()]  # Handle negative numbers
            
            if ops:
                st.success(f"Successfully parsed {len(ops)} operations")
                
                # Show preview and stats side by side
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

# Simulation and Visualization Section
ops = None

# Get operations from either mode
if mode == "Random" and "generated_ops" in st.session_state:
    ops = st.session_state["generated_ops"]
elif mode == "Manual" and manual_input:
    try:
        ops = [int(x.strip()) for x in manual_input.split(",") if x.strip() and x.strip().lstrip('-').isdigit()]
    except:
        ops = None

# Display simulation when ops are available
if ops and len(ops) > 0:
    st.divider()
    st.markdown("### Cache Simulation & Results")
    
    # Simulation controls
    sim_col1, sim_col2, sim_col3 = st.columns([1, 1, 1])
    
    with sim_col1:
        st.metric("Cache Capacity", capacity)
    with sim_col2:
        st.metric("Operations", len(ops))
    with sim_col3:
        run_btn = st.button("▶️ Run Simulation", type="primary", use_container_width=True)
    
    # Auto-run simulation or run on button click
    if run_btn or st.session_state.get('auto_simulate', False):
        if run_btn:
            st.session_state['auto_simulate'] = True
        
        try:
            # Run simulation using the DynamicCache class
            with st.spinner("Running cache simulation..."):
                cache = DynamicCache(capacity)
                
                # Track hits, misses, and other metrics
                hits = 0
                misses = 0
                hit_log = []
                strategy_switches = []
                current_strategy = cache.current_strategy
                
                # Run operations
                for i, key in enumerate(ops):
                    result = cache.get(key)
                    if result != -1:
                        hits += 1
                    else:
                        misses += 1
                        # PUT operation for cache miss
                        cache.put(key, f"value_{key}")
                    # logs of strategy switches
                    if cache.current_strategy != current_strategy:
                        strategy_switches.append(f"Step {i+1}: Switched to {cache.current_strategy}")
                        current_strategy = cache.current_strategy
                    # running hit rate
                    total_so_far = hits + misses
                    hit_rate_so_far = (hits / total_so_far) * 100 if total_so_far > 0 else 0
                    hit_log.append((i+1, hit_rate_so_far))
            
            # Calculate final metrics
            total_ops = hits + misses
            hit_rate = (hits / total_ops * 100) if total_ops > 0 else 0
            
            st.success(f"✅ Simulation completed! Hit rate: {hit_rate:.1f}%")
            
            # Display key metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Hits", hits, delta=f"{hit_rate:.1f}%")
            with metric_col2:
                st.metric("Misses", misses, delta=f"{(misses/total_ops*100) if total_ops > 0 else 0:.1f}%")
            with metric_col3:
                st.metric("Hit Rate", f"{hit_rate:.1f}%")
            with metric_col4:
                efficiency = "🟢 High" if hit_rate > 70 else "🟡 Medium" if hit_rate > 40 else "🔴 Low"
                st.metric("Efficiency", efficiency)
            
            # Display graphs side by side
            st.markdown("#### 📊 Performance Visualizations")
            
            graph_col1, graph_col2 = st.columns([1, 1])
            
            with graph_col1:
                st.markdown("**Hit vs Miss Ratio**")
                if hits > 0 or misses > 0:
                    try:
                        fig_ratio = plot_hit_miss_ratio(hits, misses)
                        st.pyplot(fig_ratio, use_container_width=True)
                        plt.close(fig_ratio)  # Free memory
                    except Exception as e:
                        st.error(f"Error plotting hit/miss ratio: {str(e)}")
                        # Fallback simple chart
                        labels = ['Hits', 'Misses']
                        sizes = [hits, misses]
                        colors = ['#28a745', '#dc3545']
                        
                        fig, ax = plt.subplots(figsize=(8, 6))
                        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                        ax.set_title('Hit vs Miss Ratio')
                        st.pyplot(fig, use_container_width=True)
                        plt.close(fig)
                else:
                    st.info("No hit/miss data to display")
            
            with graph_col2:
                st.markdown("**Hit Rate Over Time**")
                if hit_log and len(hit_log) > 1:
                    try:
                        fig_time = plot_hit_rate_over_time(hit_log)
                        st.pyplot(fig_time, use_container_width=True)
                        plt.close(fig_time) 
                    except Exception as e:
                        st.error(f"Error plotting hit rate over time: {str(e)}")
                        steps, rates = zip(*hit_log)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(steps, rates, marker='o', linewidth=2, markersize=4)
                        ax.set_xlabel('Operation Number')
                        ax.set_ylabel('Hit Rate (%)')
                        ax.set_title('Hit Rate Over Time')
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig, use_container_width=True)
                        plt.close(fig)
                else:
                    st.info("Insufficient data for time-series plot")
            if strategy_switches and len(strategy_switches) > 0:
                st.markdown("#### 🔄 Strategy Switching Analysis")
                switch_col1, switch_col2 = st.columns([1, 1])
                
                with switch_col1:
                    st.metric("Total Switches", len(strategy_switches))
                
                with switch_col2:
                    switch_rate = (len(strategy_switches) / len(ops)) * 100
                    st.metric("Switch Rate", f"{switch_rate:.1f}%")
                
                with st.expander("View Strategy Switch Details", expanded=False):
                    for i, switch in enumerate(strategy_switches):
                        st.write(f"**Switch {i+1}:** {switch}")
            else:
                st.info("No strategy switches occurred during this simulation")
            
            # Additional insights
            with st.expander("Detailed Analysis", expanded=False):
                unique_keys = len(set(ops))
                most_frequent = max(set(ops), key=ops.count) if ops else None
                key_frequency = ops.count(most_frequent) if most_frequent else 0
                
                st.markdown(f"""
                **Performance Analysis:**
                - Total operations processed: {total_ops}
                - Unique keys accessed: {unique_keys}
                - Cache utilization: {min(unique_keys, capacity)}/{capacity} slots
                - Most accessed key: {most_frequent} ({key_frequency} times)
                - Final strategy: {cache.current_strategy}
                
                **Cache Efficiency Breakdown:**
                - **Overall Performance:** {efficiency} ({hit_rate:.1f}% hit rate)
                - **Key Diversity:** {'High' if unique_keys > capacity * 2 else 'Medium' if unique_keys > capacity else 'Low'}
                - **Access Pattern:** {'Repetitive' if key_frequency > len(ops) * 0.3 else 'Diverse'}
                - **Cache Pressure:** {'High' if unique_keys > capacity * 1.5 else 'Normal'}
                
                **Recommendations:**
                """)
                
                if hit_rate < 40:
                    st.warning("🔴 Consider increasing cache capacity or optimizing access patterns")
                elif hit_rate < 70:
                    st.info("🟡 Performance is moderate - dynamic switching may help")
                else:
                    st.success("🟢 Excellent cache performance!")
                
                # Show access sequence sample
                st.markdown("**Access Sequence Sample:**")
                sample_size = min(50, len(ops))
                sample_ops = ops[:sample_size]
                st.code(", ".join(map(str, sample_ops)) + ("..." if len(ops) > sample_size else ""))
        
        except Exception as e:
            st.error(f"❌ Simulation failed: {str(e)}")
            st.info("Make sure your `DynamicCache` class is properly implemented and accessible.")
            
            # Show debug info
            with st.expander("🔧 Debug Information", expanded=False):
                st.write("**Error Details:**")
                st.code(str(e))
                st.write("**Available classes from structures module:**")
                try:
                    import structures
                    available_classes = [attr for attr in dir(structures) if not attr.startswith('_') and isinstance(getattr(structures, attr), type)]
                    st.code(", ".join(available_classes))
                except Exception as import_error:
                    st.code(f"Import error: {str(import_error)}")
    
    else:
        # Show preview without simulation
        st.info("👆 Click 'Run Simulation' to see cache performance analysis with interactive graphs!")
        
        # Preview the sequence
        with st.expander("🔍 Preview Access Sequence", expanded=False):
            preview_size = min(30, len(ops))
            preview_ops = ops[:preview_size]
            st.code(", ".join(map(str, preview_ops)) + ("..." if len(ops) > preview_size else ""))
            
            prev_col1, prev_col2, prev_col3 = st.columns(3)
            with prev_col1:
                st.metric("Total Operations", len(ops))
            with prev_col2:
                st.metric("Unique Keys", len(set(ops)))
            with prev_col3:
                st.metric("Key Range", f"{min(ops)}-{max(ops)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Dynamic Cache Strategy Visualizer | Built with Streamlit</p>
    <p><em>Analyze and optimize your caching strategies with real-time visualizations</em></p>
</div>
""", unsafe_allow_html=True)