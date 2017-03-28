package org.openalgorithm;

import java.util.Scanner;

public class Main { //Testing mergeSort!
    public static void main(String[] args)  {
        System.out.println("Enter number of items : ");
        int size = new Scanner(System.in).nextInt();
        System.out.println("Enter items : ");
        String[] arr = new String[size];
        int i = 0;
        String string = new Scanner(System.in).nextLine();
        for(String s : string.split("\\s+"))    {
            arr[i++] = s;
        }
        String[] sorted = Sort.mergeSort(arr);
        for(String x : sorted)
            System.out.println(x);

    }
}