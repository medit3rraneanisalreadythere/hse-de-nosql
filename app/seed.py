from pymongo import MongoClient
from faker import Faker
from random import randint, choice, sample
from datetime import datetime, timedelta
from config import MONGO_URI, DB_NAME

fake = Faker("ru_RU")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

SEMESTERS = ["2024-fall", "2025-spring", "2025-fall"]
ASSESSMENTS = ["quiz", "midterm", "exam", "project"]
DEPARTMENTS = [
    "Computer Science",
    "Software Engineering",
    "Mathematics",
    "Physics",
    "Economics"
]

def reset_db():
    db.students.drop()
    db.teachers.drop()
    db.courses.drop()

    db.enrollments.delete_many({})
    db.grades.delete_many({})

def create_indexes():
    db.students.create_index([("student_id", 1)], unique=True)
    db.teachers.create_index([("teacher_id", 1)], unique=True)
    db.courses.create_index([("course_code", 1)], unique=True)

    db.enrollments.create_index([("student_id", 1), ("semester", 1)])
    db.enrollments.create_index([("course_code", 1), ("semester", 1)])
    db.enrollments.create_index([("teacher_id", 1), ("semester", 1)])

    db.grades.create_index([("student_id", 1), ("semester", 1)])
    db.grades.create_index([("course_code", 1), ("semester", 1)])
    db.grades.create_index([("teacher_id", 1), ("semester", 1)])
    db.grades.create_index([("student_id", 1), ("course_code", 1), ("semester", 1)])

def seed_students(n=1000):
    docs = []
    for i in range(1, n + 1):
        docs.append({
            "student_id": f"S{i}",
            "full_name": fake.name(),
            "group": f"PI-{randint(21,25)}-{randint(1,5)}",
            "faculty": "Faculty of Informatics",
            "enrollment_year": randint(2021, 2025),
            "email": f"student{i}@example.com",
            "birth_date": fake.date_of_birth(minimum_age=17, maximum_age=25).isoformat()
        })
    db.students.insert_many(docs)

def seed_teachers(n=100):
    docs = []
    for i in range(1, n + 1):
        docs.append({
            "teacher_id": f"T{i}",
            "full_name": fake.name(),
            "department": choice(DEPARTMENTS),
            "email": f"teacher{i}@example.com",
            "position": choice(["assistant", "lecturer", "senior lecturer", "associate professor", "professor"])
        })
    db.teachers.insert_many(docs)

def seed_courses(n=100):
    docs = []
    for i in range(1, n + 1):
        docs.append({
            "course_code": f"C{i}",
            "title": f"Course {i}",
            "department": choice(DEPARTMENTS),
            "credits": choice([3, 4, 5, 6]),
            "hours": choice([72, 108, 144, 180])
        })
    db.courses.insert_many(docs)

def seed_enrollments(n=10000):
    docs = []
    for _ in range(n):
        docs.append({
            "student_id": f"S{randint(1,1000)}",
            "course_code": f"C{randint(1,100)}",
            "semester": choice(SEMESTERS),
            "teacher_id": f"T{randint(1,100)}",
            "enrolled_at": datetime.utcnow() - timedelta(days=randint(1, 365)),
            "status": choice(["active", "completed"])
        })
    db.enrollments.insert_many(docs)

def seed_grades(n=50000):
    docs = []
    for _ in range(n):
        docs.append({
            "student_id": f"S{randint(1,1000)}",
            "course_code": f"C{randint(1,100)}",
            "semester": choice(SEMESTERS),
            "teacher_id": f"T{randint(1,100)}",
            "assessment_type": choice(ASSESSMENTS),
            "score": randint(50, 100),
            "graded_at": datetime.utcnow() - timedelta(days=randint(1, 365))
        })
    batch_size = 5000
    for i in range(0, len(docs), batch_size):
        db.grades.insert_many(docs[i:i+batch_size])

def main():
    print("Reset DB...")
    reset_db()

    print("Create indexes...")
    create_indexes()

    print("Seed students...")
    seed_students()

    print("Seed teachers...")
    seed_teachers()

    print("Seed courses...")
    seed_courses()

    print("Seed enrollments...")
    seed_enrollments()

    print("Seed grades...")
    seed_grades()

    print("Done")

if __name__ == "__main__":
    main()