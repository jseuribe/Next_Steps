//
//  main.cpp
//  NextStepMethod
//
//  Created by NextStep on 3/1/16.
//  Copyright © 2016 NextStep. All rights reserved.
//
//

#include <iostream>
#include <vector>
#include <stdlib.h> /* for rand() */
#include <time.h>   /* for time() */
#include "school.h"
#include "profile.h"
using namespace std;

// Function to calculate the Fit Number.
const unsigned int calculateFitNumber();

int main(int argc, const char * argv[]) {
    // Initilizing the Random Seed.
    srand((unsigned int) time(NULL));
    
    // Psuedo Database.
     const unsigned int number_of_schools = 10;
    vector<School> database_of_schools;
    vector<string> list_of_locations{"New York", "Philadelphia", "Boston", "Pittsburg", "Providence", "Hartford", "Buffalo", "Rochester"};
    
    // Randomizing Schools in the database.
    for (unsigned int i = 0; i < number_of_schools; i++) {
        const string school_name = "Some University " + to_string(i);
        const string city_name = list_of_locations[rand() % list_of_locations.size()];
        const unsigned int average_sat_score = rand() % 2401;
        const unsigned int average_student_debt = rand() % 200000;
        const unsigned int average_tuition_cost = rand() % 70000;
        const unsigned int average_sutdent_population = rand() % 20000;
        const unsigned int transfer_rate = rand() % 101;
        database_of_schools.push_back(School(school_name, city_name, average_sat_score, average_student_debt, average_sutdent_population, average_tuition_cost, transfer_rate));
        
        // To demonstrate how bookmarks are incremented.
        database_of_schools[i]++;
    } // end for
    
    // Displaying the entire database to the terminal.
    for (const auto& const_itr : database_of_schools)
        cout << const_itr << endl;
    
    return 0;
} // end main

const unsigned int calculateFitNumber() {
    unsigned int fit_number = 0;
    
    
    return fit_number;
} // end calculateFitNumber