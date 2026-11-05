# DevOps Lab 4: Quản lý Cấu hình Hạ tầng với Ansible (Configuration Management)

- **Sinh viên thực hiện:** NGUYỄN VĂN NAM
- **Mã số sinh viên (MSSV):** DTC235180129
- **Lớp:** K22
- **Trường:** Đại học Công nghệ Thông tin & Truyền thông - ĐH Thái Nguyên (ICTU)

---

## 1. Mục tiêu bài thực hành
- Xây dựng hệ thống quản lý cấu hình tự động (Configuration Management) bằng Ansible.
- Quản trị cụm máy chủ phân tán (Web Servers, Database Servers) qua giao thức SSH không cần cài agent (Agentless).
- Viết kịch bản tự động hóa cài đặt Apache Web Server, phân phối file cấu hình và script kiểm tra sức khỏe hệ thống.
- Kiểm chứng tính bất biến và idempotent (`changed=0`) khi chạy lại playbook nhiều lần.

---

## 2. Cấu trúc thư mục Lab 4
```
lab4/
├── ansible.cfg                # Cấu hình Ansible Controller
├── inventory.ini              # Danh sách máy chủ phân theo nhóm [webservers], [dbservers]
├── playbook-webserver.yml     # Playbook cài đặt & cấu hình Apache Web Server
├── playbook-full.yml          # Playbook triển khai bộ giám sát & công cụ phát triển
├── demo-ansible-live.html     # Giao diện mô phỏng giám sát trực quan
├── setup-lab4.sh              # Script khởi tạo nhanh môi trường Docker Managed Nodes
├── ho_ten_mssv.txt            # Báo cáo chi tiết kết quả thực hành
├── templates/
│   └── index.html.j2          # Jinja2 template render thông số server động
└── screenshots/               # 5 ảnh minh chứng kết quả chạy thực tế
    ├── 01-ansible-ping.png
    ├── 02-adhoc-check.png
    ├── 03-playbook-webserver.png
    ├── 04-playbook-full.png
    └── 05-idempotent.png
```

---

## 3. Các lệnh chính để demo
```bash
# 1. Kiểm tra kết nối tới toàn bộ máy chủ (Ping pong test)
ansible all -m ping

# 2. Chạy kịch bản cài đặt Web Server
ansible-playbook playbook-webserver.yml

# 3. Kiểm chứng tính Idempotent (chạy lần 2 - trả về changed=0)
ansible-playbook playbook-webserver.yml
```
