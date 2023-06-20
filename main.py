import math

class Node:
    def __init__(self, key):
        self.key = key                      # value of the mode
        self.parent = None                  # parent pointer
        self.child = None                   # child pointer
        self.left = None                    # pointer to left sibiling
        self.right = None                   # ponter to right sibiling
        self.degree = 0                     # degree of node
        self.mark = False                   # mark of node

class FibHeap:
    def __init__(self):
        self.min = None                     # minimum of heap
        self.n = 0                          # number of nodes

    def insert_node(self, x):               # insert node
        if self.min == None:
            x.left = x
            x.right = x
            self.min = x
        else:
            x.right = self.min
            x.left = self.min.left
            self.min.left.right = x
            self.min.left = x
            if x.key < self.min.key:
                self.min = x
        self.n = self.n + 1

    def insert_node_in_root(self, x):       # insert node in root
        if self.min == None:
            x.left = x
            x.right = x
            self.min = x
        else:
            x.right = self.min
            x.left = self.min.left
            self.min.left.right = x
            self.min.left = x
            if x.key < self.min.key:
                self.min = x

    def union(self, h1, h2):                # merge two f_heaps
        h = FibHeap()
        h.min = h1.min
        
        if (h1.min != None and h1.min != None):
            h1_min_right = h1.min.right
            h2_min_left = h2.min.left
            h1.min.right = h2.min               #join two mins of each heap
            h2.min.left = h1.min

            h1_min_right.left = h2_min_left     # join right sibiling of h1 and left sibiling of h2
            h2_min_left.right = h1_min_right

        if h1.min == None or (h2.min != None and h2.min.key < h1.min.key):
            h.min = h2.min
        h.n = h1.n + h2.n
        return h

    def extract_min(self):
        z = self.min                        # take the min
        if z != None:                       
            child = z.child                 # take the first child
            first_child = child
            if child != None:
                temp = child
                while child != None:        # put every child to list of roots
                    temp = child.right
                    child.parent = None
                    self.insert_node_in_root(child)
                    child = temp
                    if child == first_child:
                        break

            z.left.right = z.right          # delete minimum from list of roots
            z.right.left = z.left
            z.child = None

            if z == z.right:                # if z has no right sibiling, he is the only node in list of roots
                self.min = None
            else:                           # set zs right child to min
                self.min = z.right          # call consolidate to fix the heap
                self.consolidate()
            self.n = self.n - 1             # number of nodes is n - 1
        return z

    def consolidate(self):
        phi = (1 + math.sqrt(5)) / 2
        d_n = int(math.log(self.n) / math.log(phi));
        a = [None] * (d_n + 1)             # alocation of array A[n]

        w = self.min                        
        if w != None:
            k = w
            while w != None:
                x = w
                x_right = x.right
                d = x.degree
                while a[d] != None:
                    y = a[d]
                    if x.key > y.key:
                        temp = x
                        x = y
                        y = temp

                    if (y == k):
                        k = k.right

                    if (y == x_right):
                        x_right = x_right.right

                    self.link(y, x)         #linking  of two root nodes
                    a[d] = None
                    d = d + 1
                a[d] = x
                w = x_right
                if w == k:
                    break
                # second part
            self.min = None
            for i in range (0, d_n):
                if (a[i] != None):
                    self.insert_node_in_root(a[i])
        return 0

    def link(self, y, x):
        y.left.right = y.right              # remove y from list of root nodes
        y.right.left = y.left

        child = x.child
        if child == None:                   # if x doesnt have children
            y.right = y
            y.left = y
        else:
            y.right = child
            y.left = child.left
            child.left.right = y 
            child.left = y 

        x.child = y                         # make y child of x
        y.parent = x                        # make x parent of y
        x.degree= x.degree + 1              # increase the degree of x
        y.mark = False                      # unmark y

        return 0

    def display(self):
        self.display_node(self.min);

    def display_node(self, x):
        print("(", end="")
        if(x == None):
            print(")", end="")
            return
        else:
            t = x;
            while(True):
                print(t.key, t.mark, end="");
                k = t.child;
                self.display_node(k);
                print("-->", end="");
                t = t.right;
                if (t == x):
                    break
            print(")", end="")

    def decrease_key(self, x: Node, k):
        if k > x.key:                                       # key is greater than current
            print("New key is greater than current key")
            return
        x.key = k                                           # set the key
        y = x.parent                                        # get the parent
        if y != None and x.key < y.key:                     # if current value of x is smaller than its parent fix it
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min.key:                            # check minimum
            self.min = x

    def cut(self, x, y):
        if x.right == x and x.left == x:            # if x is only child of y
            y.child = None 
        else:
            if y.child == x:                        # if child pointer is on x we will lose pointer to children
                y.child = x.right
            x.left.right = x.right                  # remove x from child list
            x.right.left = x.left
            
        y.degree = y.degree - 1                     # decrement degree of y 
        x.right = None
        x.left = None
        x.parent = None
        x.mark = False
        self.insert_node_in_root(x)                # insert x in root list

    def cascading_cut(self, y):                    # check parent of x 
        z = y.parent
        if z != None:
            if y.mark == False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def delete(self, x):
        self.decrease_key(x, -1000)
        self.extract_min()

