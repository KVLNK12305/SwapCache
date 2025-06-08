class Node:
    def __init__(self,data,key,frequency=1):
        self.val = data
        # for the linked list
        self.prev = None
        self.next = None
        # for mapping purpose
        self.key = key
        self.freq = frequency
class DLL:
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def size_dll(self):
        return self.length
    
    def insert_first(self,data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head.prev = new_node
        self.head = new_node
        self.length+=1

    def insert_last(self,data):
        new_node = Node(data)
        if self.tail:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        else:
            self.head = new_node
        self.length+=1

        self.length+=1

    def delete_first(self):
        if self.length == 0:
            raise Exception("Cannot perform operation on an empty list")
        self.head = self.head.next  
        if self.head:
            self.head.prev = None  
        self.length -= 1

    def delete_last(self):
        if self.length == 0:
            raise Exception("Cannot perform operation on an empty list")
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.length -= 1
