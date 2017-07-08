import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


class SearchingAlgorithm:
    """
    Base class for all Searching Algorithms
    """
    def __init__(self, name: str):
        """
        Constructor
        :param name: Name of Searching algorithm being implemented
        """
        self.count = 0
        self.name = name

    def search(self, arr:np.ndarray, key):
        """
        The core search method
        :param arr: numpy array, in witch the search is performed
        :param key: the element to be searched
        :return: True if key in arr else False
        """
        self.count = 0
        pass
        # Do search in derived classes


class LinearSearch(SearchingAlgorithm):
    def __init__(self):
        SearchingAlgorithm.__init__(self, "Linear Search")

    def search(self, arr:np.ndarray, key) -> bool:
        SearchingAlgorithm.search(self, arr, key)
        for i in range(0, arr.size - 1):
            self.count += 1
            if arr[i] == key:
                return True
        return False


class BinarySearch(SearchingAlgorithm):
    def __init__(self):
        SearchingAlgorithm.__init__(self, "Binary Search")

    def search(self, arr:np.ndarray, key) -> bool:
        SearchingAlgorithm.search(self, arr, key)
        SearchingAlgorithm.search(self, arr, key)
        low, high = 0, arr.size - 1
        while low <= high:
            mid = int((low + high) / 2)
            self.count += 1
            if arr[mid] == key:
                return True
            elif arr[mid] < key:
                low = mid + 1
            else:
                high = mid - 1
        return False


class SearchVisualizer:
    """
    Class for Visualizing Search algorithms
    """
    def __init__(self, searcher: SearchingAlgorithm):
        """
        Constructor for visualizer
        :param searcher: Implementation of a Searching Algorithm
        """
        self.searcher = searcher
        self.fig = plt.figure()

    def analyze(self, maxpts=1000):
        """
        Plots the running time of sorting algorithm
        Checks for 3 cases, Already Sorted array, reverse sorted array and Shuffled array
        Analysis is done  by inputting integer arrays with size staring from 100, and varying
        upto maxpts in the steps of 100, and counting the number of basic operations
        :param maxpts: Maximum number of element in the array, using witch analysis is done
        """
        # x Number of elements
        # y_1 number of comparisons when First Element is the key
        # y_2 number of comparisons when Middle Element is the key
        # y_3 number of comparisons when key is not present in the array
        x, y_1, y_2, y_3 = np.array([0]), np.array([0]), np.array([0]), np.array([0])
        for i in range(100, maxpts, 100):
            x = np.vstack((x, [i]))
            arr = np.arange(0, i, 1)
            key = 0
            self.searcher.search(arr, key)
            y_1 = np.vstack((y_1, [self.searcher.count]))
            key = int(i / 2)
            self.searcher.search(arr, key)
            y_2 = np.vstack((y_2, [self.searcher.count]))
            key = i + 1
            self.searcher.search(arr, key)
            y_3 = np.vstack((y_3, [self.searcher.count]))
        plt.suptitle(self.searcher.name + " Analysis", size=19)
        plt.subplot(2, 2, 1)
        plt.title("First Element as key")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_1)
        plt.subplot(2, 2, 2)
        plt.title("Middle Element as key")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_2)
        plt.subplot(2, 2, 3)
        plt.title("Key is not in the array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_3)
        plt.tight_layout(pad=2)
        plt.show()

    @staticmethod
    def compare(algorithms):
        """
         Compares the given list of Searching Algorithms and Plots a bar chart
         :param algorithms: List of Searching Algorithms
         """
        arr = np.arange(2000)
        key = np.random.randint(0,2000)
        operations = []
        for algorithm in algorithms:
            algorithm.search(arr,key)
            operations.append((algorithm.name,algorithm.count))
        operations = sorted(operations,key=lambda x:x[0])
        rects = plt.bar(left=np.arange(len(operations)),height=[y for (x,y) in operations])
        plt.xticks(np.arange(len(operations)),[x for (x,y) in operations])
        ax = plt.axes()
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')
        plt.show()


if __name__ == "__main__":
    # SearchVisualizer(BinarySearch()).analyze(maxpts=10000)
    SearchVisualizer.compare([LinearSearch(),BinarySearch()])