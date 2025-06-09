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
    fig, ax = plt.subplots()
    ax.bar(["Hits", "Misses"], [hits, misses], color=["green", "red"])
    ax.set_title("Hit vs Miss Ratio")
    ax.set_ylabel("Count")
    plt.show()


def plot_hit_rate_over_time(hit_log):
    steps, rates = zip(*hit_log)
    fig, ax = plt.subplots()
    ax.plot(steps, rates, color="blue", label="Hit Rate")
    ax.set_xlabel("Step")
    ax.set_ylabel("Hit Rate")
    ax.set_title("Hit Rate Over Time")
    ax.grid(True)
    ax.legend()
    plt.show()