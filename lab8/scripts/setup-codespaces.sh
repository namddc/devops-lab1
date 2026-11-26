#!/bin/bash
# ==============================================================================
# setup-codespaces.sh — Khởi động môi trường Lab 8 trên GitHub Codespaces / Linux
# Sinh viên: NGUYỄN VĂN NAM - MSSV: DTC235180129 - K22 - ICTU
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}  LAB 8: PHÁT HÀNH LIÊN TỤC (CD) — DOCKER & JENKINS CD PIPELINE ${NC}"
echo -e "${CYAN}  Môi trường: GitHub Codespaces / Ubuntu Linux                ${NC}"
echo -e "${CYAN}==============================================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

# 1. Kiểm tra Docker
echo -e "${YELLOW}[1/5] Kiểm tra Docker engine...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}LỖI: Docker chưa được cài đặt!${NC}"
    exit 1
fi
echo -e "${GREEN}Docker đã sẵn sàng: $(docker --version)${NC}"

# 2. Build Image Multi-stage và so sánh Image fat
echo -e "${YELLOW}[2/5] Build Docker Image tối ưu (Multi-stage build)...${NC}"
docker build -t devops-lab8-app:1.0 -t devops-lab8-app:latest .
docker build -t devops-lab8-app:fat -f Dockerfile.fat . 2>/dev/null || true

echo -e "${GREEN}So sánh kích thước hai Docker image:${NC}"
docker images devops-lab8-app

# 3. Khởi động cụm 3 container với Docker Compose
echo -e "${YELLOW}[3/5] Khởi động Docker Compose stack (App, Redis, Nginx)...${NC}"
docker compose up -d

echo -e "${YELLOW}[4/5] Đợi các dịch vụ khởi tạo (10 giây)...${NC}"
sleep 10

# 4. Kiểm tra sức khỏe của dịch vụ
echo -e "${YELLOW}[5/5] Kiểm tra phản hồi ứng dụng qua Nginx và trực tiếp...${NC}"
docker compose ps

echo ""
echo -e "Test trực tiếp cổng 3000 (App):"
curl -s http://localhost:3000/ || echo "App khởi động..."
echo ""
echo -e "Test qua cổng 80 (Nginx Reverse Proxy):"
curl -s http://localhost:80/ || echo "Nginx đang chuyển tiếp..."
echo ""

echo -e "${CYAN}==============================================================${NC}"
echo -e "${GREEN}               THÔNG TIN KẾT NỐI VÀ TRUY CẬP                  ${NC}"
echo -e "${CYAN}==============================================================${NC}"
echo -e "🔹 ${CYAN}1. NGINX REVERSE PROXY:${NC} Cổng 80  (Xem tab PORTS trên Codespaces)"
echo -e "🔹 ${CYAN}2. NODE.JS APP:        ${NC} Cổng 3000 (API trực tiếp)"
echo -e "🔹 ${CYAN}3. REDIS CACHE:        ${NC} Cổng 6379"
echo -e "🔹 ${CYAN}4. PRODUCTION DEPLOY:  ${NC} Cổng 3002 (Do Jenkins CD deploy)"
echo ""
echo -e "${GREEN}Chạy lệnh sau để kiểm tra trạng thái: bash scripts/verify.sh${NC}"
echo -e "${CYAN}==============================================================${NC}"