# tests
def test_insert_empty_heap():
    print("\n-Test insert in empty heap-\n")
    h1 = FibHeap()
    x = Node(3)
    h1.insert_node(x)
    print("Heap after inserting:")
    h1.display()
    print("\nAttributes of our node are: parent: ", h1.min.parent, ", left sibiling: ", h1.min.left.key, ", right sibiling: ", h1.min.right.key, ", child: ", h1.min.child, ", mark: ", h1.min.mark);

def test_insert_two_nodes():
    print("\n-Test insert two nodes-\n");
    h1 = FibHeap()
    print("Heap h1 before insert: ", end="");
    h1.display();

    print("\nInserting elements: 17, 23, 24");
    keys = [17, 23, 24]
    for key in keys:
        h1.insert_node(Node(key));

    print("Heap h1 after insert: ", end="");
    h1.display();

    if(h1.n == 3 and h1.min.key == 17 and h1.min.left.key == 24):
        print("\nPassed!");
    else:
        print("\nFailed");

def test_insert():
    print("\n-Test insert-\n");
    h1 = FibHeap()
    print("Heap h1 before insert: ", end="");
    h1.display();

    print("\nInserting elements: 12, 11, 10, 9, 8, 7, 6, 5");
    keys = [12, 11, 10, 9, 8, 7, 6, 5]
    for key in keys:
        h1.insert_node(Node(key));

    print("Heap h1 after insert: ", end="");
    h1.display();

    if(h1.n == 8 and h1.min.key == 5):
        print("\nPassed!");
    else:
        print("\nFailed");


def test_union_empty_heap():
    print("\n- Test union -\n");
    h1 = FibHeap()
    print("Heap h1 before union:", "( n:", h1.n, ") ", end="");
    h1.display();

    h2 = FibHeap()
    print("\nHeap h2 before union:", "( n:", h2.n, ") ", end="");
    h2.display();

    h = FibHeap()
    h = FibHeap.union(h,h1,h2)
    print("\nNew heap: ", "(n: ", h.n, ")");
    h.display();
    if(h.n == h1.n + h2.n):
        print("\nPassed!");
    else:
        print("\nFailed");

def test_union():
    print("\n- Test union -\n");

    h1 = FibHeap()
    keys_h1 = [17, 24, 23]
    for key in keys_h1:
        h1.insert_node(Node(key))

    print("Heap h1 before union:", "( n:", h1.n, ") ", end="")
    h1.display();

    h2 = FibHeap()
    keys_h2 = [21, 3, 7]
    for key in keys_h2:
        h2.insert_node(Node(key))

    print("\nHeap h2 before union:", "( n:", h2.n, ") ", end="")
    h2.display()

    h = FibHeap()
    h = FibHeap.union(h,h1,h2)
    print("\nNew heap: ", "(n: ", h.n, ")")
    h.display();
    if(h.n == h1.n + h2.n and h.min.key == 3): 
        print("\nPassed!");
    else:
        print("\nFailed");



