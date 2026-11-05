# DevOps Lab 1: Xây dựng CI/CD Pipeline với GitHub Actions & GitHub Pages

- **Sinh viên thực hiện:** NGUYỄN VĂN NAM
- **Mã số sinh viên (MSSV):** DTC235180129
- **Lớp:** K22
- **Trường:** Đại học Công nghệ Thông tin & Truyền thông - ĐH Thái Nguyên (ICTU)
- **Website Live:** https://namddc.github.io/devops-lab1/

---

## 1. Mục tiêu bài thực hành
- Thiết lập quy trình tự động hóa tích hợp và triển khai liên tục (CI/CD) với GitHub Actions.
- Tự động kiểm tra chất lượng mã nguồn HTML & tài nguyên khi có commit mới.
- Tích hợp kiểm thử hiệu năng và chuẩn SEO với Google Lighthouse CI.
- Tự động xuất bản website cá nhân lên GitHub Pages qua nhánh `gh-pages`.

---

## 2. Cấu trúc thư mục Lab 1
```
lab1/
├── index.html            # Trang chủ Portfolio cá nhân
├── about.html            # Trang giới thiệu bản thân
├── contact.html          # Trang thông tin liên hệ
├── avatar.png            # Ảnh đại diện cá nhân
├── lighthouserc.json     # Cấu hình kiểm thử chuẩn Google Lighthouse CI
├── ho_ten_mssv.txt       # Báo cáo chi tiết kết quả thực hành
└── screenshots/          # 5 ảnh minh chứng quy trình CI/CD
    ├── 01-github-repo.png
    ├── 02-pipeline-running.png
    ├── 03-pipeline-success.png
    ├── 04-website-online.png
    └── 05-update-pipeline.png
```
