//
//  profile.cpp
//  NextStepMethod
//
//  Created by NextStep on 3/1/16.
//  Copyright © 2016 NextStep. All rights reserved.
//
//

#include "profile.h"

Profile::Profile()
{
} // end Default Constructor

Profile::Profile(const Profile& a_profile) : name_(a_profile.name_),
                                                location_(a_profile.location_),
                                                sat_score_(a_profile.sat_score_)
{
} // end Copy Constructor

Profile::~Profile()
{
} // end Destructor

Profile& Profile::operator=(const Profile& right_hand_side)
{
    Profile copy(right_hand_side);
    std::swap(*this, copy);
    return *this;
} // end operator= Overload

std::ostream& operator<<(std::ostream& out_stream, const Profile& output_profile)
{
    out_stream << "Name: " << output_profile.name_ << std::endl;
    out_stream << "Location: " << output_profile.location_ << std::endl;
    out_stream << "Average SAT Score: " << output_profile.sat_score_ << std::endl;
    
    return out_stream;
} // end operator<< Overload

const std::string Profile::getName()
{
    return name_;
} // end getName

const std::string Profile::getLocation()
{
    return location_;
} // end getLocation

const unsigned int Profile::getSATScore()
{
    return sat_score_;
} // end getSATScore