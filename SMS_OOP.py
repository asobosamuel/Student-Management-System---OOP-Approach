import jsonpickle
from csv import DictWriter


class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def set_name(self, new_name):
        self._name = new_name
        return self

    def get_name(self):
        return self._name

    def set_age(self, new_age):
        self._age = new_age
        return self

    def get_age(self):
        return self._age

    def calculate_age_in_months(self):
        return self._age * 12


class Student(Person):
    list_of_subjects = ['Biology', 'Chemistry', 'Physics', 'Mathematics', 'Further Maths', 'Comp. Sc']
    number_of_students = 0
    students = []

    def __init__(self, name, age, subjects=None):
        super().__init__(name=name, age=age)
        if subjects is None:
            subjects = {}
        self._subjects = subjects
        self._grade = None
        Student.number_of_students += 1
        Student.students.append(self)
        Student.save_to_file()

    def __repr__(self):
        return f"Name: {self._name}\t|\tAge: {self._age}\t|\tGrade: {self._grade}"

    def calculate_grade(self):
        self._grade = round(sum(self._subjects.values()) / len(self._subjects), 2)
        return self._grade

    def get_grade(self):
        return self._grade

    @classmethod
    def get_highest_grade(cls):
        return max(student.get_grade() for student in Student.students)

    @classmethod
    def get_lowest_grade(cls):
        return min(student.get_grade() for student in Student.students)

    @classmethod
    def get_average_grade(cls):
        average_grade = round(sum(student.get_grade() for student in Student.students) / Student.number_of_students, 2)
        return average_grade

    def display_info(self):
        print("Student name:", self._name)
        print("Subjects:", ', '.join(self._subjects.keys()))
        print("Grades:", ', '.join(str(value) for value in self._subjects.values()))
        print("Overall grade:", self._grade)
        print("Number of subjects passed:", self.num_of_subjects_passed())
        print("NUmber of subjects failed:", len(self._subjects) - self.num_of_subjects_passed())

    def num_of_subjects_passed(self):
        return len([score for score in self._subjects.values() if score >= 50])

    @classmethod
    def display_all_students(cls):
        for student_id, student in enumerate(cls.students):
            print("Student ID:", student_id, "\t|", student)

    @classmethod
    def add_student(cls):
        name = input("Enter name of Student: ")
        while True:
            try:
                age = int(input("Enter the age of student: "))
            except ValueError:
                print('Enter a number!!!')
            else:
                break

        subjects = dict.fromkeys(cls.list_of_subjects, None)
        print("\n...Creating new student...\n")
        return cls(name=name, age=age, subjects=subjects)

    @classmethod
    def update_student(cls):
        cls.display_all_students()
        while True:
            while True:
                try:
                    choice = int(input("Choose student you want to update by the student ID: "))
                except ValueError:
                    print('Enter a number!!!')
                else:
                    break

            if choice in range(Student.number_of_students):
                print(Student.students[choice])
                print("What info do you want to update")
                print("1. Name")
                print("2. Age")
                print("3. Name & Age")
                while True:
                    while True:
                        try:
                            option = int(input("Enter choice: "))
                        except ValueError:
                            print('Enter a number!!!')
                        else:
                            break

                    if option == 1:
                        new_name = input("Enter new name: ")
                        Student.students[choice].set_name(new_name=new_name)
                        print("...Name Updated Successfully...")
                        Student.save_to_file()
                        break
                    elif option == 2:
                        new_age = input("Enter new age: ")
                        Student.students[choice].set_age(new_age=new_age)
                        print("...Age Updated Successfully...")
                        Student.save_to_file()
                        break
                    elif option == 3:
                        new_name = input("Enter new name: ")
                        Student.students[choice].set_name(new_name=new_name)
                        new_age = input("Enter new age: ")
                        Student.students[choice].set_age(new_age=new_age)
                        print("...Name & Age Updated Successfully...")
                        Student.save_to_file()
                        break
                    print("Enter valid choice!!!")
                break
            print("Enter valid ID!!!")

    @classmethod
    def delete_student(cls):
        cls.display_all_students()
        while True:
            while True:
                try:
                    choice = int(input("Choose student you want to delete by the student ID: "))
                except ValueError:
                    print('Enter a number!!!')
                else:
                    break

            if choice in range(Student.number_of_students):
                del Student.students[choice]
                Student.number_of_students -= 1
                print("...Student Deleted Successfully...")
                Student.save_to_file()
                break
            print("Enter valid ID!!!")

    @classmethod
    def calculate_statistics(cls):
        print("Number of students:", cls.number_of_students)
        num_of_students_passed = len([student for student in Student.students if student.get_grade() >= 50])
        print("Number of students who passed:", num_of_students_passed)
        print("Number of students who failed:", Student.number_of_students - num_of_students_passed)
        print("Highest grade:", Student.get_highest_grade())
        print("Lowest grade:", Student.get_lowest_grade())
        print("Average grade:", Student.get_average_grade())
        for index, student in enumerate(Student.students):
            print()
            print(f"Student {index}:")
            print(f"Name: {student.get_name()}")
            print(f"Grade: {student.get_grade()}")
            subjects_passed = [subject for subject in student.get_subjects() if student.get_subjects()[subject] >= 50]
            print(', '.join(subjects_passed))

    def assign_grade(self, subject, score):
        self._subjects[subject] = score

    def get_subjects(self):
        return self._subjects

    @classmethod
    def save_to_file(cls):
        with open("students.json", "w") as file:
            data = jsonpickle.encode(Student.students)
            file.write(data)

    @classmethod
    def load_from_file(cls):
        with open("students.json", "r") as file:
            content = file.read()
            data = jsonpickle.decode(content)
            Student.students = data
            Student.number_of_students = len(data)

    @classmethod
    def generate_report(cls):
        with open("report.csv", 'w') as file:
            headers = ["name", "age", *Student.list_of_subjects, "grade"]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            for student in Student.students:
                info = {
                    "name": student.get_name(),
                    "age": student.get_age(),
                    "grade": student.get_grade()
                }
                for subject, score in student.get_subjects().items():
                    info[subject] = score
                csv_writer.writerow(info)


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name=name, age=age)
        self._subject = subject

    @staticmethod
    def assign_grade():
        Student.display_all_students()
        while True:
            while True:
                try:
                    choice = int(input("Choose student you want to enter score for: "))
                except ValueError:
                    print('Enter a number!!!')
                else:
                    break

            if choice in range(Student.number_of_students):
                print(Student.students[choice])
                for subject in Student.list_of_subjects:
                    while True:
                        try:
                            score = int(input(f"Enter {Student.students[choice].get_name()}'s mark for {subject} /100:"))
                        except ValueError:
                            print('Enter a number!!!')
                        else:
                            break

                    Student.students[choice].assign_grade(subject=subject, score=score)
                Student.students[choice].calculate_grade()
                Student.save_to_file()
                break
            print("Enter valid ID!!!")


