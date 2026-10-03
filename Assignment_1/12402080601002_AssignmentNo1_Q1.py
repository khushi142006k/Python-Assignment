'''
Problem Statement: You are given records of students in the form enrollment, name, semester, CPI and a list of subject marks. Build a
program that stores the records using lists, tuples and dictionaries. For each semester, print the top K students by CPI. If CPI is the
same, prefer the student with higher average marks; if still tied, prefer lexicographically smaller enrollment number. Also print the
subject-wise topper for every subject code.
'''

n = int(input(" Enter No. of students: "))
k = int(input("Enter No. of Top Students Required: "))
m = int(input("Enter the no. of subjects:"))

students=[]

for i in range(n):
    enrollment = input("Enrollment: ")
    name = input("Name: ")
    semester = int(input("Semester: "))
    cpi = float(input("CPI: "))

    marks = []

    for j in range(m):
        mark = int(input(f"Enter marks of S{j+1}: "))
        marks.append(mark)

    average = sum(marks) / m

    student = {
        "enrollment": enrollment,
        "name": name,
        "semester": semester,
        "cpi": cpi,
        "marks": marks,
        "average": average
    }

    students.append(student)

semester_dict = {}

for student in students:
    sem = student["semester"]

    if sem not in semester_dict:
        semester_dict[sem] = []

    semester_dict[sem].append(student)

for sem in semester_dict:
    semester_dict[sem].sort(
        key=lambda x: (-x["cpi"], -x["average"], x["enrollment"])
    )

print("---- RESULTS ----")

for sem in sorted(semester_dict):
    print(f"Semester {sem}:", end=" ")

    for student in semester_dict[sem][:k]:
        print(student["enrollment"], end=" ")

    print()

# Find subject-wise toppers

for subject in range(m):

    highest = -1
    toppers = []

    for student in students:

        mark = student["marks"][subject]

        if mark > highest:
            highest = mark
            toppers = [student["enrollment"]]

        elif mark == highest:
            toppers.append(student["enrollment"])

    print(f"S{subject+1}:", end=" ")

    for enrollment in toppers:
        print(enrollment, end=" ")

    print()
