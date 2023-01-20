/*
 * Name: Nicholas Strohmeyer
 * EID: nas3882
 */

// Implement your heap here
// Methods may be added to this file, but don't remove anything
// Include this file in your final submission

import java.util.ArrayList;

public class Heap {
    private ArrayList<Student> minHeap;

    public Heap() {
        minHeap = new ArrayList<Student>();
    }

    /**
     * buildHeap(ArrayList<Student> students)
     * Given an ArrayList of Students, build a min-heap keyed on each Student's minCost
     * Time Complexity - O(nlog(n)) or O(n)
     *
     * @param students
     */
    public void buildHeap(ArrayList<Student> students) {
        int n = students.size();
        minHeap = students;
        // call heapify-down in reverse order starting from first non-leaf
        for (int i = n/2 - 1; i >= 0; i--){
            heapifyDown(i);
        }
    }

    /**
     * insertNode(Student in)
     * Insert a Student into the heap.
     * Time Complexity - O(log(n))
     *
     * @param in - the Student to insert.
     */
    public void insertNode(Student in) {
        // paste to end, and call heapify-up
        minHeap.add(in);
        heapifyUp(minHeap.size()-1);
    }

    /**
     * findMin()
     * Time Complexity - O(1)
     *
     * @return the minimum element of the heap.
     */
    public Student findMin() {
        if (minHeap.size() == 0) {
            return null;
        } else{
            return minHeap.get(0); 
        }
    }

    /**
     * extractMin()
     * Time Complexity - O(log(n))
     *
     * @return the minimum element of the heap, AND removes the element from said heap.
     */
    public Student extractMin() {
        if (minHeap.size() == 0) {
            return null;
        }
        else{
            Student min = minHeap.get(0); 
            this.delete(0);
            return min;
        }
    }

    /**
     * delete(int index)
     * Deletes an element in the min-heap given an index to delete at.
     * Time Complexity - O(log(n))
     *
     * @param index - the index of the item to be deleted in the min-heap.
     */
    public void delete(int index) {
        // base case
        if (minHeap.size() == 1){
            minHeap.remove(index);
            return;
        }
        // replace with the last element & call heapify down
        Student lastElmt = minHeap.get(minHeap.size()-1);
        minHeap.remove(minHeap.size()-1);
        minHeap.set(index, lastElmt);
        heapifyDown(index);
        return;
    }

    /**
     * changeKey(Student r, int newCost)
     * Changes minCost of Student s to newCost and updates the heap.
     * Time Complexity - O(log(n))
     *
     * @param r       - the Student in the heap that needs to be updated.
     * @param newCost - the new cost of Student r in the heap (note that the heap is keyed on the values of minCost)
     */
    public void changeKey(Student r, int newCost) {
        // for path algos we expect change to get smaller.. but both cases are considered:
        // possible safeguard to ensure it is in Q 
        int ind = minHeap.indexOf(r);
        if (ind < 0){
            System.out.println("Error: Item was not found in queue");
            return;
        }
        int currCost = r.getminCost();
        r.setminCost(newCost);
        if (currCost > newCost) {
            heapifyUp(ind); 
        }
        if (currCost < newCost){
            heapifyDown(ind); 
        }
    }

    public String toString() {
        String output = "";
        for (int i = 0; i < minHeap.size(); i++) {
            output += minHeap.get(i).getName() + " ";
        }
        return output;
    }

    // HELPER METHODS BELOW //
    private void heapifyUp(int index){
        Student node = minHeap.get(index);
        //base case at the root:
        if (index == 0) return;
        else{
            int parentIndex = (index-1)/2;
            Student parent = minHeap.get(parentIndex);
            if (node.getminCost() < parent.getminCost() || (node.getminCost() == parent.getminCost() && nameCompare(parent, node) == node)){
                minHeap.set(index, parent);
                minHeap.set(parentIndex, node);
                // and recursive call up:
                heapifyUp(parentIndex);
            }
            else return; // node is at correct level, stop recursive calls
        }
    }

    private void heapifyDown(int index){
        Student node = minHeap.get(index);
        Student minChild = null;
        if (2*index + 2 < minHeap.size()){
            Student left = minHeap.get(2*index + 1);
            Student right = minHeap.get(2*index + 2);
            if (left.getminCost() > right.getminCost()) minChild = right;
            else if (left.getminCost() < right.getminCost()) minChild = left;
            else minChild = nameCompare(left, right);
        } 
        else if (2*index + 1 < minHeap.size()){
            Student left = minHeap.get(2*index + 1);
            minChild = left;
        }
        else{
            // the node is a leaf and we should return up the recursive stack
            return;
        }
        // next compare to parent and see if we need to make swap
        if (minChild.getminCost() < node.getminCost() || (minChild.getminCost() == node.getminCost() && nameCompare(minChild, node) == minChild)) {
            int placeholder = minHeap.indexOf(minChild);
            minHeap.set(index, minChild);
            minHeap.set(placeholder, node);
            // and recursive call down :
            heapifyDown(placeholder);
        }
    }
    private Student nameCompare(Student a, Student b){
        if (a.getName() > b.getName()) return b;
        else return a;
    }

///////////////////////////////////////////////////////////////////////////////
//                           DANGER ZONE                                     //
//                everything below is used for grading                       //
//                      please do not change :)                              //
///////////////////////////////////////////////////////////////////////////////

    public ArrayList<Student> toArrayList() {
        return minHeap;
    }
}
