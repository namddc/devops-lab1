#!/bin/bash
# ==============================================================================
# verify.sh — Script kiểm tra toàn diện tiêu chí chấm điểm Lab 8
# ==============================================================================

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PASS=0
FAIL=0
TOTAL=0

check() {
    TOTAL=$((TOTAL + 1))
    echo -n "[$TOTAL] $1 ... "
    if [ "$2" = "OK" ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}❌ $2${NC}"
        FAIL=$((FAIL + 1))
    fi
}

echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}  VERIFY — KIỂM TRA MÔI TRƯỜNG & KẾT QUẢ LAB 8 CD PIPELINE     ${NC}"
echo -e "${CYAN}==============================================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

# 1. Docker running
if docker info &>/dev/null; then
    check "Docker daemon đang hoạt động" "OK"
else
    check "Docker daemon" "Chưa chạy"
fi

if docker compose version &>/dev/null; then
    check "Docker Compose v2 có sẵn" "OK"
else
    check "Docker Compose" "Chưa cài đặt"
fi

# 2. Check files
[ -f "Dockerfile" ] && check "Dockerfile tồn tại" "OK" || check "Dockerfile" "Không tìm thấy"
[ -f "docker-compose.yml" ] && check "docker-compose.yml tồn tại" "OK" || check "docker-compose.yml" "Không tìm thấy"
[ -f "nginx.conf" ] && check "nginx.conf tồn tại" "OK" || check "nginx.conf" "Không tìm thấy"
[ -f "Jenkinsfile" ] && check "Jenkinsfile tồn tại" "OK" || check "Jenkinsfile" "Không tìm thấy"
[ -f "app/server.js" ] && check "app/server.js tồn tại" "OK" || check "app/server.js" "Không tìm thấy"

# 3. Check Docker image
if docker images --format '{{.Repository}}' 2>/dev/null | grep -q "devops-lab8-app"; then
    check "Docker image devops-lab8-app đã được build" "OK"
else
    check "Docker image" "Chưa build image devops-lab8-app"
fi

# 4. Check Containers running
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "lab8-app"; then
    check "Container lab8-app đang chạy" "OK"
else
    check "Container lab8-app" "Chưa chạy. Gõ: docker compose up -d"
fi

if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "lab8-redis"; then
    check "Container lab8-redis đang chạy" "OK"
else
    check "Container lab8-redis" "Chưa chạy"
fi

if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "lab8-nginx"; then
    check "Container lab8-nginx đang chạy" "OK"
else
    check "Container lab8-nginx" "Chưa chạy"
fi

# 5. Check Ports & HTTP response
if curl -s -f http://localhost:3000/health &>/dev/null; then
    check "App HTTP Healthcheck (:3000/health) phản hồi OK" "OK"
else
    check "App HTTP Healthcheck" "Không phản hồi trên port 3000"
fi

if curl -s -f http://localhost:80/health &>/dev/null; then
    check "Nginx Reverse Proxy (:80/health) chuyển tiếp thành công" "OK"
else
    check "Nginx Reverse Proxy" "Không phản hồi trên port 80"
fi

# 6. Summary
echo ""
echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}  KẾT QUẢ KIỂM TRA: ${GREEN}$PASS/$TOTAL PASS${NC}, ${RED}$FAIL FAIL${NC}"
echo -e "${CYAN}==============================================================${NC}"

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}🎉 TẤT CẢ TIÊU CHÍ ĐỀU ĐẠT! Sẵn sàng demo hoặc nộp bài.${NC}"
else
    echo -e "${YELLOW}⚠️ Có $FAIL tiêu chí cần hoàn thiện thêm.${NC}"
fi
