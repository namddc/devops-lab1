# Lab 6: Kiểm thử & Phân tích Mã nguồn Tĩnh trong DevOps

**Học phần:** Vận hành và Bảo trì Phần mềm (DevOps)  
**Sinh viên thực hiện:** NGUYỄN VĂN NAM — MSSV: DTC235180129 — Lớp: K22  
**Repository:** [https://github.com/namddc/devops-lab1](https://github.com/namddc/devops-lab1)  

---

## 1. Giới thiệu Lab 6
Lab 6 thực hành việc tích hợp 3 loại kiểm thử cốt lõi trong quy trình CI/CD DevSecOps:
1. **Functional Testing (Kiểm thử chức năng API):** Postman & Newman CLI.
2. **DAST - Dynamic Application Security Testing (Kiểm thử an ninh động):** OWASP ZAP.
3. **SAST - Static Application Security Testing (Phân tích mã nguồn tĩnh):** SonarQube & SonarScanner.

---

## 2. Cấu trúc thư mục Lab 6

```
lab6/
├── server.js                        # Node.js + Express Sample Student API
├── package.json                     # Cấu hình dependencies (express, cors)
├── Student-API-Tests.json           # Postman Collection 5 requests kiểm thử
├── sonar-project.properties         # Cấu hình SonarQube phân tích tĩnh
├── ci-test.sh                       # CI Pipeline script (Linux/Bash/Codespaces)
├── ci-test.ps1                      # CI Pipeline script (Windows PowerShell)
├── newman-report.json               # Báo cáo kết quả kiểm thử Newman CLI (12 assertions pass)
├── zap-report.html                  # Báo cáo kết quả quét an ninh OWASP ZAP
├── ho_ten_mssv.txt                  # Thông tin sinh viên & báo cáo so sánh
├── README.md                        # Hướng dẫn chi tiết
└── screenshots/                     # Ảnh chụp minh chứng kết quả
    ├── 01-newman-pass.png           # Chạy Newman pass 5/5 requests, 12/12 assertions
    ├── 02-zap-alerts.png            # Các cảnh báo an ninh từ OWASP ZAP
    ├── 03-sonarqube-dashboard.png   # Dashboard tổng quan SonarQube
    ├── 04-sonarqube-issues.png      # Danh sách Bugs & Code Smells trên SonarQube
    └── 05-comparison-table.png      # Bảng tổng hợp so sánh 3 loại kiểm thử
```

---

## 3. Hướng dẫn chạy

### 3.1 Khởi động API Server
```bash
npm install
node server.js
```
API lắng nghe tại `http://localhost:3000/api/students`.

### 3.2 Chạy kiểm thử Newman CLI
```bash
newman run Student-API-Tests.json -r cli,json --reporter-json-export newman-report.json
```

### 3.3 Chạy SonarQube qua Docker (hoặc trên GitHub Codespaces)
```bash
docker run -d --name lab6-sonarqube -p 9000:9000 -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true sonarqube:lts-community
```
Chạy phân tích SAST:
```bash
npx sonar-scanner
```

### 3.4 Chạy toàn bộ Pipeline tự động
- **Trên Windows (PowerShell):**
  ```powershell
  .\ci-test.ps1
  ```
- **Trên Linux / Git Bash / GitHub Codespaces:**
  ```bash
  bash ci-test.sh
  ```

---

## 4. Bảng So sánh 3 Loại Kiểm thử

| Tiêu chí | Postman/Newman | OWASP ZAP | SonarQube |
|---|:---:|:---:|:---:|
| **Loại kiểm thử** | Functional Test | DAST (Dynamic Security) | SAST (Static Analysis) |
| **Chạy ứng dụng?** | ✅ Có | ✅ Có | ❌ Không |
| **Phát hiện gì?** | Sai logic, sai status code, response time | XSS, SQLi, thiếu Security Headers | Bugs cú pháp, Code Smells, Security Hotspots |
| **Cần source code?** | ❌ Không (chỉ cần API endpoint) | ❌ Không (chỉ cần URL web) | ✅ Có (cần mã nguồn) |
| **Giai đoạn CI** | Sau khi deploy | Sau khi deploy | Trước khi build (Shift-Left) |
| **Tự động hóa** | ✅ Newman CLI | ✅ ZAP REST API / CLI | ✅ SonarScanner |
