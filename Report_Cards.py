# Date: November 8th, 2020
# Developed by: Hirad Soltani
# This code is developed to read 5 csv files from the command line argument,
# in regards to students course grades, and output the results in JSON

# Importing the necessary libraries
import pandas as pd
import numpy as np
import json
import sys

# The following file names are read from the command line argument
courses = pd.read_csv(sys.argv[1]) # Courses information
students = pd.read_csv(sys.argv[2]) # Students information
tests = pd.read_csv(sys.argv[3]) # Tests information
marks = pd.read_csv(sys.argv[4]) # Marks for each student for courses taken
output = str(sys.argv[5]) # Name of the output file, ex: myoutput.json

df = {} # The final list to be converted to JSON

#Checking if the sum of weights for each course is 100
sum_weight = tests.groupby('course_id').sum()
for row in range(1,sum_weight.shape[0]+1):
    if sum_weight["weight"][row] != 100:
        df["error"] = "invalid course weight"
        with open(output, 'w') as outfile:
            json.dump(df, outfile,indent = 4)
        sys.exit()

df["students"] = [] # Making the "students" key a list

# Running a for loop for each student id.
for student in range(1,marks["student_id"].nunique()+1):
    temp_student = {} # list of info (values) that goes to "students" key

    student_df = marks[marks["student_id"] == student] #list of marks per each student
    temp_student["id"] = int(student) # Ensuring the id is an integer
    temp_student["name"] = students[students["id"] == student]["name"].tolist()[0]

    # List of course ids taken by each student.
    temp_course = [] # Making a list

    #List of test ids taken by each student.
    test_lst = marks[marks["student_id"] == student]["test_id"].tolist()

    # Determining total courses taken
    for i in test_lst:
        temp_course.append(tests[tests["id"] == i]["course_id"].tolist())
    courses_lst = np.unique(temp_course)

    temp_student["courses"] = [] # making a list of values for "courses" key
    sum_course = 0 #This will be used for calculating total average of students

    for course in courses_lst:

        test_lst = [] #List of test ids for the courses taken by each student
        temp_course = {} #This dictionary will be appended to the "courses" key
        temp_course["id"] = int(course)
        temp_course["name"] = courses[courses["id"] == course]["name"].tolist()[0]
        temp_course["teacher"] = courses[courses["id"] == course]["teacher"].tolist()[0]
        temp_student["courses"].append(temp_course)

        #test ids for the courses taken by each student
        test_lst = tests[tests["course_id"] == course]["id"].tolist()

        mark_lst = [] #list of marks for each courses
        for test in test_lst:
            mark_lst.append(student_df[student_df["test_id"] == test]["mark"].tolist()[0])

        # weight ids for the courses taken by each student
        weight_lst = tests[tests["course_id"] == course]["weight"].tolist()
        products = [a * b for a, b in zip(mark_lst, weight_lst)]
        temp_course["courseAverage"] = float(sum(products)/100)

        sum_course = sum_course + temp_course["courseAverage"] # Used for averaging
    temp_student["totalAverage"] = float(round(sum_course/len(courses_lst),2))

    df["students"].append(temp_student)

# Writing the desired output file in JSON format
with open(output, 'w') as outfile:
    json.dump(df, outfile,indent = 4)
#print(df)
