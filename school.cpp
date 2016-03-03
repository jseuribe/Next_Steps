//
//  school.cpp
//  NextStepMethod
//
//  Created by NextStep on 3/1/16.
//  Copyright © 2016 NextStep. All rights reserved.
//

#include "school.h"

School::School() :  name_("no_entry"),
                    city_("no_entry"),
                    average_sat_score_(NULL),
                    average_student_debt_(NULL),
                    average_tuition_cost_(NULL),
                    average_student_population_(NULL),
                    transfer_rate_(NULL),
                    bookmarks_(0)
{
} // end Default Constructor

School::School(const std::string& input_name,
               const std::string& input_city,
               const unsigned int& input_average_sat_score,
               const unsigned int& input_average_student_debt,
               const unsigned int& input_average_tuition_cost,
               const unsigned int& input_average_student_population,
               const unsigned int& input_transfer_rate) :
                name_(input_name),
                city_(input_city),
                average_sat_score_(input_average_sat_score),
                average_student_debt_(input_average_student_debt),
                average_tuition_cost_(input_average_tuition_cost),
                average_student_population_(input_average_student_population),
                transfer_rate_(input_transfer_rate),
                bookmarks_(0)
{
} // end Parameter Constructor

School::School(const School& a_school) : name_(a_school.name_),
                                        city_(a_school.city_),
                                        average_sat_score_(a_school.average_sat_score_),
                                        average_student_debt_(a_school.average_student_debt_),
                                        average_tuition_cost_(a_school.average_tuition_cost_),
                                        average_student_population_(a_school.average_student_population_),
                                        transfer_rate_(a_school.transfer_rate_),
                                        bookmarks_(a_school.bookmarks_)
{
} // end Copy Constructor

School::~School()
{
} // end Destructor

School& School::operator=(const School& right_hand_side)
{
    School copy(right_hand_side);
    std::swap(*this, copy);
    return *this;
} // end operator= Overload

School& School::operator++()
{
    incrementBookmarks();
    return *this;
} // end operator++ Prefix Overload

School School::operator++(int)
{
    School result(*this);
    ++(*this);
    return result;
} // end operator++ Postfix Overload

std::ostream& operator<<(std::ostream& out_stream, const School& output_school)
{
    out_stream << "Name: " << output_school.name_ << std::endl;
    out_stream << "City: " << output_school.city_ << std::endl;
    out_stream << "Average SAT Score: " << output_school.average_sat_score_ << std::endl;
    out_stream << "Average Student Debt: $" << output_school.average_student_debt_ << std::endl;
    out_stream << "Average Tuition Cost: $" << output_school.average_tuition_cost_ << std::endl;
    out_stream << "Average Student Population: " << output_school.average_student_population_ << std::endl;
    out_stream << "Transfer Rate: " << output_school.transfer_rate_ << "%" << std::endl;
    out_stream << "Bookmarks: " << output_school.bookmarks_ << std::endl;
    
    return out_stream;
} // end operator<< Overload

const std::string School::getName()
{
    return name_;
} // end getName

const std::string School::getCity()
{
    return city_;
} // end getCity

const unsigned int School::getAverageSATScore()
{
    return average_sat_score_;
} // end getAverageSATScore

const unsigned int School::getAverageStudentDebt()
{
    return average_student_debt_;
} // end getAverageStudentDebt

const unsigned int School::getAverageTuitionCost()
{
    return average_tuition_cost_;
} // end getAverageTuitionCost

const unsigned int School::getAverageStudentPopulation()
{
    return average_student_population_;
} // end getAverageStudentPopulation

const unsigned int School::getTransferRate()
{
    return transfer_rate_;
} // end getTransferRate

const unsigned int School::getBookmarks()
{
    return bookmarks_;
} // end getBookmarks

void School::incrementBookmarks()
{
    bookmarks_++;
} // end incrementBookmarks