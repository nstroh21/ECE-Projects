/*
 * Name: <your name>
 * EID: <your EID>
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
public class Program1 extends AbstractProgram1 {


    /**
     * Determines whether a candidate Matching represents a solution to the stable matching problem.
     * Study the description of a Matching in the project documentation to help you with this.
     */
    @Override
    public boolean isStableMatching(Matching problem) {
        // get some things
        ArrayList<Integer> solution = problem.getStudentMatching();
        int m = problem.getHighSchoolCount();
        int n = problem.getStudentCount(); 

        /* I see no way of doing this other than brute force;
            iterate through all matches and caputre both types 1 and 2 of instability */
        for ( int student = 0 ; student < n ; student++ ){
            
            ArrayList<Integer> studentPref = problem.getStudentPreference().get(student); //gets the ith student's preference list from 2d array
            Integer currentMatch = solution.get(student);
            //type 1 instability
            if (currentMatch.equals(-1)){
                if (!checkHigherPreferences(student, problem, solution, m-1)){ // this method abstracts the checking process for either type of instability
                        return false;
                }
                else continue;  //check next student
            }
            // type 2 instability
            else{
                int currMatchIndex = studentPref.indexOf(currentMatch);  // same as above except start search from current match, look at only the higher preferences
                if (!checkHigherPreferences(student, problem, solution, currMatchIndex - 1)){
                    return false;
                }
                else continue;

            }
        } // we have checked for all students, it is a stable matching    
    return true;
    }

    /**
     * Determines a solution to the stable matching problem from the given input set. Study the
     * project description to understand the variables which represent the input to your solution.
     *
     * @return A stable Matching.
     */

    // A lot of this will be very similar to school optimal except here we are going to use the review applicant method (which makes algorithm deg 3 time)
    @Override
    public Matching stableMatchingGaleShapley_studentoptimal(Matching problem) {
        
        int n = problem.getStudentCount();
        int m = problem.getHighSchoolCount();
        ArrayList<Integer> studentMatching = new ArrayList<Integer>();   // for final solution
        int[] prefPosition = new int[n];  // array where index is student and value is position in their preference array
        LinkedList<Integer> studentQueue = new LinkedList<Integer>();
        ArrayList<Integer> capacity = problem.getHighSchoolSpots();
        ArrayList<ArrayList<Integer>> rosters = new ArrayList<>(m);  // as we traverse, we need to keep track of rosters at school level


        // start out with all students as free, put all students in queue:
        for (int i = 0; i < n; i++){
            studentMatching.add(Integer.valueOf(-1));
            studentQueue.add(Integer.valueOf(i));
        }
        // put all students into the queue , also init pref pos arr with all 0's 
        for (int i = 0; i < m; i++){
            ArrayList<Integer> empty = new ArrayList<Integer>();
            rosters.add(empty);
            prefPosition[i] = 0;
        }

        // top of while loop, while queue is not empty : 
        while (!studentQueue.isEmpty()){
            Integer student = studentQueue.remove();    // pop student
            int s = student.intValue(); // use for student index
            ArrayList<Integer> studentPref = problem.getStudentPreference().get(s);

            /* //for debugging: 
            if (s == 57){
                System.out.println("pause");
            }*/

            //"pos" = position
            for (int pos = prefPosition[s]; pos < studentPref.size(); pos++){
                Integer school = studentPref.get(pos);
                int h = school.intValue(); // school index
                ArrayList<Integer> schoolPref = problem.getHighSchoolPreference().get(h);
                int spots = capacity.get(h).intValue();   // capacity stores spots open at this school
                ArrayList<Integer> thisRoster = rosters.get(h);
                //int rosterSize = thisRoster.size() ;
                
                //  if student is on last option & not accepted, update the pref array. Not actually needed because student drops off the queue either way but just for consistency
                if (pos == studentPref.size()-1){
                    prefPosition[s] = pos+1;
                }

                // check if school has space
                if (spots > 0) {
                    // set new match, freeze pref position, decrement spots & save to capacity, re-order roster, break school loop
                    studentMatching.set(s, school);
                    prefPosition[s] = pos + 1; 
                    spots -- ;
                    capacity.set(h, Integer.valueOf(spots));
                    buildRoster(student, thisRoster, schoolPref);
                    break;
                }

                // otherwise (spots full) call reviewApplicant : returns key of rejected student & rebuilds roster if applicant is accepted
                Integer response = reviewApplicant(student, schoolPref, thisRoster, spots);
                
                //rejected :
                if (response.equals(student)){
                    continue;
                }
                else{
                    // set new match , unmatch old student, put them on queue, freeze pref position, capacity is still 0 (no change)
                    studentMatching.set(s, school);
                    int swapIdx = response.intValue(); 
                    studentMatching.set(swapIdx, Integer.valueOf(-1)); 
                    studentQueue.add(response);  // put rejected student back onto the queue
                    prefPosition[s] = pos + 1;
                    break;
                }
            } // if we get through all schools on prefList , student has no match

            /* //gut check
            if (s == 57){
                System.out.println(studentMatching.get(s));
            }*/

        } // we are finished traversing all students
        problem.setStudentMatching(studentMatching);
        return problem;
    }

    /**
     * Determines a solution to the stable matching problem from the given input set. Study the
     * project description to understand the variables which represent the input to your solution.
     *
     * @return A stable Matching.
     */
    @Override
    public Matching stableMatchingGaleShapley_highschooloptimal(Matching problem) {

        int n = problem.getStudentCount();
        int m = problem.getHighSchoolCount();
        ArrayList<Integer> studentMatching = new ArrayList<Integer>();   // for final solution
        int[] prefPosition = new int[m];  // array where index is a school and value is where we left off in their preference list
        LinkedList<Integer> schoolQueue = new LinkedList<Integer>();
        ArrayList<Integer> capacity = problem.getHighSchoolSpots();

        // start out with all students as free :
        for (int i = 0; i < n; i++){
            studentMatching.add(Integer.valueOf(-1));
        }
        // put all schools into the queue :
        for (int i = 0; i < m; i++){
            schoolQueue.add(Integer.valueOf(i));
        }
        //preference positions all start at 0 :
        for (int i = 0; i < m; i++){
            prefPosition[i] = 0;
        }

        // while queue is not empty :
        while (!schoolQueue.isEmpty()){
            Integer school = schoolQueue.remove();  
            int h = school.intValue(); // use as highschool index
            ArrayList<Integer> schoolPref = problem.getHighSchoolPreference().get(h);

            //"pos" = position, the index we last left off on for this school
            for (int pos = prefPosition[h]; pos < schoolPref.size(); pos++ ){
                Integer student = schoolPref.get(pos);
                int s = student.intValue(); // use as student index
                Integer current = studentMatching.get(s); //student's current match
                int hPrime = current.intValue(); // current match index
                
                // if spots filled, freeze pref position, break and go on to the next school
                if (capacity.get(h).equals(0)){  
                    prefPosition[h] = pos;
                    break;
                }
                //isStudentFree ?
                //yes
                if (current.equals(Integer.valueOf(-1))){
                    studentMatching.set(s, school); // create new match
                    capacity.set(h, capacity.get(h) - 1); // decrement school capacity
                }
                //no
                else{
                    ArrayList<Integer> studPref = problem.getStudentPreference().get(s);   // get the student preference list
                    // does student prefer this school over current ?      
                    boolean result = reviewSchool(school, current, studPref);
                    // if yes match student to school, else continue to next student
                    if (result == true){
                        studentMatching.set(s, school);
                        capacity.set(h, capacity.get(h) - 1); //decrement school's spots
                        capacity.set(hPrime, capacity.get(hPrime) + 1); //increment current's spots
                        schoolQueue.add(current);   // put free school back onto queue
                    }
                    else continue;
                } 

            }
        }        
        // when while loop is done, we should have a stable matching (school optimal)
        problem.setStudentMatching(studentMatching);
        return problem;
    }

    /* =======================  END of Main Algorithms , DROP Helper MethodS BELOW =================================== */
    // these methods sometimes appear with "helpers." preceding. What's the cleanest way ?

    /*  DESC: returns free student, or -1 if no free students. Also rebuilds the roster with applicant inserted */
    public static Integer reviewApplicant(Integer applicant, ArrayList<Integer> schoolPreference , ArrayList<Integer> schoolRoster , int limit ){
        int size = schoolRoster.size();
        // depending how we call this method, the following base case would likely be avoided
        if ( size < limit ) {
            buildRoster(applicant, schoolRoster, schoolPreference);
            return -1;
        }
        // otherwise assume the roster is in order, simply compare to the last studnet on the list
        Integer check = schoolRoster.get(size - 1);
        int checkRank = schoolPreference.indexOf(Integer.valueOf(check));
        int applicantRank = schoolPreference.indexOf(Integer.valueOf(applicant));  
        if (applicantRank < checkRank){
            //applicant is preferred to lowest ranked student, so we remove the lowest ranked student:
            schoolRoster.remove(size-1);
            //and then insert applicant in the correct position in roster :
            buildRoster(applicant, schoolRoster, schoolPreference);
            return check;
        }
        return applicant;
    }



    /*  DESC: the idea is that if the roster is starting from empty, it should be relatively inexpensive to keep it in sorted order */
    public static void buildRoster(Integer newStudent , ArrayList<Integer> currRoster, ArrayList<Integer> schoolPref ){
        // base case
        if (currRoster.isEmpty() == true) {
            currRoster.add(newStudent);
            return;
        }
        int end = currRoster.size() - 1;
        int newRank = schoolPref.indexOf(newStudent);
        // traversing backward bc I'm assuming if  n >> spots then likely a newStudent will go towards the end but doesn't matter that much
        for (int n = end; n >= 0 ; n--){
            // ranks of each student
            int checkRank = schoolPref.indexOf(currRoster.get(n)); 
            if (newRank > checkRank){
                currRoster.add(n+1, newStudent);
                return;
            }
        }
        // if entire for loop executes, then student should go to top of roster
        currRoster.add(0, newStudent);
        return;
    }


    /* DESC: return true if the sudent prefers the new school to their current school, else return false */
    public static boolean reviewSchool(Integer school, Integer current, ArrayList<Integer> studentPreference ){
        // this will tell us if a student prefers a school to their current match
        int schoolRank = studentPreference.indexOf(school);
        int currentRank = studentPreference.indexOf(current);  // these need to be indexOF functions i think (not get())
        // edge case -- what if they are equal ? --> should stay false because we wouldn't change anything
        if (schoolRank < currentRank){
            return true;
        } 
        else{
             return false;
        }
    }


    /*  DESC: goes through a student's preferences (from low to high) to see if a school higher on their list will accept them */   
    public static boolean checkHigherPreferences(Integer student, Matching problem, ArrayList<Integer> solution, int startFrom){ 
        
        ArrayList<Integer> studentPrefLocalCopy = problem.getStudentPreference().get(student.intValue()); // i am just re-accessing instead of passing it in

        for (int j = startFrom; j >= 0; j--){

            Integer school = studentPrefLocalCopy.get(j);
            int h = school.intValue();  //use as school index
            ArrayList<Integer> schoolPref = problem.getHighSchoolPreference().get(h);
            
            //  we go through the entire solution to look for any instance of this school
            for ( int k = 0 ; k < solution.size(); k ++ ){
                // following condition finds an instance of school, k is the current matched student key
                if (school.equals(solution.get(k))){
                    Integer compare = Integer.valueOf(k);
                    int pref1 = schoolPref.indexOf(compare);
                    int pref2 = schoolPref.indexOf(student);
                    if (pref1 > pref2){
                        // then this is not stable , because student and school we are checking prefer each other to current match
                        
                        /*FOR TESTING:
                        System.out.println("Unstable group is {format : (student, school) x 2} :");
                        System.out.println("(" + student + ", " + solution.get(student.intValue()) + ")");
                        System.out.println("(" + k + ", " + school + ")"); */

                        return false;
                    }
                    else continue;
                }
                else continue;               
            } // match was stable, look for the next student matched to this school on the solution array (k for loop)
        }  // if we get here, then the previous school did not prefer student. Check next school (decrement j)                      
        
        return true;
    }
        

}