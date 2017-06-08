import matplotlib.pyplot as plt
import numpy.random as ran
import matplotlib.animation as animation
import seaborn as sb
from multiprocessing import Process
import numpy as np


class SortingAlgorithm:
    def __init__(self,name):
        self.name = name
        self.hist_array = None
        self.count = 0

    def sort(self,array,visualization):
        self.count = 0
        if visualization:
            self.hist_array = np.array(array)
        pass
        # Do sorting in derived classes


class BubbleSort(SortingAlgorithm):
    def __init__(self):
        SortingAlgorithm.__init__(self,"Bubble Sort")

    def sort(self,array,visualization=False):
        SortingAlgorithm.sort(self,array,visualization)
        for i in range(0, array.size):
            exch = False
            for j in range(0, array.size - i - 1):
                self.count += 1
                if array[j] > array[j + 1]:
                    array[j],array[j+1] = array[j+1],array[j]
                    exch = True
                if visualization:
                    self.hist_array = np.vstack([self.hist_array, array])
            if not exch:
                break
        if visualization:
            self.hist_array = np.vstack([self.hist_array, array])


class InsertionSort(SortingAlgorithm):
    def __init__(self):
        SortingAlgorithm.__init__(self, "Insertion Sort")

    def sort(self,array,visualization=False):
        SortingAlgorithm.sort(self, array,visualization)
        for i in range(1, array.size):
            ele = array[i]
            ins_pos = i - 1
            while ins_pos >= 0 and ele < array[ins_pos]:
                self.count += 1
                array[ins_pos + 1] = array[ins_pos]
                ins_pos -= 1
                if visualization:
                    self.hist_array = np.vstack([self.hist_array, array])
            array[ins_pos + 1] = ele
        if visualization:
            self.hist_array = np.vstack([self.hist_array, array])


class SelectionSort(SortingAlgorithm):
    def __init__(self):
        SortingAlgorithm.__init__(self, "Selection Sort")

    def sort(self,array,visualization=False):
        SortingAlgorithm.sort(self, array,visualization)
        for i in range(array.size):
            min_index = i
            for j in range(i + 1, array.size):
                self.count += 1
                if array[min_index] > array[j]:
                    min_index = j
            array[i], array[min_index] = array[min_index], array[i]
            if visualization:
                self.hist_array = np.vstack([self.hist_array, array])
        if visualization:
            self.hist_array = np.vstack([self.hist_array, array])


class MergeSort(SortingAlgorithm):
    def __init__(self):
        SortingAlgorithm.__init__(self, "Merge Sort")

    def sort(self,array,visualization=False):
        SortingAlgorithm.sort(self, array,visualization)
        unit = 1
        while unit <= array.size:
            for h in range(0, array.size, unit * 2):
                l, r = h, min(array.size, h + 2 * unit)
                mid = h + unit
                # merge xs[h:h + 2 * unit]
                p, q = l, mid
                while p < mid and q < r:
                    self.count += 1
                    if array[p] < array[q]:
                        p += 1
                    else:
                        tmp = array[q]
                        array[p + 1: q + 1] = array[p:q]
                        array[p] = tmp
                        p, mid, q = p + 1, mid + 1, q + 1
                    if visualization:
                        self.hist_array = np.vstack([self.hist_array, array])
            unit *= 2
        if visualization:
            self.hist_array = np.vstack([self.hist_array, array])


class QuickSort(SortingAlgorithm):
    def __init__(self):
        SortingAlgorithm.__init__(self, "Quicksort")

    @staticmethod
    def __median_of_three(array, start, end, visualization=False):
        histarr = None
        count = 0
        if visualization:
            histarr = np.array(array)
        median = int((end - start) / 2)
        median = median + start
        left = start + 1
        if (array[median] - array[end - 1]) * (array[start] - array[median]) >= 0:
            array[start], array[median] = array[median], array[start]
        elif (array[end - 1] - array[median]) * (array[start] - array[end - 1]) >= 0:
            array[start], array[end - 1] = array[end - 1], array[start]
        pivot = array[start]
        for right in range(start, end + 1):
            count += 1
            if pivot > array[right]:
                array[left], array[right] = array[right], array[left]
                if visualization:
                    histarr = np.vstack([histarr, array])
                left = left + 1
        array[start], array[left - 1] = array[left - 1], array[start]
        return left - 1, histarr, count

    @staticmethod
    def __right_partition(arr, l, h, visualization=False):
        i = (l - 1)
        x = arr[h]
        hist = None
        if visualization:
            hist = np.array(arr)
        count = 0
        for j in range(l, h):
            if arr[j] <= x:
                count += 1
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
                if visualization:
                    hist = np.vstack([hist, arr])
        arr[i + 1], arr[h] = arr[h], arr[i + 1]
        return i + 1, hist, count

    def quickSortIterative(self,arr, l, h, partition_alg=__right_partition, visualization=False):
        # Create an auxiliary stack
        size = h - l + 1
        stack = [0] * size

        # initialize top of stack
        top = -1

        # push initial values of l and h to stack
        top = top + 1
        stack[top] = l
        top = top + 1
        stack[top] = h

        # Keep popping from stack while is not empty
        while top >= 0:

            # Pop h and l
            h = stack[top]
            top = top - 1
            l = stack[top]
            top = top - 1

            # Set pivot element at its correct position in
            # sorted array
            p, hist, comps = partition_alg(arr, l, h, visualization)
            self.count += comps
            if visualization:
                self.hist_array = np.vstack([self.hist_array, hist])
            # If there are elements on left side of pivot,
            # then push left side to stack
            if p - 1 > l:
                top = top + 1
                stack[top] = l
                top = top + 1
                stack[top] = p - 1

            # If there are elements on right side of pivot,
            # then push right side to stack
            if p + 1 < h:
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = h
        if visualization:
            self.hist_array = np.vstack([self.hist_array, arr])

    def sort(self,array, visualization=False):
        SortingAlgorithm.sort(self,array,visualization)
        self.quickSortIterative(array, 0, array.size - 1, partition_alg=self.__median_of_three, visualization=visualization)


