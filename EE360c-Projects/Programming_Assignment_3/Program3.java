/*
 * Name: Nicholas Strohmeyer
 * EID: nas3882
 */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;

/**
 * Your solution goes in this class.
 * 
 * Please do not modify the other files we have provided for you, as we will use
 * our own versions of those files when grading your project. You are
 * responsible for ensuring that your solution works with the original version
 * of all the other files we have provided for you.
 * 
 * That said, please feel free to add additional files and classes to your
 * solution, as you see fit. We will use ALL of your additional files when
 * grading your solution.
 */

public class Program3 extends AbstractProgram3 {

    // GLOBALS to be accessed by any method / used for memoizing
    private ArrayList<ArrayList<ArrayList<Integer>>> P = new ArrayList<>(); // "P" for "positions"
    private ArrayList<ArrayList<Integer>> R = new ArrayList<>(); // "R" for "response times"
    private ArrayList<Integer> houses = new ArrayList<>();
    //private int memoX = 0;

    /**
     * Determines the solution of the optimal response time for the given input TownPlan. Study the
     * project description to understand the variables which represent the input to your solution.
     * @return Updated TownPlan town with the "responseTime" field set to the optimal response time
     */
    @Override
    public TownPlan findOptimalResponseTime(TownPlan town) {
        //long startTime = System.nanoTime();
        
        houses = town.getHousePositions();
        int n = houses.size();
        int k = town.getStationCount();

        // initialize Position & Response matrices
        for (int i = 0; i < n; i++){
            ArrayList<Integer> tempR = new ArrayList<>();
            ArrayList<ArrayList<Integer>> tempP = new ArrayList<>();
            ArrayList<Integer> empty = new ArrayList<>();
            for (int j = 0; j < k; j++){
                if ( j > i){ tempR.add(0); }
                else  { tempR.add(-1); } //-1 is flag = "never seen before"
                tempP.add(empty);
            }
            R.add(tempR); P.add(tempP);
        }

        //Solve problem, set responseTime, and return town (with stationPositions untouched)
        TownPlan best = findOptimalTown(0, n-1, k); //n-1 for end of array bc 0-indexed
        town.setResponseTime(best.getResponseTime());

        // for testing runtime
        //long endTime   = System.nanoTime();
        //long totalTime = (endTime - startTime);
        //System.out.println(totalTime);
        //System.out.println(memoX);
        return town;
    }

    /**
     * Determines the solution of the set of police station positions that optimize response time for the given input TownPlan. Study the
     * project description to understand the variables which represent the input to your solution.
     * @return Updated TownPlan town with the "policeStationPositions" field set to the optimal police station positions
     */
    @Override
    public TownPlan findOptimalPoliceStationPositions(TownPlan town) {
        houses = town.getHousePositions();
        int n = houses.size();
        int k = town.getStationCount();
        
        // initialize Position & Response matrices
        for (int i = 0; i < n; i++){
            ArrayList<Integer> tempR = new ArrayList<>();
            ArrayList<ArrayList<Integer>> tempP = new ArrayList<>();
            ArrayList<Integer> empty = new ArrayList<>();
            for (int j = 0; j < k; j++){
                if ( j > i){ tempR.add(0); }
                else { tempR.add(-1);} //-1 is flag = "never seen before"
                tempP.add(empty);
            }
            R.add(tempR); P.add(tempP);
        }

        //Solve problem, set positions and return town (with responseTime untouched)
        TownPlan best = findOptimalTown(0, n-1, k); //n-1 for end of array bc 0-indexed
        town.setPoliceStationPositions(best.getPoliceStationPositions());
        return town;
    }


