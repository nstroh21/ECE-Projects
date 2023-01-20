// This Driver file will be replaced by ours during grading
// Do not include this file in your final submission

import java.io.File;
import java.util.*;

public class Driver {
    private static String filename; // input file name
    private static boolean testHeap; // set to true by -h flag
    private static boolean testMinStuCost; // set to true by -s flag
    private static boolean testMinClassCost; // set to true by -c flag
    private static Program2 testProgram2; // instance of your graph
    private static ArrayList<Student> students;

    private static void usage() { // error message
        System.err.println("usage: java Driver [-h] [-s] [-c] <filename>");
        System.err.println("\t-h\tTest Heap implementation");
        System.err.println("\t-s\tTest findMinimumStudentCost implementation");
        System.err.println("\t-c\tTest findMinimumClassCost implementation");
        System.exit(1);
    }

    public static void main(String[] args) throws Exception {
        students = new ArrayList<Student>();
        parseArgs(args);
        parseInputFile(filename);
        testRun();
    }

    public static void parseArgs(String[] args) {
        boolean flagsPresent = false;
        if (args.length == 0) {
            usage();
        }
        filename = "";
        testHeap = false;
        testMinStuCost = false;
        testMinClassCost = false;
        for (String s : args) {
            if (s.equals("-h")) {
                flagsPresent = true;
                testHeap = true;
            } else if (s.equals("-s")) {
                flagsPresent = true;
                testMinStuCost = true;
            } else if (s.equals("-c")) {
                flagsPresent = true;
                testMinClassCost = true;
            } else if (!s.startsWith("-")) {
                filename = s;
            } else {
                System.err.printf("Unknown option: %s\n", s);
                usage();
            }
        }

        if (!flagsPresent) {
            testHeap = true;
            testMinStuCost = true;
            testMinClassCost = true;
        }
    }

    public static void parseInputFile(String filename) throws Exception {
        int numV = 0, numE = 0;
        Scanner sc = new Scanner(new File(filename));
        String[] inputSize = sc.nextLine().split(" ");
        numV = Integer.parseInt(inputSize[0]);
        numE = Integer.parseInt(inputSize[1]);
        HashMap<Integer, ArrayList<NeighborPriceTuple>> tempNeighbors = new HashMap<>();
        testProgram2 = new Program2(numV);
        for (int i = 0; i < numV; ++i) {

            String[] pairs = sc.nextLine().split(" ");
            String[] pricePairs = sc.nextLine().split(" ");

            Integer currNode = Integer.parseInt(pairs[0]);
            Student currentStudent = new Student(currNode);
            students.add(currNode, currentStudent);
            ArrayList<NeighborPriceTuple> currNeighbors = new ArrayList<>();
            tempNeighbors.put(currNode, currNeighbors);

            for (int k = 1; k < pairs.length; k++) {
                Integer neighborVal = Integer.parseInt(pairs[k]);
                Integer priceVal = Integer.parseInt(pricePairs[k]);
                currNeighbors.add(new NeighborPriceTuple(neighborVal, priceVal));
            }
        }
        for (int i = 0; i < students.size(); ++i) {
            Student currStudent = students.get(i);
            ArrayList<NeighborPriceTuple> neighbors = tempNeighbors.get(i);
            for (NeighborPriceTuple neighbor : neighbors) {
                testProgram2.setEdge(currStudent, students.get(neighbor.neighborID), neighbor.price);
            }
        }

        testProgram2.setAllNodesArray(students);
    }

