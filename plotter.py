import matplotlib.pyplot as plt
import numpy as np

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
    ax.set_facecolor('white')
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('white')
    ax.set_ylabel("Efficiency %")
    ax.set_title("Cache Strategy Comparison in E-Commerce")
    ax.legend()
    return fig

def plot_benchmarks():
    workloads = ["E-commerce", "Social Media", "Analytics", "Mixed Pattern"]
    lru = [78.2, 82.1, 69.5, 75.8]
    lfu = [71.4, 74.8, 83.2, 76.2]
    swapcache = [86.7, 89.3, 88.1, 87.4]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(workloads, lru, marker='o', label="LRU Only")
    ax.plot(workloads, lfu, marker='s', label="LFU Only")
    ax.plot(workloads, swapcache, marker='^', label="SwapCache (Dynamic)")

    ax.set_title("Cache Strategy Efficiency Across Workload Types")
    ax.set_xlabel("Workload Type")
    ax.set_ylabel("Efficiency (%)")
    ax.set_ylim(60, 95)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    fig.tight_layout()
    
    return fig


def plot_hit_miss_ratio(hits, misses):
    """
    Create a bar chart showing hit vs miss ratio with enhanced styling
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Data and colors
    categories = ["Hits", "Misses"]
    values = [hits, misses]
    colors = ["#2E8B57", "#DC143C"]  # Sea green and crimson
    
    # Create bars with better styling
    bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Styling
    ax.set_title("Cache Hit vs Miss Ratio", fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel("Count", fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add percentage annotations
    total = hits + misses
    if total > 0:
        hit_pct = (hits / total) * 100
        miss_pct = (misses / total) * 100
        ax.text(0, hits/2, f'{hit_pct:.1f}%', ha='center', va='center', 
                fontweight='bold', fontsize=14, color='white')
        ax.text(1, misses/2, f'{miss_pct:.1f}%', ha='center', va='center', 
                fontweight='bold', fontsize=14, color='white')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

def plot_hit_rate_over_time(hit_log):
    if not hit_log or len(hit_log) == 0:
        fig, ax = plt.subplots(figsize=(8, 5))  # Reduced figure size
        ax.text(0.5, 0.5, 'No hit rate data available',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=14, style='italic')
        ax.set_title("Hit Rate Over Time", fontsize=16, fontweight='bold')
        plt.tight_layout()  # Important: removes extra whitespace
        return fig
    
    steps, rates = zip(*hit_log)
    
    # Convert rates to proper percentage format (0-100 instead of 0-1 if needed)
    # Check if rates are in decimal format (0-1) and convert to percentage
    max_rate = max(rates)
    if max_rate <= 1.0:
        rates = [r * 100 for r in rates]  # Convert to percentage
    
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced figure size for Streamlit
    
    ax.plot(steps, rates, color="#1f77b4", linewidth=2.5, label="Hit Rate", 
            marker='o', markersize=3)  # Smaller markers
    
    ax.fill_between(steps, rates, alpha=0.2, color="#1f77b4")  # Reduced alpha
    
    # Add moving average only if there are enough data points
    if len(steps) > 5:
        window_size = max(3, len(steps) // 10)
        rates_array = np.array(rates)
        moving_avg = np.convolve(rates_array, np.ones(window_size)/window_size, mode='valid')
        moving_steps = steps[window_size-1:]
        ax.plot(moving_steps, moving_avg, color="red", linewidth=2,
                linestyle='--', alpha=0.8, label=f"Moving Average ({window_size})")
    
    # Styling
    ax.set_xlabel("Operation Step", fontsize=11, fontweight='bold')
    ax.set_ylabel("Hit Rate (%)", fontsize=11, fontweight='bold')
    ax.set_title("Hit Rate Over Time", fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='-')
    
    # Set proper y-axis limits
    ax.set_ylim(0, max(100, max(rates) * 1.1))  # Ensure 0-100 range or slightly above max
    
    # Add average line
    avg_rate = np.mean(rates)
    ax.axhline(y=avg_rate, color='green', linestyle=':', alpha=0.8, linewidth=1.5)
    ax.text(max(steps)*0.02, avg_rate + max(rates)*0.02, f'Avg: {avg_rate:.1f}%',
            fontweight='bold', color='green', fontsize=9)
    
    # Legend
    ax.legend(loc='best', framealpha=0.9, fontsize=9)
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # CRITICAL: This removes extra whitespace
    plt.tight_layout()
    
    return fig

def plot_cache_state_evolution(cache_states, capacity):
    
    if not cache_states:
        return None
        
    fig, ax = plt.subplots(figsize=(12, 6))
    
    steps = range(len(cache_states))
    all_keys = set()
    for state in cache_states:
        all_keys.update(state)
    
    all_keys = sorted(list(all_keys))
    matrix = np.zeros((len(all_keys), len(cache_states)))
    
    for step, state in enumerate(cache_states):
        for key in state:
            if key in all_keys:
                key_idx = all_keys.index(key)
                matrix[key_idx, step] = 1
    
    im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', interpolation='nearest')
    
    ax.set_xlabel("Operation Step", fontsize=12, fontweight='bold')
    ax.set_ylabel("Cache Keys", fontsize=12, fontweight='bold')
    ax.set_title("Cache State Evolution", fontsize=16, fontweight='bold', pad=20)
    

    ax.set_yticks(range(len(all_keys)))
    ax.set_yticklabels([f'Key {key}' for key in all_keys])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('In Cache', rotation=270, labelpad=15, fontweight='bold')
    
    plt.tight_layout()
    return fig

def plot_strategy_switches(switch_log, operations):
    """
    Optional: Visualize when strategy switches occur
    """
    if not switch_log:
        return None
        
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot operation timeline
    ax.plot(range(len(operations)), [1]*len(operations), 'b-', alpha=0.3, linewidth=2)
    
    # Mark strategy switches
    for switch in switch_log:
        step = switch.get('step', 0)
        old_strategy = switch.get('from', 'Unknown')
        new_strategy = switch.get('to', 'Unknown')
        
        ax.axvline(x=step, color='red', linestyle='--', alpha=0.8, linewidth=2)
        ax.text(step, 1.1, f'{old_strategy}→{new_strategy}', 
                rotation=90, ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel("Operation Step", fontsize=12, fontweight='bold')
    ax.set_ylabel("Timeline", fontsize=12, fontweight='bold')
    ax.set_title("Cache Strategy Switches", fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0.5, 1.5)
    ax.set_yticks([])
    
    plt.tight_layout()
    return fig