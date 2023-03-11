# course_names = [
#     "Communicative English",
#     "Readings on Kerala",
#     "Sahithya Ganangal",
#     "Introduction to C Programming",
#     "Mathematics for Computer Science I",
#     "Basic Statistics"
# ]

def course_names(sem):
    if sem == 1:
        return [
        "Communicative English",
        "Readings on Kerala",
        "Sahithya Ganangal",
        "Introduction to C Programming",
        "Mathematics for Computer Science I",
        "Basic Statistics"
        ]
    elif sem == 2:
        return ['Readings On Life and Nature', 'Readings On Gender', 'Gadya Mathrikakal', 'Advanced C Programming', 'Lab I: C Programming', 'Mathematics for Computer Science II', 'Probability Theory And Random']
    elif sem == 4:
        return ['Digital Electronics','Operating Systems','Software Engineering','LabII: Data Structures Using C++','Lab III: Database Managenent System','Mathematics for Computer Science IV','Statistical Inference']
    elif sem == 5:
        return ['Web Technology','Java Programming','Computation Using Python','Algorithm Designing','Quantitative Arithmetic and Reasoning']