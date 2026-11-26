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
| [📁 **lab7/**](./lab7/) | **Triển khai CI Pipeline với Jenkins, Maven, Nexus & SonarQube** | Jenkins Declarative Pipeline, Maven, JUnit 5, SonarQube SAST, Nexus Repository, Docker Compose | ✅ Hoàn thành |
| [📁 **lab8/**](./lab8/) | **Phát hành Liên tục (CD) với Docker & Jenkins CD Pipeline** | Docker Multi-stage, Docker Compose, Redis, Nginx, Docker Hub, Jenkins CD Pipeline | ✅ Hoàn thành |

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

### 5. [Lab 7 — Triển khai CI Pipeline với Jenkins, Maven, Nexus & SonarQube](./lab7/)
- Xây dựng chuỗi CI Pipeline tự động 6 giai đoạn (Checkout -> Build -> Test -> SonarQube -> Package -> Publish Nexus).
- Biên dịch và kiểm thử tự động ứng dụng Java Calculator với JUnit 5 (6/6 tests pass).
- Tích hợp phân tích mã tĩnh SonarQube SAST tự động phát hiện sớm Bugs, Code Smells, Hotspots.
- Đóng gói file .jar và đẩy artifact nhị phân lên kho lưu trữ Nexus Repository Manager.
- Minh chứng đầy đủ qua 8 ảnh chụp màn hình trong `lab7/screenshots/`.

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

### Khởi chạy môi trường Lab 7 (Jenkins, Nexus, SonarQube):
```bash
cd lab7
docker-compose up -d
```

---
*© 2026 Nguyễn Văn Nam — Khoa Công nghệ Thông tin, ICTU*


### 6. [Lab 8 — Phát hành Liên tục (CD) với Docker & Jenkins CD Pipeline](./lab8/)
- Xây dựng Dockerfile tối ưu hóa với kỹ thuật Multi-stage build và phân quyền non-root user (appuser).
- Quản trị ứng dụng đa dịch vụ bằng Docker Compose: Node.js App (port 3000), Redis Cache (port 6379), Nginx Reverse Proxy (port 80).
- Đẩy Docker image lên kho lưu trữ Docker Hub Registry công khai (namddc/devops-lab8-app:1.0 & latest).
- Xây dựng Jenkins CD Pipeline tự động hóa 6 giai đoạn (Checkout -> Build -> Scan -> Push -> Deploy -> Verify Healthcheck).
- Lập bảng so sánh và phân tích toàn diện chu trình liên kết CI (Bài 7) sang CD (Bài 8).
- Minh chứng đầy đủ qua 7 ảnh chụp màn hình trong lab8/screenshots/.
