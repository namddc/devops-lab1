#!/bin/bash
# ==============================================================================
# setup-codespaces.sh — Khởi động môi trường Lab 7 trên GitHub Codespaces / Linux
# Sinh viên: NGUYỄN VĂN NAM - MSSV: DTC235180129 - K22 - ICTU
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}  LAB 7: CI PIPELINE VỚI JENKINS, MAVEN, NEXUS & SONARQUBE    ${NC}"
echo -e "${CYAN}  Môi trường: GitHub Codespaces / Ubuntu Linux                ${NC}"
echo -e "${CYAN}==============================================================${NC}"
echo ""

# 1. Cấu hình kernel cho SonarQube (Elasticsearch)
echo -e "${YELLOW}[1/5] Cấu hình bộ nhớ hệ thống cho SonarQube...${NC}"
sudo sysctl -w vm.max_map_count=262144 2>/dev/null || true

# 2. Kiểm tra Docker & Docker Compose
echo -e "${YELLOW}[2/5] Kiểm tra Docker engine...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}LỖI: Docker chưa được cài đặt!${NC}"
    exit 1
fi
echo -e "${GREEN}Docker đã sẵn sàng: $(docker --version)${NC}"

# 3. Khởi động các container qua Docker Compose
echo -e "${YELLOW}[3/5] Khởi động stack Jenkins + Nexus + SonarQube...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

docker compose up -d

# 4. Chờ các service khởi động
echo -e "${YELLOW}[4/5] Đang chờ các dịch vụ khởi động (khoảng 45 giây)...${NC}"
for i in {45..1}; do
    echo -ne "Đang đợi: $i giây...\r"
    sleep 1
done
echo -e "\n${GREEN}Hạ tầng container đã sẵn sàng!${NC}"

# 5. Lấy mật khẩu ban đầu
echo ""
echo -e "${CYAN}==============================================================${NC}"
echo -e "${GREEN}               THÔNG TIN KẾT NỐI VÀ ĐĂNG NHẬP                 ${NC}"
echo -e "${CYAN}==============================================================${NC}"

JENKINS_PASS=$(docker exec lab7-jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "Đang khởi tạo, hãy kiểm tra lại sau vài giây...")
NEXUS_PASS=$(docker exec lab7-nexus cat /nexus-data/admin.password 2>/dev/null || echo "Đang khởi tạo, hãy kiểm tra lại sau vài giây...")

echo -e "🔹 ${CYAN}1. JENKINS CI SERVER:${NC}"
echo -e "   - Cổng nội bộ: 8080 (Mở tab 'PORTS' trên Codespaces để click link)"
echo -e "   - Initial Admin Password: ${YELLOW}${JENKINS_PASS}${NC}"
echo -e "   - Hướng dẫn: Chọn 'Install suggested plugins' -> Tạo user admin/admin123"
echo ""
echo -e "🔹 ${CYAN}2. NEXUS REPOSITORY:${NC}"
echo -e "   - Cổng nội bộ: 8081 (Mở tab 'PORTS' trên Codespaces để click link)"
echo -e "   - Username: admin"
echo -e "   - Initial Admin Password: ${YELLOW}${NEXUS_PASS}${NC}"
echo -e "   - Hướng dẫn: Đổi pass thành 'nexus123' -> Bật Anonymous access -> Tạo repo 'maven-snapshots'"
echo ""
echo -e "🔹 ${CYAN}3. SONARQUBE SERVER:${NC}"
echo -e "   - Cổng nội bộ: 9000 (Mở tab 'PORTS' trên Codespaces để click link)"
echo -e "   - Username mặc định: admin"
echo -e "   - Password mặc định: admin (Đổi pass khi đăng nhập lần đầu)"
echo -e "   - Hướng dẫn: Vào My Account -> Security -> Tạo Token cho dự án"
echo ""
echo -e "${CYAN}==============================================================${NC}"
echo -e "${GREEN}Chạy lệnh sau để kiểm tra trạng thái: bash scripts/verify.sh${NC}"
echo -e "${CYAN}==============================================================${NC}"

