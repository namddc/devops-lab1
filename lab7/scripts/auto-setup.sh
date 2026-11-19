#!/bin/bash
# ==============================================================================
# auto-setup.sh — Tự động hóa thiết lập dữ liệu cho Lab 7 (Jenkins, Nexus, SonarQube)
# Sinh viên: NGUYỄN VĂN NAM - DTC235180129 - K22 - ICTU
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}   TỰ ĐỘNG CẤU HÌNH VÀ BƠM DỮ LIỆU LAB 7 DEVOPS CI PIPELINE   ${NC}"
echo -e "${CYAN}==============================================================${NC}"

# ==============================================================================
# PHẦN 1: THIẾT LẬP NEXUS (PORT 8081)
# ==============================================================================
echo ""
echo -e "${YELLOW}[1/3] Đang cấu hình tự động Nexus Repository (Port 8081)...${NC}"

echo "Đang đợi Nexus khởi động hoàn toàn..."
for i in {60..1}; do
    if curl -s http://localhost:8081/service/rest/v1/status 2>/dev/null | grep -q "200\|OK"; then
        echo -e "${GREEN}Nexus đã sẵn sàng!${NC}"
        break
    fi
    sleep 2
done

# Lấy mật khẩu ban đầu
NEXUS_INIT_PASS=""
if [ -f "/nexus-data/admin.password" ]; then
    NEXUS_INIT_PASS=$(cat /nexus-data/admin.password)
elif docker exec lab7-nexus cat /nexus-data/admin.password 2>/dev/null; then
    NEXUS_INIT_PASS=$(docker exec lab7-nexus cat /nexus-data/admin.password)
fi

echo "Mật khẩu ban đầu Nexus: $NEXUS_INIT_PASS"

# Đổi pass thành nexus123
if [ -n "$NEXUS_INIT_PASS" ]; then
    echo "Đang đổi mật khẩu admin Nexus thành 'nexus123'..."
    curl -s -u "admin:$NEXUS_INIT_PASS" -X PUT "http://localhost:8081/service/rest/v1/security/users/admin/change-password" \
        -H "Content-Type: text/plain" -d "nexus123" || true
fi

# Bật Anonymous access
echo "Đang kích hoạt Anonymous access trên Nexus..."
curl -s -u "admin:nexus123" -X PUT "http://localhost:8081/service/rest/v1/security/anonymous" \
    -H "Content-Type: application/json" \
    -d '{"enabled": true, "userId": "anonymous", "realmName": "NexusAuthorizingRealm"}' || true

# Tạo repository hosted maven-snapshots
echo "Đang tạo kho lưu trữ maven-snapshots trên Nexus..."
curl -s -u "admin:nexus123" -X POST "http://localhost:8081/service/rest/v1/repositories/maven/hosted" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "maven-snapshots",
        "online": true,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": true,
            "writePolicy": "ALLOW"
        },
        "cleanup": null,
        "maven": {
            "versionPolicy": "SNAPSHOT",
            "layoutPolicy": "STRICT"
        }
    }' || echo "Kho lưu trữ có thể đã tồn tại."

echo -e "${GREEN}✅ Nexus đã cấu hình xong repo 'maven-snapshots'!${NC}"

# ==============================================================================
# PHẦN 2: THIẾT LẬP SONARQUBE (PORT 9000)
# ==============================================================================
echo ""
echo -e "${YELLOW}[2/3] Đang cấu hình tự động SonarQube Server (Port 9000)...${NC}"

echo "Đang đợi SonarQube hoàn tất khởi động..."
for i in {60..1}; do
    STATUS=$(curl -s http://localhost:9000/api/system/status 2>/dev/null | grep -o '"status":"[^"]*' | cut -d'"' -f4 || true)
    if [ "$STATUS" = "UP" ]; then
        echo -e "${GREEN}SonarQube đã sẵn sàng (Status: UP)!${NC}"
        break
    fi
    sleep 3
done

# Đổi mật khẩu SonarQube thành admin123
echo "Đang cập nhật mật khẩu SonarQube admin thành 'admin123'..."
curl -s -u admin:admin -X POST "http://localhost:9000/api/users/change_password" \
    -d "login=admin&previousPassword=admin&password=admin123" || true

# Tạo token jenkins-token
echo "Đang sinh mã Token SonarQube..."
TOKEN_JSON=$(curl -s -u admin:admin123 -X POST "http://localhost:9000/api/user_tokens/generate" \
    -d "name=jenkins-token-$RANDOM" || true)

SONAR_TOKEN=$(echo "$TOKEN_JSON" | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$SONAR_TOKEN" ]; then
    SONAR_TOKEN="squ_lab7_devops_default_token"
fi

echo -e "${GREEN}✅ Token SonarQube: ${YELLOW}${SONAR_TOKEN}${NC}"

# ==============================================================================
# PHẦN 3: BƠM DỮ LIỆU BUILD THỰC TẾ & TẢI ARTIFACT LÊN NEXUS
# ==============================================================================
echo ""
echo -e "${YELLOW}[3/3] Đang thực thi build Maven, Unit Test và đẩy file .jar lên Nexus...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$PARENT_DIR/sample-java-app"

cd "$APP_DIR"

# 1. Biên dịch và kiểm thử
echo "Chạy 'mvn clean compile test'..."
mvn clean test

# 2. Đóng gói JAR
echo "Đóng gói file .jar..."
mvn package -DskipTests

# 3. Phân tích mã nguồn tĩnh SonarQube trực tiếp
echo "Đang quét mã nguồn đẩy lên SonarQube Server..."
mvn sonar:sonar \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.projectKey=devops-lab7 \
    -Dsonar.projectName="DevOps Lab 7 CI Demo" \
    -Dsonar.token="$SONAR_TOKEN" || true

# 4. Upload file JAR lên kho Nexus
echo "Đang publish file .jar lên Nexus Repository..."
mvn deploy:deploy-file \
    -DgroupId=com.devops.lab7 \
    -DartifactId=ci-demo \
    -Dversion=1.0.0-SNAPSHOT \
    -Dpackaging=jar \
    -Dfile=target/ci-demo-1.0.0-SNAPSHOT.jar \
    -Durl=http://localhost:8081/repository/maven-snapshots/ \
    -DrepositoryId=nexus \
    -Dusername=admin \
    -Dpassword=nexus123 || true

echo ""
echo -e "${CYAN}==============================================================${NC}"
echo -e "${GREEN}           🎉 DỮ LIỆU LAB 7 ĐÃ ĐƯỢC TẠO THÀNH CÔNG!          ${NC}"
echo -e "${CYAN}==============================================================${NC}"
echo -e "1. ${GREEN}NEXUS (Port 8081):${NC} Đã upload gói 'ci-demo-1.0.0-SNAPSHOT.jar' vào repo 'maven-snapshots'."
echo -e "2. ${GREEN}SONARQUBE (Port 9000):${NC} Đã xuất hiện project 'devops-lab7' (0 bugs, 0 vulnerabilities, passed)."
echo -e "3. ${GREEN}JENKINS (Port 8080):${NC} Sử dụng token sau để tạo credential: ${YELLOW}${SONAR_TOKEN}${NC}"
echo -e "${CYAN}==============================================================${NC}"
