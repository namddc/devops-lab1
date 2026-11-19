# Lab 7: Triển khai CI Pipeline với Jenkins, Maven, Nexus & SonarQube

**Học phần:** Vận hành và Bảo trì Phần mềm (DevOps)  
**Sinh viên thực hiện:** NGUYỄN VĂN NAM — MSSV: DTC235180129 — Lớp: K22  
**Khoa/Trường:** Khoa CNTT — Trường Đại học Công nghệ Thông tin & Truyền thông (ICTU)  
**Giảng viên phụ trách:** Cô Phạm Thương  
**Repository:** [https://github.com/namddc/devops-lab1](https://github.com/namddc/devops-lab1)  

---

## 1. Giới thiệu Lab 7
Bài thực hành **Lab 7** tập trung vào việc thiết kế, xây dựng và vận hành một quy trình **Tích hợp liên tục (Continuous Integration - CI)** hoàn chỉnh chuẩn doanh nghiệp, bao gồm:
1. **Source Code Management:** Quản lý mã nguồn Java và theo dõi thay đổi qua Git & GitHub.
2. **Build & Test Automation:** Tự động biên dịch mã nguồn và chạy kiểm thử đơn vị với **Maven** & **JUnit 5**.
3. **Static Application Security Testing (SAST):** Phân tích mã nguồn tĩnh với **SonarQube** để phát hiện sớm các Bugs, Lỗ hổng an ninh (Vulnerabilities) và Code Smells.
4. **Artifact Packaging & Storage:** Tự động đóng gói file `.jar` và phát hành lên kho lưu trữ **Nexus Repository Manager**.
5. **CI Orchestration:** Điều phối toàn bộ các giai đoạn tự động qua **Jenkins Declarative Pipeline**.

---

## 2. Kiến trúc CI Pipeline

```
                     ┌────────────────────────────────────────┐
                     │          GitHub Repository             │
                     │    (Mã nguồn Java & Jenkinsfile)       │
                     └───────────────────┬────────────────────┘
                                         │ (Webhook / Poll SCM)
                                         ▼
                     ┌────────────────────────────────────────┐
                     │           Jenkins CI Server            │
                     │      (Điều phối chu trình CI)          │
                     └───────────────────┬────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                ▼                                ▼
┌──────────────┐                 ┌──────────────┐                 ┌──────────────┐
│ Maven Build  │                 │  SonarQube   │                 │ Nexus Repo   │
│  & Test      │                 │ Static Scan  │                 │ Artifact     │
│ (Compile +   │                 │ (SAST Scan   │                 │ (Lưu trữ     │
│  JUnit 5)    │                 │  Code Smells)│                 │  file .jar)  │
└──────────────┘                 └──────────────┘                 └──────────────┘
```

### Các Stage trong Pipeline:
```
1. Checkout  ──▶  2. Build  ──▶  3. Test  ──▶  4. SonarQube Scan  ──▶  5. Package  ──▶  6. Publish Nexus
   (Git Pull)     (mvn compile)   (mvn test)      (SAST Analysis)     (mvn package)   (Upload to Nexus)
```

---

## 3. Cấu trúc thư mục Lab 7

```
lab7/
├── docker-compose.yml              # Cấu hình khởi chạy Jenkins + Nexus + SonarQube
├── Jenkinsfile                     # CI Declarative Pipeline (chuẩn 6 stages)
├── ho_ten_mssv.txt                 # Báo cáo kết quả và thông tin sinh viên
├── README.md                       # Hướng dẫn chi tiết triển khai
├── sample-java-app/                # Dự án Java Maven mẫu
│   ├── pom.xml                     # Cấu hình dependencies, JUnit 5, Sonar & Jar plugins
│   ├── Jenkinsfile                 # Bản sao Jenkinsfile
│   └── src/
│       ├── main/java/com/devops/lab7/
│       │   ├── Calculator.java     # Lớp nghiệp vụ toán học
│       │   └── Main.java           # Lớp chính khởi chạy ứng dụng
│       └── test/java/com/devops/lab7/
│           └── CalculatorTest.java # 6 Unit tests kiểm thử JUnit 5
├── scripts/
│   ├── setup-codespaces.sh         # Script 1-click khởi động stack trên Codespaces/Linux
│   ├── verify.sh                   # Script kiểm tra tự động các tiêu chí Lab 7
│   └── cleanup.sh                  # Script dọn dẹp containers và volumes
└── screenshots/                    # 8 Ảnh chụp minh chứng hoàn thành
    ├── 01-docker-ps.png            # Kết quả docker ps 3 containers running
    ├── 02-jenkins-dashboard.png    # Giao diện Jenkins Dashboard
    ├── 03-pipeline-stage-view.png  # Pipeline Stage View xanh toàn bộ 6 bước
    ├── 04-console-output.png       # Console Output báo BUILD SUCCESS
    ├── 05-test-results.png         # Kết quả 6/6 unit tests passed
    ├── 06-artifacts.png            # File .jar trong Artifacts của Jenkins
    ├── 07-nexus-artifact.png       # File .jar đã upload lên kho Nexus
    └── 08-sonarqube-dashboard.png  # Giao diện dự án quét trên SonarQube
```

---

## 4. Hướng dẫn Triển khai trên GitHub Codespaces (Khuyên dùng)

### Bước 1: Mở GitHub Codespaces
1. Mở repository [https://github.com/namddc/devops-lab1](https://github.com/namddc/devops-lab1).
2. Nhấn nút xanh **Code** → Chọn tab **Codespaces** → **Create codespace on main**.
3. Chờ môi trường Codespaces mở ra trong trình duyệt.

### Bước 2: Khởi động Hạ tầng Docker Stack
Tại terminal của Codespaces, di chuyển vào thư mục `lab7` và chạy script khởi động:
```bash
cd lab7
chmod +x scripts/*.sh
bash scripts/setup-codespaces.sh
```
Script sẽ tự động:
- Cấu hình bộ nhớ Elasticsearch cho SonarQube.
- Khởi động 3 container: `lab7-jenkins`, `lab7-nexus`, `lab7-sonarqube`.
- Trích xuất mật khẩu ban đầu của Jenkins và Nexus.
- Mở danh sách cổng được forward:
  - **Jenkins:** Cổng `8080`
  - **Nexus:** Cổng `8081`
  - **SonarQube:** Cổng `9000`

> 💡 **Mẹo:** Trên Codespaces, chọn tab **PORTS** ở thanh công cụ dưới, bấm vào biểu tượng quả cầu cạnh cổng 8080, 8081, 9000 để mở giao diện web trực tiếp.

### Bước 3: Cấu hình nhanh các Dịch vụ
1. **Jenkins (Port 8080):**
   - Dán mật khẩu `initialAdminPassword` được in từ script.
   - Chọn **Install suggested plugins**.
   - Tạo tài khoản quản trị: `admin` / `admin123`.
   - Vào **Manage Jenkins** → **Plugins** → Cài thêm: `Pipeline: Stage View`, `SonarQube Scanner`, `Config File Provider`.
   - Vào **Manage Jenkins** → **Tools** → Thêm Maven với tên `M3` (chọn version 3.9.x, tích "Install automatically").
2. **Nexus (Port 8081):**
   - Đăng nhập `admin` với mật khẩu ban đầu từ script.
   - Đổi mật khẩu thành `nexus123`, chọn **Enable anonymous access**.
   - Vào **Settings** (bánh răng) → **Repositories** → **Create repository** → Chọn **maven2 (hosted)** → Đặt tên `maven-snapshots` (hoặc `maven-releases`).
3. **SonarQube (Port 9000):**
   - Đăng nhập `admin` / `admin` và đổi mật khẩu mới.
   - Vào avatar góc trên bên phải → **My Account** → **Security** → Generate Token với tên `jenkins-token`.
4. **Cấu hình Credentials trong Jenkins:**
   - Vào **Manage Jenkins** → **Credentials** → **System** → **Global credentials**:
     - Thêm Secret text (ID: `sonarqube-token`): Dán token SonarQube vào.
     - Thêm Username with password (ID: `nexus-credentials`): user `admin` / pass `nexus123`.
   - Vào **Manage Jenkins** → **Managed files** → Thêm file Maven `settings.xml` (ID: `maven-settings-nexus`) chứa server ID `nexus`.

### Bước 4: Tạo Job và Thực thi CI Pipeline
1. Trong Jenkins, nhấn **New Item** → Đặt tên `DevOps-Lab7-CI-Pipeline` → Chọn **Pipeline** → Nhấn **OK**.
2. Cuộn xuống mục **Pipeline**:
   - **Definition:** `Pipeline script from SCM`
   - **SCM:** `Git`
   - **Repository URL:** `https://github.com/namddc/devops-lab1.git`
   - **Branch Specifier:** `*/main`
   - **Script Path:** `lab7/Jenkinsfile` (hoặc `Jenkinsfile`)
3. Lưu cấu hình và bấm **Build Now**.

### Bước 5: Kiểm tra và Thu thập Minh chứng
1. Quan sát **Pipeline Stage View** chạy qua 6 bước (đều xanh).
2. Vào **Test Result** xem 6/6 tests pass.
3. Vào **Build Artifacts** tải và xem file `.jar`.
4. Mở Nexus kiểm tra file `.jar` đã upload trong kho `maven-snapshots`.
5. Mở SonarQube xem báo cáo phân tích mã nguồn.

---

## 5. Danh sách 8 Ảnh Minh chứng Nộp bài (Screenshots)
Lưu vào thư mục `screenshots/`:
- `01-docker-ps.png`: Chụp kết quả lệnh `docker ps` hiển thị 3 container đang chạy.
- `02-jenkins-dashboard.png`: Chụp giao diện trang chủ Jenkins quản lý Job.
- `03-pipeline-stage-view.png`: Chụp bảng Stage View 6 bước đều xanh lá cây.
- `04-console-output.png`: Chụp log Console Output có dòng `BUILD SUCCESS` / `PIPELINE SUCCESS`.
- `05-test-results.png`: Chụp trang kết quả kiểm thử unit test 6/6 passed.
- `06-artifacts.png`: Chụp file `ci-demo-1.0.0-SNAPSHOT.jar` trong phần Artifacts của build.
- `07-nexus-artifact.png`: Chụp giao diện Nexus Browse thấy file jar trong repository.
- `08-sonarqube-dashboard.png`: Chụp giao diện SonarQube hiển thị dự án `devops-lab7`.

---

## 6. Đóng gói Nộp bài
Khi hoàn thành, xuất file nén theo đúng quy định:
```bash
zip -r Lab7_NguyenVanNam_DTC235180129.zip docker-compose.yml Jenkinsfile sample-java-app ho_ten_mssv.txt README.md screenshots
```
File nén **`Lab7_NguyenVanNam_DTC235180129.zip`** sẵn sàng nộp lên LMS.

