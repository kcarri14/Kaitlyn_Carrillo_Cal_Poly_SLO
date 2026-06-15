#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdint.h>
#include <float.h>

//struct to hold the info from the file
typedef struct {
    char student_lastname[100];
    char student_firstname[100];
    int grade;
    int classroom_number;
    int bus;
    float GPA;
    char teacher_lastname[100];
    char teacher_firstname[100];
} Info;
//parses the file and places the information into the struct

int parsing(char *line, Info *information){
    char buffer[4000];
    strcpy(buffer,line);

    //copy student last name into structure
    char *token= strtok(buffer, ",");
    if(!token){
        return -1;
    }
    strcpy(information->student_lastname, token);

    //copy student first name into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    strcpy(information->student_firstname, token);

    //copy grade into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    information->grade = atoi(token);

    //copy classroom number into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    information->classroom_number = atoi(token);

    //copy bus route into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    information->bus = atoi(token);

    //copy GPA into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    information->GPA = atof(token);

    //copy teacher last name into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    strcpy(information->teacher_lastname, token);

    //copy teacher first name into structure
    token= strtok(NULL, ",");
    if(!token){
        return -1;
    }
    strcpy(information->teacher_firstname, token); 

    return 0;

}
// loads data from file
int load_data(char *filename, Info **info){
    FILE *file = fopen(filename, "r");
    if(!file){
        perror("Error: can't open file\n");
        return -1;
    }
    char line[1024];
    int line_num = 0;
    int count = 0;
    int capacity = 3000;
//allocs memory so it can be used to hold the struct
    *info = malloc(capacity * sizeof(Info));
    if (!*info) {
        perror("Error allocating memory");
        fclose(file);
        return -1;
    }
    while(fgets(line, sizeof(line), file)){
        line_num++;
        Info information;
        if(parsing(line, &information) == -1){
            printf("Error: line entry is malformed %d\n", line_num);
            continue;
        }
//reallocs more memory if needed
        if (count == capacity) {
            capacity *= 2; // Double the capacity
            Info *temp = realloc(*info, capacity * sizeof(Info));
            if (!temp) {
                perror("Error: memory reallocation failed\n");
                free(*info);
                fclose(file);
                return -1;
            }
            *info = temp;
        }    
        (*info)[count++] = information;

    }
    fclose(file);
    return count;
}
//searches the bus route by last name
void student_bus(char *argument, Info *information, int *count){
    int found = 0;
    for(int i = 0; i < *count; i++){
        if(strcmp(information[i].student_lastname, argument)== 0){
            found = 1;
            printf("Student: %s, %s\n", information[i].student_lastname,information[i].student_firstname );
            printf("Bus Route: %d\n", information[i].bus);
        }
    }
    if(!found){
        printf("No Student found with this last name: %s\n", argument);
    }
}
//searches for information with the students last name
void student_search(char *argument, Info *information, int *count){
    int found = 0;
    if (argument) {
        size_t len = strlen(argument);
        if (len > 0 && argument[len - 1] == '\n') {
            argument[len - 1] = '\0';
        }
    }
    for(int i = 0; i < *count; i++){
        if(strcmp(information[i].student_lastname, argument)== 0){
            found = 1;
            printf("Student: %s, %s\n", information[i].student_lastname,information[i].student_firstname );
            printf("Grade: %d\n", information[i].grade);
            printf("Classroom: %d\n", information[i].classroom_number);
            printf("Teacher: %s, %s\n", information[i].teacher_lastname, information[i].teacher_firstname);
        }
    }
    if(!found){
        printf("No Student found with this last name: %s\n", argument);
    }
}
//searches the students that specific teacher has
void teacher_search(char *argument, Info *information, int *count){
    int found = 0;
    for(int i = 0; i < *count; i++){
        if(strcmp(information[i].teacher_lastname, argument)== 0){
            found = 1;
            printf("Student: %s, %s\n", information[i].student_lastname,information[i].student_firstname );
        }
    }
    if(!found){
        printf("No teacher found with this last name: %s\n", argument);
    }
}
//searches by grade who is in each grade
void grade(char *argument, Info *information, int *count){
    int found = 0;
    int grade = atoi(argument);
    for(int i = 0; i < *count; i++){
        if(information[i].grade == grade){
            found = 1;
            printf("Student: %s, %s\n", information[i].student_lastname,information[i].student_firstname );
        }
    }
    if(!found){
        printf("No Student found with grade: %s\n", argument);
    }
}
//searches by grade and finds either the highest or the lowest GPA 
void grade_gpa(char *argument, char *additional_info, Info *information, int *count){
    float target_gpa = 0.0;
    if(strcmp(additional_info, "H")== 0){
        target_gpa = FLT_MIN;
    }else{
        target_gpa = FLT_MAX;
    }
    Info *target_student = NULL;
    int grade = atoi(argument);
    for(int i = 0; i < *count; i++){
        if(information[i].grade == grade){
            if((strcmp(additional_info, "H")== 0 && information[i].GPA > target_gpa) || (strcmp(additional_info,"L") == 0 && information[i].GPA < target_gpa)){
                target_gpa = information[i].GPA;
                target_student = &information[i];
                
            }
        }
    }
    if(target_student != NULL){
        printf("Student: %s, %s\n", target_student->student_lastname ,target_student->student_firstname);
        printf("GPA: %.2f\n", target_student->GPA);
        printf("Bus Route: %d\n", target_student->bus);
        printf("Teacher: %s, %s\n", target_student->teacher_lastname, target_student->teacher_firstname);
    }
    
}
//searches the students who are on a specific bus route
void bus_search(char *argument, Info *information, int *count){
    int found = 0;
    int bus_route = atoi(argument);
    for(int i = 0; i < *count; i++){
        if(information[i].bus == bus_route){
            found = 1;
            printf("Student: %s, %s\n", information[i].student_lastname,information[i].student_firstname );
            printf("Grade: %d\n", information[i].grade);
            printf("Classroom: %d\n", information[i].classroom_number);
        }
    }
    if(!found){
        printf("No Student found with this last name: %s\n", argument);
    }
}
//searches by grade and gives the average gpa for that grade
void average_GPA(char *argument, Info *information, int *count){
    float average = 0.0;
    int count_average = 0;
    int grade = atoi(argument);
    for(int i = 0; i < *count; i++){
        if(information[i].grade == grade){
            average += information[i].GPA;
            count_average += 1;
        }
    }
    if(count_average == 0){
        printf("No students in this grade level\n");
    }else{
        float average_overall = average / count_average;
        printf("Grade: %d\n", grade);
        printf("Average GPA for grade %d: %.2f\n", grade, average_overall);
    }

}
//gives how many students are in each grade in the specified file
void info(Info *information, int *count){
    int students_0 = 0;
    int students_1 = 0;
    int students_2 = 0;
    int students_3 = 0;
    int students_4 = 0;
    int students_5 = 0;
    int students_6 = 0;
    for(int i = 0; i < *count; i++){
        if(information[i].grade == 0){
            students_0 += 1;
        }else if(information[i].grade == 1){
            students_1 += 1;
        }else if(information[i].grade == 2){
            students_2 += 1;
        }else if(information[i].grade == 3){
            students_3 += 1;
        }else if(information[i].grade == 4){
            students_4 += 1;
        }else if(information[i].grade == 5){
            students_5 += 1;
        }else if(information[i].grade == 6){
            students_6 += 1;
        }             
    }
    printf("Grade 0: %d\n", students_0);
    printf("Grade 1: %d\n", students_1);
    printf("Grade 2: %d\n", students_2);
    printf("Grade 3: %d\n", students_3);
    printf("Grade 4: %d\n", students_4);
    printf("Grade 5: %d\n", students_5);
    printf("Grade 6: %d\n", students_6);
    
}


