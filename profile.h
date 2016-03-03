//
//  profile.h
//  NextStepMethod
//
//  Created by NextStep on 3/1/16.
//  Copyright © 2016 NextStep. All rights reserved.
////

#ifndef profile_h
#define profile_h

#include <string>

class Profile{
public:
    // Default Constructor
    Profile();
    
    // Copy Constructor
    Profile(const Profile& a_profile);
    
    // Destructor
    ~Profile();
    
    // Copy Assignment Operator
    Profile& operator=(const Profile& right_hand_side);
    
    // operator<< Overload
    friend std::ostream& operator<<(std::ostream& out_stream, const Profile& output_profile);
    
    const std::string getName();
    const std::string getLocation();
    const unsigned int getSATScore();
private:
    std::string name_;
    std::string location_;
    unsigned int sat_score_;
}; // end Profile

#include "profile.cpp"

#endif /* profile_h */
