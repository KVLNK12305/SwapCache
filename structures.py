class Node:
    def __init__(self, key, data):
        self.key = key
        self.val = data
        self.prev = None
        self.next = None

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