    // feel free to alter this method however you wish, we will replace it with our own version during grading
    public static void testRun() {
        if (testHeap) {
            // test out Heap.java here
            // the code below is an example of how to test your heap
            // you will want to do more extensive testing than just this
            /* Student zero = new Student(0);
            zero.setminCost(10);
            Student one = new Student(1);
            one.setminCost(20);
            Student two = new Student(2);
            two.setminCost(30);

            ArrayList<Student> tester = new ArrayList<>();
            tester.add(two);
            tester.add(zero);
            tester.add(one);

            testProgram2.getHeap().buildHeap(tester);
            System.out.println(testProgram2.getHeap());
            testProgram2.getHeap().changeKey(zero, 100);
            testProgram2.getHeap().changeKey(one, 1000);
            System.out.println(testProgram2.getHeap()); */
            
            //create some test nodes
            ArrayList<Student> newNodes = new ArrayList<Student>();
            int key = 5;
            for (int i = 10; i >= 0; i--){
                Student temp = new Student(i);
                temp.setminCost(i);
                newNodes.add(temp);
            }
            
            
            // test buildHeap 
            testProgram2.getHeap().buildHeap(newNodes);
            ArrayList<Student> heapList = testProgram2.getHeap().toArrayList();
            ArrayList<Integer> keys = new ArrayList<Integer>();
            System.out.println("Original buildheap : ");
            for (Student node : heapList){
                keys.add(node.getminCost());
            }
            System.out.println("Original buildheap : ");
            System.out.println(keys);

            //extract min -- heapSort
            System.out.println("\n Sorted Heap: \n");
            boolean run = true;
            while (run == true){
                Student min = testProgram2.getHeap().extractMin();
                if (min == null){
                    run = false;
                }
                else{
                    System.out.println(min.getminCost());
                }
            }

            // Should be null
            Heap thisThingIsNull = testProgram2.getHeap();
            System.out.println(thisThingIsNull);

            ArrayList<Student> newNodes2 = new ArrayList<Student>();

            // Test Build Heap # 2 
            for (int i = 0; i < 11; i++){
                Student temp = new Student(3+i);
                temp.setminCost(key*i);
                newNodes2.add(temp);
                if ((key*i)%2 == 0) key += 3*i;
                else key -= 2*i;
                if (key< 0) key = key*-1;

            }

            System.out.println("Second Heap is: \n");
            Collections.reverse(newNodes2);
            for (Student node : newNodes2){ System.out.println(node.getminCost());}
            
            testProgram2.getHeap().buildHeap(newNodes2);
            heapList = testProgram2.getHeap().toArrayList();
            ArrayList<Integer> keys2 = new ArrayList<Integer>();
            for (Student node : heapList){
                keys2.add(node.getminCost());
            }
            System.out.println("Second buildheap : ");
            System.out.println(keys2);

            //extract min -- heapSort
            System.out.println("\n Sorted Second Heap: \n");
            boolean run2 = true;
            while (run2 == true){
                Student min = testProgram2.getHeap().extractMin();
                if (min == null){
                    run2 = false;
                }
                else{
                    System.out.println(min.getminCost());
                }
            }
            
            
             // Test Build Heap # 3 
             int key3 = 45;
             ArrayList<Student> newNodes3 = new ArrayList<Student>();
             for (int i = 0; i < 100; i++){
                Student temp = new Student(i);
                temp.setminCost(key3);
                newNodes3.add(temp);
                if (i%2 == 0) key3 += 11;
                else key3 -= 13;
                //if (key3 < 0) key3 = key3*-1;

            }

            //System.out.println("Third Heap is: \n");
            Collections.reverse(newNodes3);
            //for (Student node : newNodes3){ System.out.println(node.getminCost());}
            
            testProgram2.getHeap().buildHeap(newNodes3);
            heapList = testProgram2.getHeap().toArrayList();
            ArrayList<Integer> keys3 = new ArrayList<Integer>();
            for (Student node : heapList){
                keys3.add(node.getminCost());
            }
            System.out.println("Third buildheap : ");
            System.out.println(keys3);
            boolean result = isValidHeap(testProgram2.getHeap().toArrayList());
            System.out.println("Is Valid?:  " + result + '\n') ;

            //extract min -- heapSort
            System.out.println("\n Sorted third Heap: \n");
            boolean run3 = true;
            while (run3 == true){
                Student min = testProgram2.getHeap().extractMin();
                if (min == null){
                    run3 = false;
                }
                else{
                    System.out.println(min.getminCost());
                }
            }
            Student thing = testProgram2.getHeap().findMin();
            System.out.println(thing.getName());

            
        }

        if (testMinStuCost) {
            // test out Program2.java findMinimumStudentCost here
            System.out.println("\nGiven wire configuration: ");
            System.out.println(testProgram2);
            System.out.println("Minimum student cost " + testProgram2.findMinimumStudentCost(students.get(1), students.get(4)));    
        }
        if (testMinClassCost) {
            // test out Program2.java findMinimumClassCost here
            System.out.println("\nGiven wire configuration: ");
            System.out.println(testProgram2);
            System.out.println("Minimum class cost: \n" + testProgram2.findMinimumClassCost());
        }
    }


    private static class NeighborPriceTuple {
        public Integer neighborID;
        public Integer price;

        NeighborPriceTuple(Integer neighborID, Integer price) {
            this.neighborID = neighborID;
            this.price = price;
        }
    }

    private static boolean isValidHeap(ArrayList<Student> heap){
        for(int i = 0; i < (heap.size()/2) - 1 ; i++ ){
            Student left = heap.get(2*i+1);
            int lMin = left.getminCost();
            int childMin = lMin;
            if (heap.size() >= 2*i + 3){
                Student right = heap.get(2*i + 1);
                int rMin = right.getminCost();
                if (lMin > rMin){
                    childMin = rMin; 
                }
            }
            if (childMin < heap.get(i).getminCost()){
                return false;
            }
        }
        return true;
    }
}
