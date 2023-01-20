import java.util.ArrayList;
import java.util.LinkedList;
//import java.util.ArrayDeque;
//import java.util.Deque; 

/*  NOTES TO SELF:
    -----------------------------------------------------
        - using a linkedList like a stack :  you can use keywords push / pop 
        - using the linkedList like a queue : you can use keywords add()/ remove()
        - in either case peekFirst() or peekLast() is a way to see if our queue/stack is empty 
        - oracle documentation recommends using deque interface as a stack instead of util.stack class: Deque<Integer> stack = new ArrayDeque<Integer>;
        - However in the final code, i'm simply going to use the linkedList like a queue/stack
        - STATIC ERROR : I would need to create a helpers object in other programs if I want to use these functions freely, otherwise make them static so they apply class-wide
    -----------------------------------------------------------------------
*/

/*  Purpose of file :
    -----------------
        - store helper methods to plug in to Program1 functions for ease of code readability and re-usability
        - scratch work & thoughts/difficulties encountered along the way 06/25/2022
    -------------------------------------------------------------------------
*/


public class helpers  {


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
        // edge case -- what if they are equal ?? 
        if (schoolRank < currentRank){
            return true;
        } 
        else{
             return false;
        }
    }


    /*  DESC: goes through a student's preferences (from low to high) to see if a school higher on their list will accept them */   
    public static boolean checkHigherPreferences(Integer student, Matching problem, ArrayList<Integer> solution, int startFrom){ 
        
        for (int j = startFrom; j >= 0; j--){

            Integer school = Integer.valueOf(j);
            int h = school.intValue();  //use as school index
            ArrayList<Integer> schoolPref = problem.getHighSchoolPreference().get(h);
            
            //  we go through the entire solution to look for any instance of this school
            for ( int k = 0 ; k < solution.size(); k ++ ){
                // following condition finds an instance of school, k is the current mathced student key
                if (school.equals(solution.get(k))){
                    Integer compare = Integer.valueOf(k);
                    Integer studentInt = Integer.valueOf(student);
                    int pref1 = schoolPref.indexOf(compare);
                    int pref2 = schoolPref.indexOf(studentInt);
                    if (pref1 > pref2){
                        // then this is not stable , because student and school we are checking prefer each other to current match
                        return false;
                    }
                    else continue;
                }
                else continue;               
            } // match was stable, look for the next student matched to this school on the solution array (k for loop)
        }  // if we get here, then the previous school did not prefer student. Check next school (decrement j)                      
        
        return true;
    }





    // practice/skeleton algorithm
    public boolean isStableMatching(Matching problem){ 

        ArrayList<Integer> solution = problem.getStudentMatching();
        for ( int student = 0 ; student < solution.size(); student++ ){

            // to get the first type of instability, we would basically need to run G-S for an unmatched student ? 
            // basically could run the algorithm below except when we get their current match we will get -1, in which case we'll just look at their whole preference list
            // -1  --> check preferences.size() 

            // PICK UP HERE TOMORROW TODO


            // Everything below here is checking hte second type of instability
            ArrayList<Integer> studentPref = problem.getStudentPreference().get(student); //gets the ith student's preference list from 2d array
            Integer currMatchIndex = studentPref.indexOf(solution.get(student)); //solution.get(i) should be the school key
            for (int j = 0; j < currMatchIndex; j++){
                 // Integer check = studentPref.get(j); I'm high so i forget what this was

                 Integer school = Integer.valueOf(j);

                // get the school's preference list in order to call reviewApplicant
                ArrayList<Integer> jPref = problem.getHighSchoolPreference().get(j);
        
                // variation of reviewApplicant because i don't have a roster here so instead will need to iterate through solution array
                // 2 types of instability -- But what about if a school still has space and student prefers it ? Or is this impossible becasue algorithm keeps executing
                
                //student applies
                // First: check the 2nd type of instability
                for ( int k = 0 ; k < solution.size(); k = k ++ ){
                    //truncate solution to ensure this temrinates --> nevermind "no need to be fancy" says stack overflow
                    if (school.equals(solution.get(k))){
                        // school compares student to someone on its roster (k)
                        int compare = k;
                        Integer compareInt = Integer.valueOf(compare);
                        int pref1 = jPref.indexOf(compareInt);
                        Integer studentInt = Integer.valueOf(student);
                        int pref2 = jPref.indexOf(studentInt);
                        if (pref1 > pref2){
                            // then this is not stable , because student and school we are checking prefer each other to current match
                            return false;
                        }
                        else{
                            // we want to look for the next student on the matchlist which is what this for loop does
                            continue;
                        }
                    }
                    else{ continue; }                
                }
                // if we get here, then the previous school did not prefer student. Check next school (increment j)                      
            }
            // if we get here, then we are done checking for this student. increment i (student) to the next in our solution
        }
    // if we get here, then we have checked for all students, it is a stable matching    
        return true;
    }

}
