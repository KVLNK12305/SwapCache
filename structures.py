import time

class Node:
    def __init__(self, key, data):
        self.key = key
        self.val = data
        self.prev = None
        self.next = None
        self.freq = 1

class DLL:
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def size_dll(self):
        return self.length

    def insert_first(self, node):
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node
        self.length += 1

    def insert_last(self, node):
        node.prev = self.tail
        node.next = None
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = self.tail = node
        self.length += 1

    def delete_first(self):
        if self.length == 0:
            raise Exception("Cannot perform operation on an empty list")
        node = self.head
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.length -= 1
        return node

    def delete_last(self):
        if self.length == 0:
            raise Exception("Cannot perform operation on an empty list")
        node = self.tail
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.length -= 1
        return node

    def show_values(self):
        curr = self.head
        while curr:
            print(f"{curr.key}:{curr.val}")
            curr = curr.next

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.length -= 1

    def move_to_front(self, node):
        self.remove_node(node)
        self.insert_first(node)

class LRU:
    def __init__(self, C):
        self.capacity = C
        self.map = {}
        self.dll = DLL()

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            self.dll.move_to_front(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.val = value
            self.dll.move_to_front(node)
        else:
            if len(self.map) >= self.capacity:
                lru_node = self.dll.delete_last()
                if lru_node:
                    del self.map[lru_node.key]
            new_node = Node(key, value)
            self.dll.insert_first(new_node)
            self.map[key] = new_node

class LFU:
    def __init__(self, capacity):  # Fixed parameter name
        self.capacity = capacity   # Fixed attribute name
        self.map = {}
        self.freq_map = {}
        self.min_freq = 0

    def get_freq_dll(self, freq):  # Fixed method name (was get_node)
        if freq not in self.freq_map:
            self.freq_map[freq] = DLL()
        return self.freq_map[freq]
    
    def update_freq(self, node):
        old_f = node.freq
        new_f = old_f + 1

        old_dll = self.freq_map[old_f]  # Fixed variable name
        old_dll.remove_node(node)

        if old_f == self.min_freq and old_dll.length == 0:
            self.min_freq += 1

        node.freq = new_f
        new_dll = self.get_freq_dll(new_f)  # Fixed method call
        new_dll.insert_first(node)

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self.update_freq(node)
        return node.val
    
    def put(self, key, value):  # Added missing put method
        if self.capacity <= 0:
            return
        
        if key in self.map:
            # Update existing key
            node = self.map[key]
            node.val = value
            self.update_freq(node)
        else:
            # Add new key
            if len(self.map) >= self.capacity:
                # Remove least frequently used item
                if self.min_freq in self.freq_map:
                    min_freq_dll = self.freq_map[self.min_freq]
                    if min_freq_dll.length > 0:
                        lfu_node = min_freq_dll.delete_last()
                        if lfu_node:
                            del self.map[lfu_node.key]
            
            # Create new node and add it
            new_node = Node(key, value)
            new_node.freq = 1
            self.map[key] = new_node
            freq_1_dll = self.get_freq_dll(1)
            freq_1_dll.insert_first(new_node)
            self.min_freq = 1

class Stats:
    def __init__(self, strategy):
        self.cache = strategy
        self.hits = 0
        self.misses = 0

    def get(self, key):
        start = time.time()
        value = self.cache.get(key)
        end = time.time()
        if value != -1:
            self.hits += 1
        else:
            self.misses += 1
        print(f"GET {key} took {end - start:.6f}s")
        return value

    def put(self, key, value):
        start = time.time()
        self.cache.put(key, value)
        end = time.time()
        print(f"PUT {key} took {end - start:.6f}s")

    def stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        miss_rate = self.misses / total if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'miss_rate': miss_rate
        }

class DynamicCache:  # Created proper class structure
    def __init__(self, capacity):
        self.capacity = capacity
        self.lru_cache = LRU(capacity)
        self.lfu_cache = LFU(capacity)
        self.current_strategy = "LRU"
        self.lru_stats = Stats(self.lru_cache)
        self.lfu_stats = Stats(self.lfu_cache)
        self.switch_threshold = 10
        self.operation_count = 0

    def dynamic_switcher(self):  # Fixed method name and indentation
        if self.operation_count < self.switch_threshold:
            return
        
        lru_performance = self.lru_stats.stats()
        lfu_performance = self.lfu_stats.stats()
        
        # Switch to the strategy with better hit rate
        if lfu_performance['hit_rate'] > lru_performance['hit_rate']:
            if self.current_strategy != "LFU":
                print(f"Switching to LFU (hit rate: {lfu_performance['hit_rate']:.2f})")
                self.current_strategy = "LFU"
        else:
            if self.current_strategy != "LRU":
                print(f"Switching to LRU (hit rate: {lru_performance['hit_rate']:.2f})")
                self.current_strategy = "LRU"
    
    def get(self, key):  # Fixed indentation and method calls
        self.operation_count += 1
        
        # Execute on both caches for comparison
        lru_result = self.lru_stats.get(key)
        lfu_result = self.lfu_stats.get(key)
        
        # Return result from current strategy
        result = lru_result if self.current_strategy == "LRU" else lfu_result
        
        # Consider switching strategy
        if self.operation_count % self.switch_threshold == 0:
            self.dynamic_switcher()  # Fixed method call
        
        return result

    def put(self, key, value):  # Fixed indentation and method calls
        self.operation_count += 1
        
        # Execute on both caches
        self.lru_stats.put(key, value)
        self.lfu_stats.put(key, value)
        
        # Consider switching strategy
        if self.operation_count % self.switch_threshold == 0:
            self.dynamic_switcher()  # Fixed method call

