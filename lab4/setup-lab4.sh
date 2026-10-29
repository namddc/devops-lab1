#!/bin/bash
# ==============================================================================
# Script tự động khởi tạo môi trường Lab 4 trên GitHub Codespaces
# Sinh viên: NGUYỄN VĂN NAM - DTC235180129
# TÍCH HỢP BÀI TẬP MỞ RỘNG: JINJA2 TEMPLATE & HANDLERS
# ==============================================================================

set -e

echo "=========================================================="
echo "🚀 ĐANG KHỞI TẠO MÔI TRƯỜNG ANSIBLE LAB 4..."
echo "=========================================================="

# 1. Cài đặt Ansible nếu chưa có
if ! command -v ansible &> /dev/null; then
    echo "📦 Đang cài đặt Ansible..."
    pip install ansible
fi

# 2. Tạo Docker Network
echo "🌐 Đang tạo Docker Network 'ansible-lab'..."
docker network create ansible-lab 2>/dev/null || true

# 3. Dừng và xóa containers cũ nếu đã tồn tại
echo "🔄 Làm sạch các container cũ nếu có..."
docker rm -f web-server-1 web-server-2 db-server-1 2>/dev/null || true

# 4. Khởi chạy 3 container làm Managed Nodes
echo "🐳 Đang khởi chạy 3 container Ubuntu SSH (web-server-1, web-server-2, db-server-1)..."
docker run -d --name web-server-1 --privileged --network ansible-lab -p 2201:22 phamthuongdocker/ubuntu-sshd:22.04
docker run -d --name web-server-2 --privileged --network ansible-lab -p 2202:22 phamthuongdocker/ubuntu-sshd:22.04
docker run -d --name db-server-1  --privileged --network ansible-lab -p 2203:22 phamthuongdocker/ubuntu-sshd:22.04

# Chờ 3 giây cho sshd bên trong container sẵn sàng
echo "⏳ Chờ 3 giây để dịch vụ SSH khởi động..."
sleep 3

# 5. Kiểm tra danh sách container
echo ""
echo "✅ DANH SÁCH 3 MÁY CHỦ CONTAINER ĐÃ SẴN SÀNG:"
docker ps --filter "network=ansible-lab"

echo ""
echo "=========================================================="
echo "🎯 ĐANG TEST KẾT NỐI: ansible all -m ping"
echo "=========================================================="
ansible all -m ping

echo ""
echo "=========================================================="
echo "🎉 SETUP HOÀN TẤT! CÁC LỆNH ĐỂ BẠN SHOW CHO CÔ:"
echo "1. Chạy playbook Web (Jinja2 + Handler): ansible-playbook playbook-webserver.yml"
echo "2. Chạy lại lần 2 kiểm tra Idempotent:  ansible-playbook playbook-webserver.yml"
echo "3. Kiểm tra trang web render Jinja2:    docker exec web-server-1 curl -s http://localhost"
echo "4. Chạy full stack & health check:      ansible-playbook playbook-full.yml"
echo "=========================================================="
