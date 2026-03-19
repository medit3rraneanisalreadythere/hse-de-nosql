import random
import time
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["university"]

SEMESTERS = ["2024-fall", "2025-spring", "2025-fall"]
ASSESSMENTS = ["quiz", "midterm", "exam", "project"]

def insert_grade(_):
    doc = {
        "student_id": f"S{random.randint(1, 1000)}",
        "course_code": f"C{random.randint(1, 100)}",
        "semester": random.choice(SEMESTERS),
        "teacher_id": f"T{random.randint(1, 100)}",
        "assessment_type": random.choice(ASSESSMENTS),
        "score": random.randint(50, 100),
        "graded_at": datetime.utcnow()
    }
    start = time.perf_counter()
    db.grades.insert_one(doc)
    return time.perf_counter() - start

def read_grades(_):
    student_id = f"S{random.randint(1, 1000)}"
    start = time.perf_counter()
    list(db.grades.find({"student_id": student_id}).limit(20))
    return time.perf_counter() - start

def mixed_op(_):
    if random.random() < 0.7:
        return read_grades(0)
    return insert_grade(0)

def percentile(values, p):
    values = sorted(values)
    idx = int(len(values) * p) - 1
    if idx < 0:
        idx = 0
    return values[idx]

def run_test(name, func, total_ops=5000, workers=50):
    latencies = []
    start_total = time.perf_counter()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(func, i) for i in range(total_ops)]
        for future in as_completed(futures):
            latencies.append(future.result())

    total_time = time.perf_counter() - start_total
    throughput = total_ops / total_time
    avg_latency = sum(latencies) / len(latencies)
    p95_latency = percentile(latencies, 0.95)

    return {
        "test": name,
        "total_ops": total_ops,
        "workers": workers,
        "total_time_sec": round(total_time, 4),
        "throughput_ops_sec": round(throughput, 2),
        "avg_latency_ms": round(avg_latency * 1000, 3),
        "p95_latency_ms": round(p95_latency * 1000, 3),
    }

def main():
    results = [
        run_test("insert-heavy", insert_grade),
        run_test("read-heavy", read_grades),
        run_test("mixed", mixed_op),
    ]

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for row in results:
        print(row)

if __name__ == "__main__":
    main()