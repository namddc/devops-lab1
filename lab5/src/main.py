"""
Student Manager — DevOps Lab 5
Module: Main Application
Dev A: Nguyen Van Nam (DTC235180129)
Dev B: Nguyen Manh Hung (DTC235200335)
"""
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from student import Student


def add_student(students: list, student_id: str, name: str, age: int, grade: str) -> list:
    """Thêm sinh viên mới vào danh sách (Feature phát triển bởi Dev A).

    Args:
        students: Danh sách sinh viên hiện tại
        student_id: Mã sinh viên
        name: Họ tên
        age: Tuổi
        grade: Khóa

    Returns:
        Danh sách sinh viên đã được cập nhật
    """
    for s in students:
        if s.student_id == student_id:
            print(f"❌ Mã sinh viên {student_id} đã tồn tại!")
            return students

    new_student = Student(student_id, name, age, grade)
    students.append(new_student)
    print(f"✅ Đã thêm sinh viên: {new_student}")
    return students


def search_student(students: list, keyword: str) -> list:
    """Tìm kiếm sinh viên theo tên hoặc mã sinh viên (Feature phát triển bởi Dev B - Nguyen Manh Hung).

    Args:
        students: Danh sách sinh viên
        keyword: Từ khóa tìm kiếm

    Returns:
        Danh sách sinh viên khớp với từ khóa
    """
    results = []
    keyword_lower = keyword.strip().lower()

    for s in students:
        if (keyword_lower in s.name.lower() or 
            keyword_lower in s.student_id.lower() or 
            keyword_lower in s.grade.lower()):
            results.append(s)

    if results:
        print(f"🔍 Tìm thấy {len(results)} sinh viên với từ khóa '{keyword}':")
        for s in results:
            print(f"  {s}")
    else:
        print(f"❌ Không tìm thấy sinh viên nào với từ khóa '{keyword}'")

    return results


def main():
    print("=" * 60)
    print("STUDENT MANAGER — DevOps Lab 5 (Git Flow Pair Programming)")
    print("Dev A: Nguyen Van Nam (DTC235180129) | Dev B: Nguyen Manh Hung (DTC235200335)")
    print("=" * 60)

    # 1. Danh sách ban đầu
    students = [
        Student("SV001", "Nguyen Van A", 20, "K20"),
        Student("SV002", "Tran Thi B", 21, "K20"),
        Student("SV003", "Le Van C", 19, "K21"),
    ]

    print("\n--- 1. Danh sách sinh viên ban đầu ---")
    for student in students:
        print(f"  {student}")
    print(f"Total: {len(students)} students")

    # 2. Thêm sinh viên (Dev A)
    print("\n--- 2. Thực hiện tính năng: Thêm sinh viên (Dev A) ---")
    students = add_student(students, "SV004", "Pham Thi D", 22, "K19")
    add_student(students, "SV001", "Nguyen Van A Duplicate", 20, "K20")

    print("\n--- 3. Danh sách sinh viên sau khi thêm ---")
    for student in students:
        print(f"  {student}")
    print(f"Total: {len(students)} students")

    # 3. Tìm kiếm sinh viên (Dev B - Nguyen Manh Hung)
    print("\n--- 4. Thực hiện tính năng: Tìm kiếm sinh viên (Dev B - Nguyen Manh Hung) ---")
    search_student(students, "Van")
    search_student(students, "SV004")
    search_student(students, "K20")
    search_student(students, "KhongTonTai")

    print("\n" + "=" * 60)
    print("✅ Hoàn thành quy trình chạy thử nghiệm Lab 5!")
    print("=" * 60)


if __name__ == "__main__":
    main()
