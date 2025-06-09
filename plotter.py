import matplotlib.pyplot as plt
import numpy as np


def plot_hit_miss_ratio(hits, misses):
    fig, ax = plt.subplots()
    ax.bar(["Hits", "Misses"], [hits, misses], color=["green", "red"])
    ax.set_title("Hit vs Miss Ratio")
    ax.set_ylabel("Count")
    return fig


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
    return fig


def plot_hit_rate_over_time(hit_log):
    steps, rates = zip(*hit_log)
    fig, ax = plt.subplots()
    ax.plot(steps, rates, color="blue", label="Hit Rate")
    ax.set_xlabel("Step")
    ax.set_ylabel("Hit Rate")
    ax.set_title("Hit Rate Over Time")
    ax.grid(True)
    ax.legend()
    return fig