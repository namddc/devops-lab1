#!/bin/bash
# ==============================================================================
# cleanup.sh — Dọn dẹp containers và giải phóng tài nguyên sau khi xong Lab 7
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

echo "Đang dừng các container Lab 7..."
docker compose down

echo "Bạn có muốn xóa toàn bộ volumes dữ liệu (jenkins_home, nexus_data, sonarqube_data)? (y/N)"
read -r answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    docker compose down -v
    echo "Đã xóa sạch volumes."
fi

echo "Hoàn tất dọn dẹp!"

