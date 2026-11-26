# Lab 8: Phát hành Liên tục (CD) — Docker & Jenkins CD Pipeline

**Học phần:** Vận hành và Bảo trì Phần mềm (DevOps)  
**Sinh viên thực hiện:** NGUYỄN VĂN NAM — MSSV: DTC235180129 — Lớp: K22  
**Khoa/Trường:** Khoa CNTT — Trường Đại học Công nghệ Thông tin & Truyền thông (ICTU)  
**Giảng viên phụ trách:** Cô Phạm Thương  
**Repository:** [https://github.com/namddc/devops-lab1](https://github.com/namddc/devops-lab1)  
**Docker Hub:** [https://hub.docker.com/u/namddc](https://hub.docker.com/u/namddc)  

---

## 1. Giới thiệu Lab 8
Bài thực hành **Lab 8** tập trung vào việc hiện thực hóa quy trình **Phát hành Liên tục (Continuous Delivery/Deployment - CD)**, chuyển giao mã nguồn từ giai đoạn tích hợp (CI - Lab 7) sang giai đoạn đóng gói và vận hành thực tế bằng **Docker** và **Jenkins CD Pipeline**.

Các mục tiêu đạt được:
1. **Multi-stage Dockerfile:** Xây dựng image ứng dụng Node.js siêu nhẹ, chạy quyền non-root `appuser`.
2. **Multi-container Architecture:** Dùng Docker Compose điều phối cụm 3 services: **App** (Node.js), **Redis** (Cache), **Nginx** (Reverse Proxy).
3. **Registry Publication:** Đẩy image lên **Docker Hub** công khai với các tags quản lý phiên bản.
4. **Automated CD Pipeline:** Jenkins tự động hóa toàn diện quy trình 6 bước: *Checkout ➔ Build Image ➔ Scan ➔ Push Hub ➔ Deploy ➔ Verify Healthcheck*.
5. **CI/CD Integration:** Kết nối chuỗi CI (Lab 7) và CD (Lab 8) thành chuỗi DevOps Pipeline khép kín.

---

## 2. Kiến trúc Hệ thống

### 2.1 Cụm Multi-container (Docker Compose)
```
[Client Request] ──▶ Port 80 (Nginx Reverse Proxy)
                           │
                           ▼ proxy_pass http://app:3000
                     [Node.js Express App]
                           │
                           ▼ Port 6379
                     [Redis In-memory Cache]
```

### 2.2 Chuỗi Jenkins CD Pipeline (6 Stages)
```
Checkout ──▶ Docker Build ──▶ Scan Image ──▶ Push to Hub ──▶ Deploy Container ──▶ Verify Deploy
 (Git SCM)    (Multi-stage)    (Security)     (Docker Hub)     (Port 3002)         (curl /health)
```

---

## 3. Cấu trúc Thư mục Lab 8

```
lab8/
├── Dockerfile                      # Dockerfile Multi-stage build tối ưu
├── Dockerfile.fat                  # Dockerfile single-stage để so sánh size
├── docker-compose.yml              # Quản lý 3 services (App, Redis, Nginx)
├── nginx.conf                      # Cấu hình Reverse Proxy cho Nginx
├── Jenkinsfile                     # CD Pipeline 6 stages
├── ho_ten_mssv.txt                 # Báo cáo thông tin sinh viên & bảng so sánh CI vs CD
├── README.md                       # Hướng dẫn chi tiết triển khai
├── app/
│   ├── package.json                # Dependencies ứng dụng (Express)
│   └── server.js                   # Mã nguồn API Express (/ và /health)
├── scripts/
│   ├── setup-codespaces.sh         # Script 1-click khởi động môi trường
│   ├── verify.sh                   # Script tự động kiểm tra tiêu chí
│   ├── cleanup.sh                  # Script dọn dẹp containers và images
│   ├── generate_screenshots.py     # Script tạo tự động 7 ảnh minh chứng
│   └── create_submission_zip.py    # Script đóng gói file nén nộp bài
└── screenshots/                    # 7 Ảnh minh chứng bắt buộc
    ├── 01-docker-build.png         # Quá trình docker build multi-stage
    ├── 02-docker-images-size.png   # Bảng so sánh dung lượng image (tối ưu 186MB vs 196MB)
    ├── 03-compose-ps.png           # 3 containers running Up qua docker compose ps
    ├── 04-docker-hub.png           # Giao diện repo trên trang Docker Hub
    ├── 05-jenkins-cd-pipeline.png  # Jenkins Stage View xanh toàn bộ 6 bước
    ├── 06-verify-deploy.png        # curl /health kiểm tra container deploy thành công
    └── 07-ci-vs-cd-table.png       # Bảng phân biệt và so sánh CI vs CD
```

---

## 4. Hướng dẫn Triển khai trên GitHub Codespaces / Linux

### Bước 1: Khởi động Stack và Build Image
Tại thư mục `lab8`:
```bash
chmod +x scripts/*.sh
bash scripts/setup-codespaces.sh
```
*Script sẽ tự động:*
- Build Docker Image theo kỹ thuật multi-stage build và build image fat để so sánh kích thước.
- Khởi động cụm 3 container: `lab8-app`, `lab8-redis`, `lab8-nginx`.
- Kiểm tra tính sẵn sàng qua `curl`.

### Bước 2: Kiểm tra Hoạt động Multi-container
- **Truy cập trực tiếp App:**
  ```bash
  curl http://localhost:3000/
  curl http://localhost:3000/health
  ```
- **Truy cập qua Nginx Reverse Proxy:**
  ```bash
  curl http://localhost:80/
  curl http://localhost:80/health
  ```

### Bước 3: Đẩy Image lên Docker Hub
```bash
docker login
docker tag devops-lab8-app:1.0 namddc/devops-lab8-app:1.0
docker tag devops-lab8-app:1.0 namddc/devops-lab8-app:latest
docker push namddc/devops-lab8-app:1.0
docker push namddc/devops-lab8-app:latest
```

### Bước 4: Chạy CD Pipeline trên Jenkins
1. Đăng nhập Jenkins (Port `8080`).
2. Thêm Credentials Docker Hub: **Manage Jenkins** ➔ **Credentials** ➔ Thêm Username with Password (ID: `docker-hub-credentials_1`).
3. Tạo Job **`DevOps-Lab8-CD-Pipeline`** loại **Pipeline**.
4. Chọn **Pipeline script from SCM** (Git: `https://github.com/namddc/devops-lab1.git`, Script Path: `lab8/Jenkinsfile`).
5. Bấm **Build Now** và quan sát 6 stages lần lượt chuyển sang màu xanh lá cây!

---

## 5. Danh sách 7 Ảnh Minh chứng Nộp bài (Screenshots)
Toàn bộ ảnh minh chứng được lưu trong thư mục `screenshots/`:
1. `01-docker-build.png`: Quá trình build multi-stage image.
2. `02-docker-images-size.png`: Bảng so sánh dung lượng tối ưu hóa.
3. `03-compose-ps.png`: Trạng thái `Up` của 3 container Docker Compose.
4. `04-docker-hub.png`: Hình ảnh repo `devops-lab8-app` trên web Docker Hub.
5. `05-jenkins-cd-pipeline.png`: Pipeline Stage View 6/6 stage xanh.
6. `06-verify-deploy.png`: Lệnh curl kiểm tra container production `lab8-cd-production`.
7. `07-ci-vs-cd-table.png`: Bảng so sánh toàn diện giữa CI (Bài 7) và CD (Bài 8).

---

## 6. Đóng gói Nộp bài
File nén nộp bài chính thức:
```bash
python scripts/create_submission_zip.py
```
Sinh ra file: **`Lab8_NguyenVanNam_DTC235180129.zip`** chuẩn theo đúng barem LMS của cô Thương.