int main(int argc, char* argv[]){
    if(argc != 2){
        perror("Error: not enough arguments\n");
        return 1;
    }
    Info *information = NULL;
    int count = load_data(argv[1], &information);
    if(count == -1){
        perror("Error: fail to load data\n");
        return -1;
    }
//used to keep the command control running until the user would like to exit 
    while(1){
	printf("--------------------------------------------------------------\n");
	printf("Commands that could be used: \n");
        printf("WHEN INPUTTING LASTNAMES MAKE SURE THEY ARE IN ALL UPPERCASE\n");
        printf("--------------------------------------------------------------\n");
        printf("S: <student lastname>\n");
        printf("S: <student lastname> [B]\n");
        printf("T: <teacher lastname>\n");
        printf("G: <grade number>\n");
        printf("B: <bus route number>\n");
        printf("G: <grade number> [H]\n");
        printf("G: <grade number> [L]\n");
        printf("A: <grade number>\n");
        printf("I\n");
        printf("Q\n");
        printf("--------------------------------------------------------------\n");
        printf("Enter Command: ");
        char input[100];
        fgets(input, sizeof(input), stdin);

        size_t len = strlen(input);
        if (len > 0 && input[len - 1] == '\n') {
            input[len - 1] = '\0';
        }

        char *command;
        char *argument;
        char *additional_info;

        command = strtok(input, ": ");
        argument = strtok(NULL, " ");
        additional_info = strtok(NULL, " []");

        if (strcmp(command, "S") == 0 && additional_info != NULL){
            student_bus(argument, information, &count);
        }else if(strcmp(command, "S") == 0 && additional_info == NULL){
            student_search(argument, information, &count);
        }else if(strcmp(command, "T") == 0){
            teacher_search(argument, information, &count);
        }else if(strcmp(command, "G") == 0 && additional_info != NULL){
            grade_gpa(argument, additional_info, information, &count);
        }else if(strcmp(command, "G") == 0 && additional_info == NULL){
            grade(argument, information, &count);
        }else if(strcmp(command, "B") == 0){
            bus_search(argument, information, &count);
        }else if(strcmp(command, "A") == 0){
            average_GPA(argument, information, &count);
        }else if(strcmp(command, "I") == 0){
            info(information, &count);
        }else if(strcmp(command, "Q") == 0){
            free(information);
            break;
        }else{
            printf("Error: invalid command");
            continue;
        }
    }
    
    return 0;

}
