#!/bin/bash
# ==============================================================================
# cleanup.sh — Dọn dẹp containers và tài nguyên Lab 8
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

echo "Đang dừng Docker Compose stack..."
docker compose down

echo "Đang dừng container CD production nếu có..."
docker stop lab8-cd-production 2>/dev/null || true
docker rm lab8-cd-production 2>/dev/null || true
docker stop lab8-app 2>/dev/null || true
docker rm lab8-app 2>/dev/null || true

echo "Bạn có muốn xóa Docker images local devops-lab8-app không? (y/N)"
read -r answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    docker rmi devops-lab8-app:1.0 devops-lab8-app:latest devops-lab8-app:fat 2>/dev/null || true
    echo "Đã xóa images."
fi

echo "Hoàn tất dọn dẹp sạch sẽ!"
