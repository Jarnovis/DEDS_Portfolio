class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    

class LinkedList:
    def __init__(self):
        self.head = None
    
    def add(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

        
    def addFirst(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def addFirstNewList(self, data):
        list = LinkedList()
        list.add(data)
        
        current = self.head
        while current:
            list.add(current.data)
            current = current.next
        
        return list
    
    def remove(self, value):
        new_list = LinkedList()

        current = self.head
        while current:
            if current.data != value:
                new_list.add(current.data)
            current = current.next

        return new_list

        
    def get(self, value):
        current = self.head
        
        while current:
            if current.data == value:
                return current.data

    def length(self):
        current = self.head
        length = 0
        
        while current:
            length += 1
            current = current.next
        
        return length
    
    def order(self):
        new_list = LinkedList()
        current_list = self

        while current_list.head != None:
            new_list.add(current_list.smallest())

            current_list = current_list.remove(current_list.smallest())

        return new_list
    
    def smallest(self):
        current = self.head
        smallest = None
        
        while current:
            if smallest == None:
                smallest = current.data
            else:
                if current.data < smallest:
                    smallest = current.data
            
            current = current.next
        
        return smallest   

    
    def toString(self):
        current = self.head
        string = ""
        
        while current:
            string += f"{current.data} "
            current = current.next
        
        print(string)
        
        return string
    
    def unique(self, node=None, previous=None):
        if node is None and previous is None:
            if self.head is None:
                return 0
            return 1 + self.unique(self.head.next, self.head.data)

        if node is None:
            return 0

        if node.data != previous:
            return 1 + self.unique(node.next, node.data)

        return self.unique(node.next, previous)
    
    def subList(self, start, end):
        new_list = LinkedList()
        current = self.head
        index = 0

        while current and index < end:
            if index >= start:
                new_list.add(current.data)
            current = current.next
            index += 1

        return new_list
    
    def merge(self, other):
        new_list = LinkedList()
        
        this = self.head
        other = other.head

        while this and other:
            if this.data <= other.data:
                new_list.add(this.data)
                this = this.next
            else:
                new_list.add(other.data)
                other = other.next

        while this:
            new_list.add(this.data)
            this = this.next

        while other:
            new_list.add(other.data)
            other = other.next

        return new_list
    
    def sortMerge(self):
        if self.head is None or self.head.next is None:
            return self  

        length = self.length()
        mid = length // 2

        left = self.subList(0, mid)
        right = self.subList(mid, length)

        sorted_left = left.sortMerge()
        sorted_right = right.sortMerge()

        return sorted_left.merge(sorted_right)



class LinkedListPopulated(LinkedList):
    def __init__(self, values = None):
        super().__init__()
        
        if values:
            for value in values:
                self.add(value)
        
    def is_empty(self):
        return self.head == None
    
    def display(self):
        print(self.toString(self.head))

class LinkedListEmpty(LinkedList):
    def __init__(self):
        super().__init__()
    
    def is_empty():
        return True

    def display(self):
        print("Linked List is leeg!!!!!!!")