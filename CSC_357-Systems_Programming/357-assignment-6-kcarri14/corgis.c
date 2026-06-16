#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "corgis.h"
// loads data from csv file
int load_data(char *filename, Info **info){
    FILE *file = fopen(filename, "r");
    if(!file){
        perror("Error: can't open file");
        return -1;
    }
    char line[1024];
    int line_num = 0;
    int count = 0;
    *info = malloc(3143 * sizeof(Info));
    while(fgets(line, sizeof(line), file)){
        line_num++;
        if(line_num == 1){
            continue;
        }
        Info information;
        if(parsing(line, &information) == -1){
            //printf("Error: line entry is malformed %d\n", line_num);
            continue;
        }
        (*info)[count++] = information;

    }
    fclose(file);
    return count;
}
// when display is in .ops this function will be called
void display_counties(Info *information, int *count){
    for(int i = 0; i < *count; i++){
        printf("%s, %s\n", information[i].county, information[i].state);
        printf("\tPopulation: %llu\n", information[i].Population_2014_Population);
        printf("\tEducation \n");
        printf("\t\t>= High School: %.6f%%\n", information[i].Education_High_School_or_Higher);
        printf("\t\t>= Bachelor's Degree: %.6f%%\n", information[i].Education_Bachelors_Degree_or_Higher);
        printf("\tEthnicity Percentages \n");
        printf("\t\tAmerican Indian and Alsaka Native: %.6f%%\n", information[i].Ethnicities_American_Indian_and_Alaska_Native_Alone);
        printf("\t\tAsian Alone: %.6f%%\n", information[i].Ethnicities_Asian_Alone);
        printf("\t\tBlack Alone: %.6f%%\n", information[i].Ethnicities_Black_Alone);
        printf("\t\tHispanic or Latino: %.6f%%\n", information[i].Ethnicities_Black_Alone);
        printf("\t\tNative Hawaiian and Other Pacific Islander Alone: %.6f%%\n", information[i].Ethnicities_Native_Hawaiian_and_Other_Pacific_Islander_Alone);
        printf("\t\tTwo or More Races: %.6f%%\n", information[i].Ethnicities_Two_or_More_Races);
        printf("\t\tWhite Alone: %.6f%%\n", information[i].Ethnicities_White_Alone);
        printf("\t\tWhite Alone, not Hispanic or Latino: %.6f%%\n", information[i].Ethnicities_White_Alone_not_Hispanic_or_Latino);
        printf("\tIncome \n");
        printf("\t\tMedian Household: %d%%\n", information[i].Income_Median_Household_Income);
        printf("\t\tPer Capita: %d%%\n", information[i].Income_Per_Capita_Income);
        printf("\t\tBelow Pverty Level: %.6f%%\n", information[i].Income_Persons_Below_Poverty_Level);
    }
}
// filters out the number of entries of state
void filter_state(Info *information, int *count, char *state){
    int new_count = 0;
    for(int i = 0; i < *count; i++){
        if(strcmp(information[i].state, state) ==0){
            information[new_count++] = information[i];
        }
    }
    *count = new_count;
    printf("Filter: state == %s (%d entries)\n", state, new_count);
}
//filters out on a specific field
void filter_field(Info *information, int *count, char *field, char *comparison, float value){
    int new_count = 0;
    for(int i = 0; i < *count; i++){
        float field_value;
        if (strcmp(field, "Education.High School or Higher") == 0) {
            field_value = information[i].Education_High_School_or_Higher;
        } else if (strcmp(field, "Education.Bachelor's Degree or Higher") == 0) {
            field_value = information[i].Education_Bachelors_Degree_or_Higher;
        } else if (strcmp(field, "Income.Persons Below Poverty Level") == 0) {
            field_value = information[i].Income_Persons_Below_Poverty_Level;
        } else if (strcmp(field, "Ethnicities.American Indian and Alaska Native Alone") == 0) {
            field_value = information[i].Ethnicities_American_Indian_and_Alaska_Native_Alone;
        } else if (strcmp(field, "Ethnicities.Asian Alone") == 0) {
            field_value = information[i].Ethnicities_Asian_Alone;
        } else if (strcmp(field, "Ethnicities.Black Alone") == 0) {
            field_value = information[i].Ethnicities_Black_Alone;
        } else if (strcmp(field, "Ethnicities.Hispanic or Latino") == 0) {
            field_value = information[i].Ethnicities_Hispanic_or_Latino;
        } else if (strcmp(field, "Ethnicities.Native Hawaiian and Other Pacific Islander Alone") == 0) {
            field_value = information[i].Ethnicities_Native_Hawaiian_and_Other_Pacific_Islander_Alone;
        } else if (strcmp(field, "Ethnicities.Two or More Races") == 0) {
            field_value = information[i].Ethnicities_Two_or_More_Races;
        } else if (strcmp(field, "Ethnicities.White Alone") == 0) {
            field_value = information[i].Ethnicities_White_Alone;
        } else if (strcmp(field, "Ethnicities.White Alone, not Hispanic or Latino") == 0) {
            field_value = information[i].Ethnicities_White_Alone_not_Hispanic_or_Latino;  
        }else {
            fprintf(stderr, "Error: Unsupported field '%s'\n", field);
            return;
        }

        if(strcmp(comparison, "ge") == 0){
            if(field_value >= value){
                information[new_count++] = information[i];
            }else{
                continue;
            }

        }else if(strcmp(comparison, "le") == 0){
            if(field_value <= value){
                information[new_count++] = information[i];
            }else{
                continue;
            }
        }
    }

    *count = new_count;
    printf("Filter: %s, %s, %.2f (%d entries)\n", field, comparison, value, *count);

}
// gives the total population number
void population_total(Info *information, int count){
    int population_total_number = 0;
    for(int i = 0; i < count; i++){
        population_total_number += information[i].Population_2014_Population;
    }
    printf("2014 population: %d\n", population_total_number);
}
// gives population percentage by the field
void population_field(Info *information, int *count, char *field){
    int sub_pop = 0;
    for(int i = 0; i < *count; i++){
        float percentage;
        if (strcmp(field, "Education.High School or Higher") == 0) {
            percentage = information[i].Education_High_School_or_Higher;
        } else if (strcmp(field, "Education.Bachelor's Degree or Higher") == 0) {
            percentage = information[i].Education_Bachelors_Degree_or_Higher;
        } else if (strcmp(field, "Income.Persons Below Poverty Level") == 0) {
            percentage = information[i].Income_Persons_Below_Poverty_Level;
        } else if (strcmp(field, "Ethnicities.American Indian and Alaska Native Alone") == 0) {
            percentage = information[i].Ethnicities_American_Indian_and_Alaska_Native_Alone;
        } else if (strcmp(field, "Ethnicities.Asian Alone") == 0) {
            percentage = information[i].Ethnicities_Asian_Alone;
        } else if (strcmp(field, "Ethnicities.Black Alone") == 0) {
            percentage = information[i].Ethnicities_Black_Alone;
        } else if (strcmp(field, "Ethnicities.Hispanic or Latino") == 0) {
            percentage = information[i].Ethnicities_Hispanic_or_Latino;
        } else if (strcmp(field, "Ethnicities.Native Hawaiian and Other Pacific Islander Alone") == 0) {
            percentage = information[i].Ethnicities_Native_Hawaiian_and_Other_Pacific_Islander_Alone;
        } else if (strcmp(field, "Ethnicities.Two or More Races") == 0) {
            percentage = information[i].Ethnicities_Two_or_More_Races;
        } else if (strcmp(field, "Ethnicities.White Alone") == 0) {
            percentage = information[i].Ethnicities_White_Alone;
        } else if (strcmp(field, "Ethnicities.White Alone, not Hispanic or Latino") == 0) {
            percentage = information[i].Ethnicities_White_Alone_not_Hispanic_or_Latino;  
        }else {
            fprintf(stderr, "Error: Unsupported field '%s'\n", field);
            return;
        }
        sub_pop += (int)(information[i].Population_2014_Population *(percentage/100.0));
    }
    printf("2014 %s population: %d\n", field, sub_pop);
}
//gives the percentage by field
void percent(Info *information, int *count, char *field){
    int total_pop = 0;
    int sub_pop = 0;
    for(int i = 0; i < *count; i++){
        total_pop += information[i].Population_2014_Population;
        float percentage;
        if (strcmp(field, "Education.High School or Higher") == 0) {
            percentage = information[i].Education_High_School_or_Higher;
        } else if (strcmp(field, "Education.Bachelor's Degree or Higher") == 0) {
            percentage = information[i].Education_Bachelors_Degree_or_Higher;
        } else if (strcmp(field, "Income.Persons Below Poverty Level") == 0) {
            percentage = information[i].Income_Persons_Below_Poverty_Level;
        } else if (strcmp(field, "Ethnicities.American Indian and Alaska Native Alone") == 0) {
            percentage = information[i].Ethnicities_American_Indian_and_Alaska_Native_Alone;
        } else if (strcmp(field, "Ethnicities.Asian Alone") == 0) {
            percentage = information[i].Ethnicities_Asian_Alone;
        } else if (strcmp(field, "Ethnicities.Black Alone") == 0) {
            percentage = information[i].Ethnicities_Black_Alone;
        } else if (strcmp(field, "Ethnicities.Hispanic or Latino") == 0) {
            percentage = information[i].Ethnicities_Hispanic_or_Latino;
        } else if (strcmp(field, "Ethnicities.Native Hawaiian and Other Pacific Islander Alone") == 0) {
            percentage = information[i].Ethnicities_Native_Hawaiian_and_Other_Pacific_Islander_Alone;
        } else if (strcmp(field, "Ethnicities.Two or More Races") == 0) {
            percentage = information[i].Ethnicities_Two_or_More_Races;
        } else if (strcmp(field, "Ethnicities.White Alone") == 0) {
            percentage = information[i].Ethnicities_White_Alone;
        } else if (strcmp(field, "Ethnicities.White Alone, not Hispanic or Latino") == 0) {
            percentage = information[i].Ethnicities_White_Alone_not_Hispanic_or_Latino;  
        }else {
            fprintf(stderr, "Error: Unsupported field '%s'\n", field);
            return;
        }
        sub_pop += (int)(information[i].Population_2014_Population *(percentage/100.0));
    }
    float result;
    if(total_pop > 0){
        result = (100.0 * sub_pop) / total_pop;
    }else{
        result = 0.0;
    }
    printf("2014 %s percentage: %.2f%%\n", field, result);
}
// executes what is in the .ops
int execute_operation(char *line, Info *information, int *count){
    char *function_wanted = strtok(line, ":\n");
    if (!function_wanted) {
    fprintf(stderr, "Malformed line: no function specified\n");
    return -1;
    }
    if(strcmp(function_wanted,"population-total")== 0){
        population_total(information, *count);
    }else if(strcmp(function_wanted, "filter-state") == 0){
        char *state_wanted = strtok(NULL, "\n");
        filter_state(information, count, state_wanted);
    }else if(strcmp(function_wanted, "filter") == 0){
        char *field_wanted = strtok(NULL, ":");
        char *ge_or_le = strtok(NULL, ":");
        float number = atof(strtok(NULL,"\n"));
        filter_field(information, count, field_wanted, ge_or_le, number);
    }else if(strcmp(function_wanted, "percent") == 0){
        char *field_wanted = strtok(NULL, "\n");
        percent(information, count, field_wanted);
    }else if(strcmp(function_wanted, "population") == 0){
        char *field_wanted = strtok(NULL, "\n");
        population_field(information, count, field_wanted);
    }else if(strcmp(function_wanted, "display") == 0){
        display_counties(information, count);
    }else{
        fprintf(stderr, "malformed line");
        return -1;
    }
    return 0;
}

// load file of  .ops
int process_operations(char *filename, Info *information, int *count){
    FILE *file = fopen(filename, "r");
    if(!file){
        perror("Error opening file");
        return -1;
    }
    char line[256];
    while(fgets(line, sizeof(line), file)){
        if(strlen(line) == 0 || line[0] == '\n'){
            continue;
        }
        if(execute_operation(line, information, count) == -1){
            printf("Error: malformed operation: %s\n", line);
            continue;
        }
    }
    fclose(file);
    return 0;
}

int main(int argc, char* argv[]){
    if(argc != 3){
        perror("Error: not enough arguments\n");
        return 1;
    }
    Info *information = NULL;
    int count = load_data(argv[1], &information);

    if(count == -1){
        perror("Error: fail to load data\n");
        return 1;
    }
    printf("Loaded %d entries.\n", count);

    if(process_operations(argv[2], information, &count)){
        perror("Error: failed to process operations\n");
        free(information);
        return 1;
    }
    free(information);
    return 0;

}


