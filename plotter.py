import matplotlib.pyplot as plt

def plot_cache_contents(cache):
    """Plots current cache contents as a bar chart."""
    keys = []
    values = []

    current = cache.dll.head
    while current:
        keys.append(str(current.key))
        values.append(current.value)
        current = current.next

    if not keys:
        print("Cache is empty — nothing to plot.")
        return

    plt.figure(figsize=(8, 4))
    plt.bar(keys, range(len(values)), tick_label=values, color='skyblue')
    plt.title("Cache Contents (Key:Value)")
    plt.xlabel("Keys")
    plt.ylabel("Order (Head → Tail)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_cache_metrics(metrics: dict):
    """Plots cache performance metrics as a pie chart."""
    labels = ['Hit', 'Miss', 'Eviction']
    sizes = [
        metrics.get('hit_ratio', 0),
        metrics.get('miss_ratio', 0),
        metrics.get('eviction_rate', 0)
    ]

    if sum(sizes) == 0:
        print("No cache accesses yet — metrics not available.")
        return

    # Normalize to 100% if needed
    total = sum(sizes)
    if total != 1.0:
        sizes = [s / total for s in sizes]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Cache Performance Metrics")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
