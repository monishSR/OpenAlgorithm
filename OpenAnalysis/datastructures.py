import networkx as nx
import matplotlib.pyplot as plt
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

'''
Usage Instructions:

>sudo apt install python-gi-cairo
>put sd.glade in same working directory
>in main(),pass any instance of DataStructureBase

'''


class DataStructureBase:
    """
    Base class for implementing Data Structures
    """
    def __init__(self, name: str):
        """
        Constructor
        :param name: Name of Data Structure. Drawing Layout is determined by the name itself
        If the name contains 'tree', then layout is tree layout, else Graph
        """
        self.name = name
        self.is_tree = "TREE" in name.upper() or "HEAP" in name.upper()
        self.layout = self.__binary_tree_layout if self.is_tree else self.__hierarchy_pos
        self.graph = nx.Graph()
        # Layout to draw BFS tree

    def insert(self, item):
        """
        Insert item to Data Structure
        While inserting, add a edge from parent to child in self.graph
        :param item: item to be added
        """
        pass

    def delete(self, item):
        """
        Delete the item from Data Structure
        While removing, delete item from self.graph and modify the edges if necessary
        :param item: item to be deleted
        """
        pass

    def find(self, item):
        """
        Finds the item in Data Structure
        :param item: item to be searched
        :return: True if item in self else False
        also can implement __contains__(self,item)
        """
        pass

    def __contains__(self, item):
        return self.find(item)

    def draw(self):
        """
        ----old-----
        Do a BFS and draw the Data Structure
        Data Structure is essentially graph like and can be represented by Mathematical Relation
        For example Graph G : 1--2--3 can be represented as R_G = {(1,2),(2,3)}
        In python they can be represented as Set, whose elements are tuples
        At last, set can be transformed into list, and a graph can be created
        example:
            >>> s = {(1,2),(2,3),(1,3)}
            >>> r = list(s)
            >>> G = nx.Graph(r)

        Such a set can be crated during operations or a BFS on Data Structure by updating self
        -----new-----
        plots self.graph, saves the image and returns the path to saved image
        """
        Tree = self.graph
        if Tree.nodes():
            pos = self.layout(Tree, self.root)
            nx.draw(Tree, pos, with_labels=True)
            plt.savefig("/tmp/algo/f.png")
        return "/tmp/algo/f.png"

    @staticmethod
    def __binary_tree_layout(G, root, width=1., vert_gap=0.2, vert_loc=0., xcenter=0.5,
                             pos=None, parent=None):
        '''If there is a cycle that is reachable from root, then this will see infinite recursion.
           G: the graph
           root: the root node of current branch
           width: horizontal space allocated for this branch - avoids overlap with other branches
           vert_gap: gap between levels of hierarchy
           vert_loc: vertical location of root
           xcenter: horizontal location of root
           pos: a dict saying where all nodes go if they have been assigned
           parent: parent of this branch.
           each node has an attribute "left: or "right"'''
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        neighbors = G.neighbors(root)
        if parent is not None:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / 2.
            leftx = xcenter - dx / 2
            rightx = xcenter + dx / 2
            for neighbor in neighbors:
                if G.node[neighbor]['child_status'] == 'left':
                    pos = DataStructureBase.__binary_tree_layout(G, neighbor, width=dx, vert_gap=vert_gap,
                                                                 vert_loc=vert_loc - vert_gap, xcenter=leftx, pos=pos,
                                                                 parent=root)
                elif G.node[neighbor]['child_status'] == 'right':
                    pos = DataStructureBase.__binary_tree_layout(G, neighbor, width=dx, vert_gap=vert_gap,
                                                                 vert_loc=vert_loc - vert_gap, xcenter=rightx, pos=pos,
                                                                 parent=root)
        return pos

    @staticmethod
    def __hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        '''If there is a cycle that is reachable from root, then result will not be a hierarchy.

           G: the graph
           root: the root node of current branch
           width: horizontal space allocated for this branch - avoids overlap with other branches
           vert_gap: gap between levels of hierarchy
           vert_loc: vertical location of root
           xcenter: horizontal location of root
        '''

        def h_recur(G, root, width=1., vert_gap=0.2, vert_loc=0., xcenter=0.5,
                    pos=None, parent=None, parsed=[]):
            if (root not in parsed):
                parsed.append(root)
                if pos == None:
                    pos = {root: (xcenter, vert_loc)}
                else:
                    pos[root] = (xcenter, vert_loc)
                neighbors = G.neighbors(root)
                if parent != None:
                    neighbors.remove(parent)
                if len(neighbors) != 0:
                    dx = width / len(neighbors)
                    nextx = xcenter - width / 2 - dx / 2
                    for neighbor in neighbors:
                        nextx += dx
                        pos = h_recur(G, neighbor, width=dx, vert_gap=vert_gap,
                                      vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                      parent=root, parsed=parsed)
            return pos

        return h_recur(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5)


