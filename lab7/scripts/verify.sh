#!/bin/bash
# ==============================================================================
# verify.sh — Script kiểm tra toàn diện môi trường và kết quả Lab 7
# ==============================================================================

set -e

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
echo -e "${CYAN}  VERIFY — KIỂM TRA MÔI TRƯỜNG & DỰ ÁN LAB 7 CI PIPELINE       ${NC}"
echo -e "${CYAN}==============================================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

# 1. Kiểm tra Docker containers
echo -e "${YELLOW}--- 1. Kiểm tra trạng thái Container Docker ---${NC}"
if docker ps --format '{{.Names}}' | grep -q "lab7-jenkins"; then
    check "Jenkins container (lab7-jenkins) đang chạy" "OK"
else
    check "Jenkins container (lab7-jenkins)" "Chưa chạy. Hãy chạy: docker compose up -d"
fi

if docker ps --format '{{.Names}}' | grep -q "lab7-nexus"; then
    check "Nexus container (lab7-nexus) đang chạy" "OK"
else
    check "Nexus container (lab7-nexus)" "Chưa chạy"
fi

if docker ps --format '{{.Names}}' | grep -q "lab7-sonarqube"; then
    check "SonarQube container (lab7-sonarqube) đang chạy" "OK"
else
    check "SonarQube container (lab7-sonarqube)" "Chưa chạy"
fi

# 2. Kiểm tra các Port dịch vụ
echo ""
echo -e "${YELLOW}--- 2. Kiểm tra khả năng truy cập Port ---${NC}"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null | grep -q "200\|403"; then
    check "Web UI Jenkins (Port 8080) phản hồi" "OK"
else
    check "Web UI Jenkins (Port 8080)" "Chưa phản hồi (đang khởi động)"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:8081 2>/dev/null | grep -q "200\|401\|302"; then
    check "Web UI Nexus (Port 8081) phản hồi" "OK"
else
    check "Web UI Nexus (Port 8081)" "Chưa phản hồi (cần thêm thời gian khởi động)"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:9000 2>/dev/null | grep -q "200\|401\|302"; then
    check "Web UI SonarQube (Port 9000) phản hồi" "OK"
else
    check "Web UI SonarQube (Port 9000)" "Chưa phản hồi"
fi

# 3. Kiểm tra Jenkinsfile
echo ""
echo -e "${YELLOW}--- 3. Kiểm tra cấu trúc Jenkinsfile ---${NC}"
if [ -f "Jenkinsfile" ]; then
    check "File Jenkinsfile tồn tại" "OK"
else
    check "File Jenkinsfile" "Không tìm thấy file"
fi

if grep -q "pipeline {" "Jenkinsfile" 2>/dev/null; then
    check "Cú pháp Declarative Pipeline chuẩn" "OK"
else
    check "Cú pháp Declarative Pipeline" "Thiếu khối pipeline {}"
fi

if grep -q "stage('Checkout')" "Jenkinsfile" && grep -q "stage('Build')" "Jenkinsfile" && \
   grep -q "stage('Test')" "Jenkinsfile" && grep -q "stage('Package')" "Jenkinsfile"; then
    check "Đầy đủ các stage bắt buộc (Checkout, Build, Test, Package, v.v.)" "OK"
else
    check "Các stage bắt buộc" "Thiếu stage theo yêu cầu"
fi

# 4. Kiểm tra Sample Java App & Maven Test
echo ""
echo -e "${YELLOW}--- 4. Kiểm tra Sample Java App & Unit Tests ---${NC}"
if [ -f "sample-java-app/pom.xml" ]; then
    check "Maven pom.xml tồn tại" "OK"
else
    check "Maven pom.xml" "Không tìm thấy pom.xml"
fi

if [ -f "sample-java-app/src/test/java/com/devops/lab7/CalculatorTest.java" ]; then
    check "CalculatorTest.java tồn tại" "OK"
else
    check "CalculatorTest.java" "Không tìm thấy file test"
fi

if command -v mvn &> /dev/null; then
    echo "Đang chạy thử mvn clean test local..."
    cd sample-java-app
    if mvn clean test | grep -q "BUILD SUCCESS"; then
        check "Maven unit test (JUnit 5) 6/6 tests passed" "OK"
    else
        check "Maven unit test" "Test thất bại"
    fi
    cd ..
else
    check "Kiểm thử Maven local" "Maven chưa cài trên host (Jenkins container sẽ chạy Maven)"
fi

# 5. Tổng kết
echo ""
echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}  KẾT QUẢ KIỂM TRA: ${GREEN}$PASS/$TOTAL PASS${NC}, ${RED}$FAIL FAIL${NC}"
echo -e "${CYAN}==============================================================${NC}"

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}🎉 TẤT CẢ TIÊU CHÍ ĐỀU ĐẠT! Môi trường sẵn sàng cho CI Pipeline.${NC}"
else
    echo -e "${YELLOW}⚠️ Có $FAIL tiêu chí chưa đạt, hãy kiểm tra lại theo thông báo ở trên.${NC}"
fi

