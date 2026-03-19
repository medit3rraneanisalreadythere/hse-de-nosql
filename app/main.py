from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def add_student():
    doc = {
        "student_id": input("student_id: ").strip(),
        "full_name": input("full_name: ").strip(),
        "group": input("group: ").strip(),
        "faculty": input("faculty: ").strip(),
        "enrollment_year": int(input("enrollment_year: ").strip()),
        "email": input("email: ").strip(),
        "birth_date": input("birth_date (YYYY-MM-DD): ").strip()
    }
    db.students.insert_one(doc)
    print("OK")

def add_teacher():
    doc = {
        "teacher_id": input("teacher_id: ").strip(),
        "full_name": input("full_name: ").strip(),
        "department": input("department: ").strip(),
        "email": input("email: ").strip(),
        "position": input("position: ").strip()
    }
    db.teachers.insert_one(doc)
    print("OK")

def add_course():
    doc = {
        "course_code": input("course_code: ").strip(),
        "title": input("title: ").strip(),
        "department": input("department: ").strip(),
        "credits": int(input("credits: ").strip()),
        "hours": int(input("hours: ").strip())
    }
    db.courses.insert_one(doc)
    print("OK")

def enroll_student():
    doc = {
        "student_id": input("student_id: ").strip(),
        "course_code": input("course_code: ").strip(),
        "semester": input("semester: ").strip(),
        "teacher_id": input("teacher_id: ").strip(),
        "enrolled_at": datetime.utcnow(),
        "status": "active"
    }
    db.enrollments.insert_one(doc)
    print("OK")

def add_grade():
    doc = {
        "student_id": input("student_id: ").strip(),
        "course_code": input("course_code: ").strip(),
        "semester": input("semester: ").strip(),
        "teacher_id": input("teacher_id: ").strip(),
        "assessment_type": input("assessment_type: ").strip(),
        "score": int(input("score: ").strip()),
        "graded_at": datetime.utcnow()
    }
    db.grades.insert_one(doc)
    print("OK")

def show_student_grades():
    student_id = input("student_id: ").strip()
    docs = db.grades.find({"student_id": student_id}, {"_id": 0}).limit(30)
    found = False
    for doc in docs:
        print(doc)
        found = True
    if not found:
        print("No data")

def show_student_grades_by_semester():
    student_id = input("student_id: ").strip()
    semester = input("semester: ").strip()
    docs = db.grades.find({"student_id": student_id, "semester": semester}, {"_id": 0}).limit(30)
    found = False
    for doc in docs:
        print(doc)
        found = True
    if not found:
        print("No data")

def show_avg_score():
    student_id = input("student_id: ").strip()
    semester = input("semester: ").strip()
    pipeline = [
        {"$match": {"student_id": student_id, "semester": semester}},
        {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
    ]
    result = list(db.grades.aggregate(pipeline))
    if result:
        print(round(result[0]["avg_score"], 2))
    else:
        print("No data")

def show_course_students():
    course_code = input("course_code: ").strip()
    docs = db.enrollments.find({"course_code": course_code}, {"_id": 0}).limit(30)
    found = False
    for doc in docs:
        print(doc)
        found = True
    if not found:
        print("No data")

def show_teacher_grades():
    teacher_id = input("teacher_id: ").strip()
    docs = db.grades.find({"teacher_id": teacher_id}, {"_id": 0}).limit(30)
    found = False
    for doc in docs:
        print(doc)
        found = True
    if not found:
        print("No data")

def menu():
    while True:
        print("\n=== MENU ===")
        print("1. Add student")
        print("2. Add teacher")
        print("3. Add course")
        print("4. Enroll student")
        print("5. Add grade")
        print("6. Show student grades")
        print("7. Show student grades by semester")
        print("8. Show average score by semester")
        print("9. Show course students")
        print("10. Show teacher grades")
        print("0. Exit")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                add_teacher()
            elif choice == "3":
                add_course()
            elif choice == "4":
                enroll_student()
            elif choice == "5":
                add_grade()
            elif choice == "6":
                show_student_grades()
            elif choice == "7":
                show_student_grades_by_semester()
            elif choice == "8":
                show_avg_score()
            elif choice == "9":
                show_course_students()
            elif choice == "10":
                show_teacher_grades()
            elif choice == "0":
                break
            else:
                print("Wrong menu item")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    menu()