class DataStructureVisualization:
    """
    Class for visualizing data structures in GUI
    Using GTK+ 3
    """
    def __init__(self, ds: DataStructureBase):
        """
        Constructor
        :param ds: Any data structure, which is an instance of DataStructureBase
        """
        self.ds = ds
        self.builder = gtk.Builder()
        self.builder.add_from_file("sd.glade")
        self.builder.connect_signals(self)
        self.map = [self.ds.insert,self.ds.delete,self.ds.find]

    def run(self):
        self.builder.get_object("stage").show_all()
        self.builder.get_object("name").set_text(self.ds.name)
        gtk.main()

    def on_stage_destroy(self, x):
        gtk.main_quit()

    def action_clicked_cb(self,button):
        try:
            ele = int(self.builder.get_object("item").get_text())
            choice = int(self.builder.get_object("operation").get_active())
            state = self.builder.get_object("state")
            self.map[choice](ele)
            state.set_from_file(self.ds.draw())
        except Exception as e:
            raise


class BinarySearchTree(DataStructureBase):
    """
    Sample implementation of Data Structure, incomplete
    """
    class Node:
        def __init__(self, data):
            self.left = None
            self.right = None
            self.data = data

        def __str__(self):
            return str(self.data)

    def __init__(self):
        DataStructureBase.__init__(self, "Binary Search Tree")
        self.root = None
        self.count = 0

    def insert(self, item):
        newNode = BinarySearchTree.Node(item)
        insNode = self.root
        parent = None
        while insNode is not None:
            parent = insNode
            if insNode.data > newNode.data:
                insNode = insNode.left
            else:
                insNode = insNode.right
        if parent is None:
            self.root = newNode
        else:
            self.graph.add_edge(parent, newNode)
            if parent.data > newNode.data:
                parent.left = newNode
                self.graph.node[newNode]['child_status'] = "left"
            else:
                parent.right = newNode
                self.graph.node[newNode]['child_status'] = "right"
        self.count += 1

    def find(self, item):
        node = self.root
        while node is not None:
            if item < node:
                node = node.left
            elif item > node:
                node = node.right
            else:
                return True
        return False

    def delete(self, item):
        if item not in self:
            raise ValueError("{0} not in Tree".format(item))
        pass


class BinaryHeap(DataStructureBase):
    """
    Sample implementation of Data Structure, Incomplete
    Do corrections
    """
    def __init__(self, a=[], typ=True):
        DataStructureBase.__init__(self, "Binary Heap")
        self.elements = [0 for k in range(len(a) + 1)]
        self.typ = typ
        self.count = 0
        for j in a:
            self.insert(j)

    def insert(self, element):
        if element in self.elements:
            raise Exception("not unique")
        self.count += 1
        self.elements.extend([0])
        insert_position = self.count
        while insert_position > 1 and self.compare_to(self.elements[int(insert_position / 2)], element):
            self.elements[insert_position] = self.elements[int(insert_position / 2)]
            insert_position = int(insert_position / 2)
        self.elements[insert_position] = element

    def delete(self, item):
        root = self.elements[1]
        item = self.elements[self.count]
        self.count -= 1
        self.elements[1] = item
        insert_position = 1
        is_heap = False
        while insert_position <= int(self.count / 2) and not is_heap:
            extreme_c_pos = 2 * insert_position
            extreme_c_pos = extreme_c_pos if self.compare_to(self.elements[extreme_c_pos + 1],
                                                             self.elements[extreme_c_pos]) \
                else extreme_c_pos + 1
            if self.compare_to(self.elements[extreme_c_pos], item):
                is_heap = True
            else:
                self.elements[insert_position] = self.elements[extreme_c_pos]
                insert_position = extreme_c_pos
        self.elements[insert_position] = item
        return root

    def compare_to(self, p, q):
        if self.typ:
            return p > q
        return p < q

    def draw(self):
        """Not necessary now, build tree during insertion"""
        current_position = 1
        H = nx.Graph()
        plt.clf()
        while current_position <= int(self.count / 2):
            H.add_edge(self.elements[current_position], self.elements[2 * current_position])
            H.node[self.elements[2 * current_position]]['child_status'] = 'left'
            if 2 * current_position + 1 <= self.count:
                H.add_edge(self.elements[current_position], self.elements[2 * current_position + 1])
                H.node[self.elements[2 * current_position + 1]]['child_status'] = 'right'
            current_position += 1
        if H.nodes():
            pos = self.layout(H, self.elements[1])
            nx.draw(H, pos, with_labels=True)
        plt.savefig("/tmp/algo/f.png")
        return "/tmp/algo/f.png"

if __name__ == "__main__":
    DataStructureVisualization(BinarySearchTree()).run()
