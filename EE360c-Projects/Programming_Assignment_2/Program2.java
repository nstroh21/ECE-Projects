/*
 * Name: Nicholas Strohmeyer
 * EID: nas3882
 */

// Implement your algorithms here
// Methods may be added to this file, but don't remove anything
// Include this file in your final submission

import java.util.ArrayList;

public class Program2 {
    private ArrayList<Student> students;    // this is a list of all Students, populated by Driver class
    private Heap minHeap;

    // additional constructors may be added, but don't delete or modify anything already here
    public Program2(int numStudents) {
        minHeap = new Heap();
        students = new ArrayList<Student>();
    }

    /**
     * findMinimumStudentCost(Student start, Student dest)
     *
     * @param start - the starting Student.
     * @param dest  - the end (destination) Student.
     * @return the minimum cost possible to get from start to dest.
     * Assume the given graph is always connected.
     */
    public int findMinimumStudentCost(Student start, Student dest) {
        //inherently creating shortest paths Tree although not remembering it
        if (start.equals(dest)){
            return 0;
        }
        //initialize heap, S( explored nodes), extract start, set pathLength var
        Heap Q = new Heap();
        Q.buildHeap(students);
        Q.changeKey(start, 0);
        ArrayList<Student> S = new ArrayList<Student>();
        Student node;
        int stop = dest.getName();
        int currLength = 0;

         // the minCost attribute is getting updated as we go and that represents the S-P tree implicitly
        while (Q.findMin() != null){
            // get next node to explore
            node = Q.extractMin();
            currLength = node.getminCost();
            // check if the node is our destination, in which case we can stop now
            if (node.getName() == stop) break;
            ArrayList<Student> neighbors = node.getNeighbors();
            ArrayList<Integer> prices = node.getPrices();
           
            for (int i = 0; i < neighbors.size(); i++){
                Student check = neighbors.get(i);
                if (S.size() > 0){
                    if (S.contains(check)){
                        continue;
                    }
                }
                int price = (int)prices.get(i);
                // relax edges
                if (currLength + price < check.getminCost()){
                    Q.changeKey(check, currLength + price);
                }
            }
            // node has been explored, put it into S
            S.add(node);
        }
        return currLength;
    }

    /**
     * findMinimumClassCost()
     *
     * @return the minimum total cost required to connect (span) each student in the class.
     * Assume the given graph is always connected.
     */
    public int findMinimumClassCost() {
        // using Prim's algorithm ... would be interesting to try Kruskal too
        Student root = students.get(0);
        //init heap with root = 0 cost, all else inf
        Heap Q = new Heap();
        Q.buildHeap(students);
        Q.changeKey(root,0);
        int totalCost = 0;

        while (Q.findMin() != null){
            Student node = Q.extractMin();
            totalCost += node.getminCost();
            if (Q.findMin() == null){
                break;
            }
            ArrayList<Student> edges = node.getNeighbors();
            ArrayList<Integer> costs = node.getPrices();
            for (int i = 0; i < edges.size(); i++ ){
                Student check = edges.get(i);
                Integer cost = costs.get(i);
                // if check is still in queue and cost can be reduced :
                if (( Q.toArrayList().indexOf(check) > -1 ) && ( cost < check.getminCost() )){
                    Q.changeKey(check, (int)cost);
                }
            }
            // update node based on minimum edge in explored set (extractmin() at top of loop)
        }


        return totalCost;
    }

    //returns edges and prices in a string.
    public String toString() {
        String o = "";
        for (Student v : students) {
            boolean first = true;
            o += "Student ";
            o += v.getName();
            o += " has neighbors ";
            ArrayList<Student> ngbr = v.getNeighbors();
            for (Student n : ngbr) {
                o += first ? n.getName() : ", " + n.getName();
                first = false;
            }
            first = true;
            o += " with prices ";
            ArrayList<Integer> wght = v.getPrices();
            for (Integer i : wght) {
                o += first ? i : ", " + i;
                first = false;
            }
            o += System.getProperty("line.separator");

        }

        return o;
    }

///////////////////////////////////////////////////////////////////////////////
//                           DANGER ZONE                                     //
//                everything below is used for grading                       //
//                      please do not change :)                              //
///////////////////////////////////////////////////////////////////////////////

    public Heap getHeap() {
        return minHeap;
    }

    public ArrayList<Student> getAllstudents() {
        return students;
    }

    // used by Driver class to populate each Student with correct neighbors and corresponding prices
    public void setEdge(Student curr, Student neighbor, Integer price) {
        curr.setNeighborAndPrice(neighbor, price);
    }

    // used by Driver.java and sets students to reference an ArrayList of all Students
    public void setAllNodesArray(ArrayList<Student> x) {
        students = x;
    }
}
