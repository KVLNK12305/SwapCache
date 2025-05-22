from plotter import plot_cache_contents, plot_cache_metrics

# Doubly Linked List for LRU Cache
class DLL:
    class Node:
        def __init__(self, key, value, frequency=1):
            self.key = key
            self.value = value
            self.frequency = frequency
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at_head(self, key, value):
        new_node = self.Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node
        if not self.tail:
            self.tail = new_node
        self.size += 1
        return new_node

    def move_to_head(self, node):
        if node == self.head:
            return
        if node == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        node.prev = None
        node.next = self.head
        self.head.prev = node
        self.head = node

    def remove_tail(self):
        if not self.tail:
            return None
        old_tail = self.tail
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return old_tail.key, old_tail.value

# AVL Tree for LFU Cache
class AVLTree_LinkedList:
    class AVLNode:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.frequency = 1
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return self.AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            node.frequency += 1
            return node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return self._balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.frequency = temp.frequency
            node.right = self._delete(node.right, temp.key)
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return self._balance(node)

    def get_height(self, node):
        return node.height if node else 0

    def _balance(self, node):
        balance_factor = self.get_height(node.left) - self.get_height(node.right)
        if balance_factor > 1:
            if self.get_height(node.left.left) >= self.get_height(node.left.right):
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
        if balance_factor < -1:
            if self.get_height(node.right.right) >= self.get_height(node.right.left):
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node)
                return self._left_rotate(node)
        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def _get_min_value_node(self, node):
        if node is None:
            return None
        current = node
        while current.left:
            current = current.left
        return current

# Performance Metrics for Cache Operations
class CachePerformanceMetrics:
    def __init__(self):
        self.hit_count = 0
        self.miss_count = 0
        self.eviction_count = 0
        self.total_accesses = 0

    def record_access(self, hit, evicted=False):
        self.total_accesses += 1
        if hit:
            self.hit_count += 1
        else:
            self.miss_count += 1
        if evicted:
            self.eviction_count += 1

    def get_metrics(self):
        if self.total_accesses == 0:
            return {"hit_ratio": 0, "miss_ratio": 0, "eviction_rate": 0}
        return {
            "hit_ratio": self.hit_count / self.total_accesses,
            "miss_ratio": self.miss_count / self.total_accesses,
            "eviction_rate": self.eviction_count / self.total_accesses,
        }

# Main Dynamic Cache
class DynamicCache:
    def __init__(self, capacity, eviction_policy='LRU'):
        self.capacity = capacity
        self.eviction_policy = eviction_policy
        self.dll = DLL()                    # Instance of DLL for LRU
        self.lfu_tree = AVLTree_LinkedList()  # AVL Tree for LFU
        self.node_map = {}                  # Key-to-node map for fast lookup
        self.memory = {}                    # Write-through memory storage
        self.metrics = CachePerformanceMetrics()  # Cache metrics tracking

    def get(self, key):
        if key not in self.node_map:
            self.metrics.record_access(hit=False)
            return -1
        node = self.node_map[key]
        if self.eviction_policy == 'LRU':
            self.dll.move_to_head(node)
        self.metrics.record_access(hit=True)
        return node.value

    def put(self, key, value):
        evicted = False
        if key in self.node_map:
            node = self.node_map[key]
            node.value = value
            if self.eviction_policy == 'LRU':
                self.dll.move_to_head(node)
        else:
            if len(self.node_map) >= self.capacity:
                if self.eviction_policy == 'LRU':
                    evict_key, evict_value = self.dll.remove_tail()
                    del self.node_map[evict_key]
                    self.memory[evict_key] = evict_value
                    evicted = True
                elif self.eviction_policy == 'LFU':
                    min_node = self.lfu_tree._get_min_value_node(self.lfu_tree.root)
                    if min_node:
                        self.lfu_tree.delete(min_node.key)
                        del self.node_map[min_node.key]
                        self.memory[min_node.key] = min_node.value
                        evicted = True
            new_node = self.dll.insert_at_head(key, value)
            self.node_map[key] = new_node
        self.metrics.record_access(hit=key in self.node_map, evicted=evicted)

    def flush_to_memory(self):
        for key, node in self.node_map.items():
            self.memory[key] = node.value
        print("Cache flushed to memory.")

    def display_cache(self):
        current = self.dll.head
        while current:
            print(f"Key: {current.key}, Value: {current.value}")
            current = current.next
        print("End of Cache\n")

# Visualizer for Cache State and Metrics
class CacheVisualizer:
    @staticmethod
    def display_cache_state(cache, message="Cache State:"):
        print(f"\n{message}")
        cache.display_cache()
        metrics = cache.metrics.get_metrics()
        print("Metrics:")
        print(f"Hit Ratio: {metrics['hit_ratio']:.2f}")
        print(f"Miss Ratio: {metrics['miss_ratio']:.2f}")
        print(f"Eviction Rate: {metrics['eviction_rate']:.2f}")
        print("-" * 40)

# Menu for interacting with the cache
def menu():
    print("\nCache Menu:")
    print("1. Write to Cache")
    print("2. Access Cache")
    print("3. Display Cache State")
    print("4. Flush Cache to Memory")
    print("5. Exit")

# Main program function
def main():
    print("Welcome to the Cache System!")
    capacity = int(input("Enter cache capacity: "))
    eviction_policy = input("Choose eviction policy (LRU / LFU): ").strip().upper()
    cache = DynamicCache(capacity, eviction_policy)
    visualizer = CacheVisualizer()
    
    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':  # Write to Cache
            key = int(input("Enter key: "))
            value = input("Enter value: ")
            cache.put(key, value)
            print(f"Added ({key}, {value}) to cache.")
        
        elif choice == '2':  # Access Cache
            key = int(input("Enter key to access: "))
            result = cache.get(key)
            if result == -1:
                print(f"Key {key} not found in cache.")
            else:
                print(f"Accessed Key {key}: Value = {result}")
        
        elif choice == '3':  # Display Cache State
            visualizer.display_cache_state(cache)
            visualizer.display_cache_state(cache)
            plot_cache_contents(cache)
            plot_cache_metrics(cache.metrics.get_metrics())
        
        elif choice == '4':  # Flush Cache to Memory
            cache.flush_to_memory()
            print("Cache flushed to memory. Current Memory State:")
            print(cache.memory)
        
        elif choice == '5':  # Exit
            print("Exiting the Cache System. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
    


# Run the program
if __name__ == "__main__":
    main()
