/*
 * Name: Nicholas Strohmeyer
 * EID: nas3882
 */

// Methods may be added to this file, but don't remove anything
// Include this file in your final submission

import java.util.*;

public class Student {
    private int minCost;
    private int name;
    private ArrayList<Student> neighbors;
    private ArrayList<Integer> prices;

    public Student(int x) {
        name = x;
        minCost = Integer.MAX_VALUE;
        neighbors = new ArrayList<Student>();
        prices = new ArrayList<Integer>();
    }

    public void setNeighborAndPrice(Student n, Integer w) {
        neighbors.add(n);
        prices.add(w);
    }

    public ArrayList<Student> getNeighbors() {
        return neighbors;
    }

    public ArrayList<Integer> getPrices() {
        return prices;
    }

    public int getminCost() { return minCost; }

    public void setminCost(int x) {
        minCost = x;
    }

    public void resetminCost() {
        minCost = Integer.MAX_VALUE;
    }

    public int getName() {
        return name;
    }
    // returns the minimum student in a comparison
    public Student compare(Student b){
        if (this.getminCost() > b.getminCost()){
            return b;
        }
        else return this;
    }
}