class Menu:
    def display_menu(self):
        print("Welcome to the student management system...")
        while True:
            print("\nWhat do you want to do?")
            print("1.\tDISPLAY ALL STUDENTS...")
            print("2.\tDISPLAY STUDENT IN DETAIL...")
            print("3.\tADD STUDENT...")
            print("4.\tUPDATE EXISTING STUDENT INFO...")
            print("5.\tDELETE EXISTING STUDENT...")
            print("6.\tASSIGN GRADES OR SCORES...")
            print("7.\tCALCULATE AND DISPLAY STATISTICS...")
            print("8.\tSAVE CHANGES TO FILE...")
            print("9.\tGENERATE REPORT...")
            print("10.\tEXIT...")
            choice = self.get_choice()
            self.execute_action(choice=choice)

    @staticmethod
    def get_choice():
        while True:
            while True:
                try:
                    choice = int(input("Enter your choice: "))
                except ValueError:
                    print('Enter a number!!!')
                else:
                    break

            print("\n")
            if choice in range(1, 11):
                return choice
            print("choice out of range ( 1 - 10 )!!!!!")

    @staticmethod
    def execute_action(choice):
        if choice == 1:
            Student.display_all_students()
        elif choice == 2:
            Student.display_all_students()
            while True:
                while True:
                    try:
                        selected_student = int(input("Enter student ID to view in detail: "))
                    except ValueError:
                        print('Enter a number!!!')
                    else:
                        break

                if selected_student in range(Student.number_of_students):
                    Student.display_info(Student.students[selected_student])
                    break
                print("Enter a valid student ID!!!")
        elif choice == 3:
            Student.add_student()
        elif choice == 4:
            Student.update_student()
        elif choice == 5:
            Student.delete_student()
        elif choice == 6:
            teacher.assign_grade()
        elif choice == 7:
            Student.calculate_statistics()
        elif choice == 8:
            Student.save_to_file()
        elif choice == 9:
            Student.generate_report()
        else:
            Student.save_to_file()
            print("...EXITING...")
            exit()


Student.load_from_file()
teacher = Teacher("Andy", 24, "Biology")
menu = Menu()
menu.display_menu()