    // recursive engine to solve problem. start, stop determine a slice of the house array & j is the # of stations for this subproblem
    private TownPlan findOptimalTown(int start, int stop, int j){
        //memo flag: 
        boolean memo = false; 
        if (start == 0) memo = true;

        // inits        
        ArrayList<Integer> slice =  createSlice(start, stop);
        ArrayList<Integer> stations = new ArrayList<>();
        int currBest = 0;
        TownPlan subTown = new TownPlan(stop - start + 1, j, slice);
        int m = subTown.getHouseCount();

        //is problem already memoized ? 
        if (memo){
            Integer check = R.get(stop).get(j-1);
            if (check != -1){
                setTown(subTown, R.get(stop).get(j-1), P.get(stop).get(j-1));
                //memoX ++ ;
                return subTown;
            }
        }
        
        // base cases are the first 2: 
        // Case 1: more stations than houses -- includes 1 house case
        if(j >= m){
            for (int i = 0; i < m; i++){
                stations.add(houses.get(start+i)); // place a station on every house
            }
        }
        // Case 2: One station
        else if ( (m > j) && (j == 1) ){
            int mid = (houses.get(start) + houses.get(stop))/ 2;   //odds round down, station at midpoint
            stations.add(mid);  //add to stations list
            currBest = max(houses.get(stop) - mid, mid - houses.get(start)); // in case of odd length interval -- although problem specs never will be
        }
        // Case 3: Recursive calls
        else{
            currBest = -1;
            //special test
            //if (start == 6 && stop == 9){
                //System.out.println("hi");
            //}
            for (int i = 0; i < slice.size()-1; i++){  // we don't need to loop through k, simply put 1 up top always
                //try to hack my runtime with if(j > m/2 ) else top-down? 
                //bottom-up
                TownPlan lowerTown = findOptimalTown(start, i, j-1);
                TownPlan upperTown = findOptimalTown(i + 1, stop, 1);
                //top-down
                //TownPlan upperTown = findOptimalTown(stop-i, stop, 1);
                //TownPlan lowerTown = findOptimalTown(start, stop-i-1, j-1);
                int response = max(upperTown.getResponseTime(), lowerTown.getResponseTime());
                if ( (currBest == -1) || (currBest > response) ){
                    currBest = response;
                    stations = mergeStations(lowerTown.getPoliceStationPositions(), upperTown.getPoliceStationPositions());
                }
            }
        }
        // after checking memoization, all cases, & possible iteration/recursion, update memoization (if memo = true ) & return best solution 
        if (memo){ memoize(stations, currBest, m-1, j-1); }   // 0-indexing
        setTown(subTown, currBest, stations);
        //subtown.setPoliceStationPositions(stations);
        //subTown.setResponseTime(currBest);
        return subTown;
    }

    /* #######################  HELPERS (to eliminate repeated code) ###################################*/

    // need a method that combines police station positions from each branch of the recursive call
    private ArrayList<Integer> mergeStations(ArrayList<Integer> left , ArrayList<Integer> right){
        ArrayList<Integer> merge = new ArrayList<Integer>(); 
        for (int i = 0; i < left.size(); i++){
            merge.add(left.get(i));
        }
        for (int i = 0; i < right.size(); i++){
            merge.add(right.get(i));
        }
        //System.out.println(" array: " + merge.toString());
        return merge;
    }

    private void memoize(ArrayList<Integer> stations, int response, int t, int j){
        R.get(t).set(j, response);
        // P.get(t).get(j).addAll(stations); // I think the addAll function is misinterpreting and adding all to both levels of arrays
        //ArrayList<Integer> placeholder = P.get(t).get(j);
        //placeholder.addAll(stations);
        P.get(t).set(j, stations);
        /*if (j > 0){
            System.out.println( t + "," + (j-1) + " array: " + P.get(t).get(j-1));
        }*/
        //below is for testing
        //Integer check = R.get(t).get(j);
        //ArrayList<Integer> arrayCheckAgain = P.get(t).get(j);
        //System.out.println(t + "," + j + " case: " + check + " array: " + arrayCheckAgain.toString());
    }

    // my own sublist method instead of importing List class, inclusive on both ends. Does NOT preserve index, must be careful here
    private ArrayList<Integer> createSlice(int start, int stop){
        ArrayList<Integer> slice = new ArrayList<>();
        for (int i = start; i < stop+1; i++){
            slice.add(houses.get(i));
        }
        return slice;
    }

    private Integer max(Integer r1 , Integer r2){
        if (r1 > r2) return r1;
        else return r2;
    }

    private void setTown(TownPlan town, int response , ArrayList<Integer> stations){
            town.setPoliceStationPositions(stations);
            town.setResponseTime(response);
    }
}
