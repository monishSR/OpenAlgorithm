package org.openalgorithm;

public final class Sort {
    public static double[] heapSort(double[] array, HeapType heapType)    {
        Double[] dArray = new Double[array.length];
        for(int i = 0;i < array.length;i++)
            dArray[i] = array[i];
        BinaryHeap<Double> binaryHeap = new BinaryHeap<>(dArray, heapType);
        double[] sorted = new double[dArray.length];
        for (int i = 0;i < array.length;i++)  {
            try {
                sorted[i] = binaryHeap.remove();

            }
            catch (InvalidOperationException e) {
                System.out.println(e.getMessage());
            }
        }
        return sorted;
    }

    private static double[] merge(double[] a, double[] b) {
        double[] merged = new double[a.length + b.length];
        int i = 0, j = 0, k = 0;
        while (i < a.length && j < b.length)
            if (a[i] <= b[j])
                merged[k++] = a[i++];
            else
                merged[k++] = b[j++];
        while (i < a.length)
            merged[k++] = a[i++];
        while (j < b.length)
            merged[k++] = b[j++];
        return merged;
    }

    public static double[] mergeSort(double[] array)  {
        if(array.length == 1)
            return array;
        double[] left = new double[array.length / 2];
	//for (int i = 0; i < array.length / 2; i++)
	//	left[i] = array[i];
        System.arraycopy(array,0,left,0,array.length / 2);
	double[] right = new double[array.length - array.length / 2];
	//for (int i = 0; i < array.length - array.length / 2; i++)
	//	right[i] = array[array.length / 2 + i];
        System.arraycopy(array,array.length / 2,right,0,array.length - array.length / 2);
	left = mergeSort(left);
	right = mergeSort(right);
	return merge(left, right);
    }
}
