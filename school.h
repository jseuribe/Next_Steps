//
//  school.h
//  NextStepMethod
//
//  Created by NextStep on 3/1/16.
//  Copyright © 2016 NextStep. All rights reserved.
//

#ifndef school_h
#define school_h

#include <string>

class School {
public:
    // Default Constructor
    School();
    
    // Parameter Constructor
    School(const std::string& input_name,
           const std::string& input_city,
           const unsigned int& input_average_sat_score,
           const unsigned int& input_average_student_debt,
           const unsigned int& input_average_tuition_cost,
           const unsigned int& input_average_student_population,
           const unsigned int& input_transfer_rate
           );
    
    // Copy Constructor
    School(const School& a_school);
    
    // Destructor
    ~School();
    
    // Copy Assignment Operator
    School& operator=(const School& right_hand_side);
    
    // Prefix operator++ Overload
    School& operator++();
    
    // Postfix operator++ Overload
    School operator++(int);
    
    // operator<< Overload
    friend std::ostream& operator<<(std::ostream& out_stream, const School& output_school);
    
    const std::string getName();
    const std::string getCity();
    const unsigned int getAverageSATScore();
    const unsigned int getAverageStudentDebt();
    const unsigned int getAverageTuitionCost();
    const unsigned int getAverageStudentPopulation();
    const unsigned int getTransferRate();
    const unsigned int getBookmarks();
    void incrementBookmarks();
    
private:
    std::string name_;
    std::string city_;
    unsigned int average_sat_score_;
    unsigned int average_student_debt_;
    unsigned int average_tuition_cost_;
    unsigned int average_student_population_;
    unsigned int transfer_rate_;
    unsigned int bookmarks_;
}; // end School

#include "school.cpp"

#endif /* school_h */