def test_extract_min_1():
    print("\n- Test extract min -\n");

    h1 = FibHeap()
    keys_h1 = [7, 3, 17, 23]
    for key in keys_h1:
        h1.insert_node(Node(key))

    print("Heap h1 before extract:", "( n:", h1.n, ") ")
    h1.display()

    h1.extract_min()
    print("\n\nHeap h1 after extract:", "( n:", h1.n, ") ")
    h1.display()
    

def test_extract_min_2():
    print("\n\n- Test extract min -\n");

    h1 = FibHeap()
    keys_h1 = [7, 3, 17, 23, 24, 13]
    for key in keys_h1:
        h1.insert_node(Node(key))

    print("Heap h1 before first extract:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.extract_min()
    print("\n\nHeap h1 after extract:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()


    print("\n\nHeap h1 before second extract:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.extract_min()
    print("\n\nHeap h1 after extract:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

def test_decrease_key1():
    print("\n\n- Test decrease key(parent is unmarked) -\n");

    h1 = FibHeap()
    keys_h1 = [7, 3, 17, 23, 24, 13]
    for key in keys_h1:
        h1.insert_node(Node(key))
    h1.extract_min()

    print("\n\nHeap h1 before decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    # 7 - 13
    # |
    # 23 - 17
    # |
    # 24

    h1.decrease_key(h1.min.child.child, 5)
    print("\n\nHeap h1 after decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    if(h1.n == 5 and h1.min.key == 5): 
        print("\nPassed!");
    else:
        print("\nFailed");

def test_decrease_key2():
    print("\n\n- Test decrease key(no mark is changed) -\n");

    h1 = FibHeap()
    keys_h1 = [7, 3, 17, 13, 5, 6, 10]
    for key in keys_h1:
        h1.insert_node(Node(key))
    h1.extract_min()

    # 5  ------  6
    # |          |
    # 7 - 13    10
    # |
    # 17

    print("\n\nHeap h1 before decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.decrease_key(h1.min.child.right, 3)
    print("\n\nHeap h1 after decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    if(h1.n == 6 and h1.min.key == 3): 
        print("\nPassed!");
    else:
        print("\nFailed");

def test_decrease_key3():
    print("\n\n- Test decrease key(parent is marked) -\n");

    h1 = FibHeap()
    keys_h1 = [7, 3, 17, 13, 5, 6, 10, 26, 24, 30, 16]
    for key in keys_h1:
        h1.insert_node(Node(key))
    h1.extract_min()

    print("\n\nHeap h1 before decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.decrease_key(h1.min.child.child.child, 3)
    print("\n\nHeap h1 after decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.decrease_key(h1.min.right.child.child, 2)
    print("\n\nHeap h1 after decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.decrease_key(h1.min.right.right.child.child, 1)
    print("\n\nHeap h1 after decrease key:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()


    if(h1.n == 10 and h1.min.key == 1): 
        print("\nPassed!");
    else:
        print("\nFailed");

def test_delete1():
    print("\n\n- Test delete 1 -\n");

    h1 = FibHeap()
    keys_h1 = [7, 3, 17, 13, 5, 6, 10]
    for key in keys_h1:
        h1.insert_node(Node(key))
    h1.extract_min()
    h1.extract_min();
    
    print("Heap h1 before delete:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    h1.delete(h1.min.child)
    print("\n\nHeap h1 after delete:", "( n:", h1.n, "min: ", h1.min.key, ") ")
    h1.display()

    if(h1.n == 4 and h1.min.key == 6): 
        print("\nPassed!");
    else:
        print("\nFailed");


if __name__ == "__main__":

    # insert
    test_insert_empty_heap()
    test_insert_two_nodes()
    test_insert()
    
    # union
    test_union_empty_heap()
    test_union()

    # extract min
    test_extract_min_1()
    test_extract_min_2()

    # decrease
    test_decrease_key1()
    test_decrease_key2()
    test_decrease_key3()

    # delete
    test_delete1()

