# HỌC PHẦN: VẬN HÀNH VÀ BẢO TRÌ PHẦN MỀM (DEVOPS)

**Kho lưu trữ các bài thực hành DevOps — Trường Đại học Công nghệ Thông tin & Truyền thông (ICTU)**

---

## 👨‍🎓 Thông tin sinh viên
- **Họ và tên:** NGUYỄN VĂN NAM
- **Mã số sinh viên (MSSV):** DTC235180129
- **Lớp:** K22
- **Email:** dtc235180129@ictu.edu.vn
- **Trường:** Trường Đại học Công nghệ Thông tin & Truyền thông - Đại học Thái Nguyên (ICTU)
- **GitHub:** [https://github.com/namddc](https://github.com/namddc)
- **Website Portfolio:** [https://namddc.github.io/devops-lab1/](https://namddc.github.io/devops-lab1/)

---

## 📂 Danh mục các bài thực hành (Labs)

| Thư mục | Tên bài thực hành | Công nghệ / Kỹ thuật | Trạng thái |
| :--- | :--- | :--- | :---: |
| [📁 **lab1/**](./lab1/) | **CI/CD Pipeline & GitHub Pages** | GitHub Actions, YAML, Lighthouse CI, GitHub Pages | ✅ Hoàn thành |
| [📁 **lab4/**](./lab4/) | **Quản lý Cấu hình Hạ tầng (Configuration Management)** | Ansible, YAML, Jinja2 Templates, Docker SSH Nodes, Idempotency | ✅ Hoàn thành |
| [📁 **lab5/**](./lab5/) | **Quản lý Mã nguồn với Git Flow & Code Review** | Git Flow, Feature Branching, Pull Request, Merge Conflict, Python | ✅ Hoàn thành |
| [📁 **lab6/**](./lab6/) | **Kiểm thử & Phân tích Mã nguồn Tĩnh trong DevOps** | Node.js Express, Postman/Newman, OWASP ZAP (DAST), SonarQube (SAST), CI Automation | ✅ Hoàn thành |

---

### Chi tiết từng bài thực hành:

### 1. [Lab 1 — CI/CD Pipeline với GitHub Actions & GitHub Pages](./lab1/)
- Xây dựng workflow tự động kiểm thử HTML, audit chất lượng với Google Lighthouse CI.
- Tự động xuất bản website cá nhân lên GitHub Pages tại nhánh `gh-pages`.
- Minh chứng đầy đủ quy trình qua 5 ảnh chụp màn hình trong `lab1/screenshots/`.

### 2. [Lab 4 — Quản lý Cấu hình Hạ tầng với Ansible](./lab4/)
- Thiết lập cụm máy chủ phân tán (Web Server, DB Server) bằng Docker SSH Managed Nodes.
- Viết Playbook cài đặt tự động Apache Web Server, phân phối template động Jinja2.
- Kiểm chứng tính bất biến và Idempotent (`changed=0`) khi thực thi lặp lại.
- Minh chứng đầy đủ qua 5 ảnh chụp màn hình trong `lab4/screenshots/`.

### 3. [Lab 5 — Quản lý Mã nguồn với Git Flow & Code Review](./lab5/)
- Triển khai ứng dụng quản lý sinh viên **Student Manager** bằng Python (`src/main.py`).
- Áp dụng mô hình nhánh **Git Flow**: `main`, `develop`, `feature/add-student`, `feature/search-student`.
- Quy trình Pull Request và Code Review chuẩn công nghiệp.
- Mô phỏng và giải quyết xung đột mã nguồn (Merge Conflict) trong `README.md`.
- Minh chứng đầy đủ qua 8 ảnh chụp màn hình trong `lab5/screenshots/`.

### 4. [Lab 6 — Kiểm thử & Phân tích Mã nguồn Tĩnh trong DevOps](./lab6/)
- Xây dựng REST API sinh viên bằng Node.js Express với các endpoint chuẩn và điểm mô phỏng an ninh.
- Kiểm thử chức năng API với Postman & Newman CLI tự động (12 assertions pass 100%).
- Quét lỗ hổng bảo mật động DAST với OWASP ZAP (phát hiện XSS, thiếu CSP, Header an ninh).
- Phân tích mã nguồn tĩnh SAST với SonarQube & SonarScanner (Bugs, Code Smells, Hotspots).
- Tích hợp tự động hóa qua kịch bản CI Pipeline (`ci-test.ps1` / `ci-test.sh`).
- Minh chứng đầy đủ qua 5 ảnh chụp màn hình trong `lab6/screenshots/`.

---

## 🚀 Hướng dẫn chạy thử nghiệm nhanh (Quick Start)

### Chạy ứng dụng Lab 5:
```bash
cd lab5
python src/main.py
```

### Chạy kịch bản Ansible Lab 4:
```bash
cd lab4
ansible all -m ping
ansible-playbook playbook-webserver.yml
```

---
*© 2026 Nguyễn Văn Nam — Khoa Công nghệ Thông tin, ICTU*