class SortVisualizer:
    def __init__(self, sorter:SortingAlgorithm) -> None:
        self.sorter = sorter
        self.fig = plt.figure()
        self.index = 0

    def __update(self, i):
        """
        Update function for animation
        Sets new array state for scatter plot
        :param i: Sent by the animator indicating the frame number
        :return: Modified scatter plot
        """
        x = np.arange(self.hist_arr.shape[1])
        y = self.hist_arr[i]
        data = np.dstack((x, y))  # call self.scatter.get_offsets() to know about initial data format
        self.scatter.set_offsets(data)
        return self.scatter,

    def visualize(self, num=100, save=False):
        """
        Visualizes given Sorting Algorithm
        And saves it
        To-Do:       * Save it with user defined name
                     * Saving thread is too slow...Make it fast
                     * When saving is in progress, animation flickers, find a solution
        """
        plt.title(self.sorter.name + " Visualization")
        plt.xlabel("Array Index")
        plt.ylabel("Element")
        data = np.arange(num)
        ran.shuffle(data)
        self.sorter.sort(data,visualization=True)
        self.hist_arr = self.sorter.hist_array
        self.scatter = plt.scatter(np.arange(self.hist_arr.shape[1]), self.hist_arr[0])  # plt.scatter(x-array,y-array)
        self.animation = animation.FuncAnimation(self.fig, self.__update, frames=self.hist_arr.shape[0], repeat=False,
                                                 blit=False, interval=1)
        if save:
            p1 = Process(target=lambda: self.animation.save(self.sorter.name+".mp4", writer=animation.FFMpegWriter(fps=100)))
            p1.start()
        plt.show()

    def efficiency(self, maxpts=1000):
        """
        Plots the running time sorting algorithm
        Checks for 3 cases, Already Sorted array, reverse sorted array and Shuffled array
        Sorting Algorithm must return number of basic operations
        """
        # x is list of input sizes
        # y_1 running time in case of Sorted Array
        # y_2 running time in case of Shuffled Array
        # y_3 running time in case of Reverse Sorted Array
        x, y_1, y_2, y_3 = np.array([0]), np.array([0]), np.array([0]), np.array([0])
        for n in range(100, maxpts, 100):
            # Vary n from 100 to max in steps of 100
            i_1 = np.arange(n)  # array of items from 1 to n
            self.sorter.sort(i_1)
            val_sorted = self.sorter.count
            i_2 = i_1[::-1]  # reverse the array
            ran.shuffle(i_1)  # shuffle the array
            self.sorter.sort(i_1)
            val_normal = self.sorter.count
            self.sorter.sort(i_2)
            val_reverse = self.sorter.count
            x = np.vstack((x, [n]))  # add n to list x
            y_1 = np.vstack((y_1, [val_sorted]))  # add number of basic operations to y lists
            y_2 = np.vstack((y_2, [val_normal]))
            y_3 = np.vstack((y_3, [val_reverse]))
        plt.title(self.sorter.name + "Analysis")
        plt.subplot(2, 2, 1)
        plt.title("Sorted Array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_1)
        plt.subplot(2, 2, 2)
        plt.title("Randomly Shuffled Array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_2)
        plt.subplot(2, 2, 3)
        plt.title("Reverse Sorted Array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_3)
        plt.tight_layout(pad=2)
        plt.show()


if __name__ == "__main__":
    vis = SortVisualizer(MergeSort())
    vis.visualize()