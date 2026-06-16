#ifndef CORGI_H
#define CORGI_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdint.h>

typedef struct{
    char county[100];                                    // Name of the county
    char state[100];                                     // Name of the state
    float Age_Percent_65_and_Older;                     // Percent 65 and older
    float Age_Percent_Under_18_Years;                   // Percent under 18 years
    float Age_Percent_Under_5_Years;                    // Percent under 5 years
    float Education_Bachelors_Degree_or_Higher;         // Percent with Bachelor's degree or higher
    float Education_High_School_or_Higher;              // Percent with High School education or higher
    uint64_t Employment_Nonemployer_Establishments;     // Count of nonemployer establishments
    uint64_t Employment_Private_Non_farm_Employment;    // Count of private non-farm employment
    float Employment_Private_Non_farm_Employment_Change;// Percent change in private non-farm employment
    uint64_t Employment_Private_Non_farm_Establishments;// Count of private non-farm establishments
    float Ethnicities_American_Indian_and_Alaska_Native_Alone; // Percent American Indian and Alaska Native alone
    float Ethnicities_Asian_Alone;                      // Percent Asian alone
    float Ethnicities_Black_Alone;                      // Percent Black alone
    float Ethnicities_Hispanic_or_Latino;               // Percent Hispanic or Latino
    float Ethnicities_Native_Hawaiian_and_Other_Pacific_Islander_Alone; // Percent Native Hawaiian and Other Pacific Islander alone
    float Ethnicities_Two_or_More_Races;                // Percent two or more races
    float Ethnicities_White_Alone;                      // Percent White alone
    float Ethnicities_White_Alone_not_Hispanic_or_Latino; // Percent White alone not Hispanic or Latino
    float Housing_Homeownership_Rate;                   // Homeownership rate
    uint64_t Housing_Households;                        // Number of households
    uint64_t Housing_Housing_Units;                     // Number of housing units
    uint32_t Housing_Median_Value_of_Owner_Occupied_Units; // Median value of owner-occupied units
    float Housing_Persons_per_Household;                // Persons per household
    float Housing_Units_in_Multi_Unit_Structures;       // Percent of units in multi-unit structures
    uint32_t Income_Median_Household_Income;            // Median household income
    uint32_t Income_Per_Capita_Income;                  // Per capita income
    float Income_Persons_Below_Poverty_Level;           // Percent below poverty level
    uint64_t Miscellaneous_Building_Permits;            // Count of building permits
    float Miscellaneous_Foreign_Born;                   // Percent foreign born
    float Miscellaneous_Land_Area;                     // Land area in square miles
    float Miscellaneous_Language_Other_than_English_at_Home; // Percent speaking other languages at home
    float Miscellaneous_Living_in_Same_House_1_Years;   // Percent living in the same house for 1+ years
    uint64_t Miscellaneous_Manufacturers_Shipments;     // Value of manufacturers shipments
    float Miscellaneous_Mean_Travel_Time_to_Work;       // Mean travel time to work (minutes)
    float Miscellaneous_Percent_Female;                 // Percent female population
    uint64_t Miscellaneous_Veterans;                    // Count of veterans
    uint64_t Population_2010_Population;                // Population in 2010
    uint64_t Population_2014_Population;                // Population in 2014
    float Population_Population_Percent_Change;         // Percent population change
    float Population_Population_per_Square_Mile;        // Population density
    uint64_t Sales_Accommodation_and_Food_Services_Sales; // Accommodation and food services sales
    uint64_t Sales_Merchant_Wholesaler_Sales;           // Merchant wholesaler sales
    uint64_t Sales_Retail_Sales;                        // Retail sales
    uint32_t Sales_Retail_Sales_per_Capita;             // Retail sales per capita
    uint64_t Employment_Firms_American_Indian_Owned;    // Count of American Indian-owned firms
    uint64_t Employment_Firms_Asian_Owned;              // Count of Asian-owned firms
    uint64_t Employment_Firms_Black_Owned;              // Count of Black-owned firms
    uint64_t Employment_Firms_Hispanic_Owned;           // Count of Hispanic-owned firms
    uint64_t Employment_Firms_Native_Hawaiian_Owned;    // Count of Native Hawaiian-owned firms
    uint64_t Employment_Firms_Total;                    // Total count of firms
    uint64_t Employment_Firms_Women_Owned;
} Info;

void trim_whitespace(char *str) {
    int len = strlen(str);
    if (len > 1 && str[0] == '"' && str[len - 1] == '"') {
        memmove(str, str + 1, len - 2);
        str[len - 2] = '\0';
    }
}

int parsing(char *line, Info *information){
    char buffer[4000];
    strcpy(buffer, line);
    //copy county into structure
    char *token = strtok(buffer, ",");
    if(!token){
        return -1;
    }
    trim_whitespace(token);
    strcpy(information->county, token);
    //copy state into structure
    token = strtok(NULL, ",");
    if(!token){
        return -1;
    }
    trim_whitespace(token);
    strcpy(information->state, token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Age_Percent_65_and_Older = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Age_Percent_Under_18_Years = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Age_Percent_Under_5_Years = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Education_Bachelors_Degree_or_Higher = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Education_High_School_or_Higher = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Nonemployer_Establishments = atoll(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Private_Non_farm_Employment = atoll(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Private_Non_farm_Employment_Change = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Private_Non_farm_Establishments = atoll(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_American_Indian_and_Alaska_Native_Alone = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_Asian_Alone = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_Black_Alone = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_Hispanic_or_Latino = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_Native_Hawaiian_and_Other_Pacific_Islander_Alone = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_Two_or_More_Races   = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_White_Alone = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Ethnicities_White_Alone_not_Hispanic_or_Latino = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Housing_Homeownership_Rate = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Housing_Households = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Housing_Housing_Units = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Housing_Median_Value_of_Owner_Occupied_Units = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Housing_Persons_per_Household = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Housing_Units_in_Multi_Unit_Structures = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Income_Median_Household_Income = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Income_Per_Capita_Income = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Income_Persons_Below_Poverty_Level = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Building_Permits = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Foreign_Born = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Land_Area = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Language_Other_than_English_at_Home = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Living_in_Same_House_1_Years = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Manufacturers_Shipments = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Mean_Travel_Time_to_Work = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Percent_Female = atof(token);

    token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Miscellaneous_Veterans = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Population_2010_Population = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Population_2014_Population = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Population_Population_Percent_Change = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Population_Population_per_Square_Mile = atof(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Sales_Accommodation_and_Food_Services_Sales = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Sales_Merchant_Wholesaler_Sales = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Sales_Retail_Sales = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Sales_Retail_Sales_per_Capita = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_American_Indian_Owned = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_Asian_Owned = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_Black_Owned = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_Hispanic_Owned = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_Native_Hawaiian_Owned = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_Total = atoll(token);

     token = strtok(NULL, ",");
    if (!token) return -1;
    trim_whitespace(token);
    information->Employment_Firms_Women_Owned = atoll(token);
    
    return 0;
 }

#endif


