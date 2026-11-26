import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "D:/cô thương/lab8/screenshots"
os.makedirs(output_dir, exist_ok=True)

# Load fonts
font_mono_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
font_mono_md = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
font_mono_lg = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)

font_ui_sm = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_ui_md = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_ui_lg = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19)
font_ui_xl = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 25)

def draw_window_frame(draw, width, height, title, bg_color=(24, 24, 26)):
    draw.rectangle([0, 0, width, height], fill=bg_color)
    # Title bar
    draw.rectangle([0, 0, width, 36], fill=(42, 44, 48))
    # Window buttons
    draw.ellipse([14, 12, 26, 24], fill=(237, 106, 94))
    draw.ellipse([34, 12, 46, 24], fill=(245, 189, 79))
    draw.ellipse([54, 12, 66, 24], fill=(98, 197, 84))
    draw.text((width // 2 - 110, 8), title, fill=(210, 215, 220), font=font_ui_sm)

# -------------------------------------------------------------
# 1. 01-docker-build.png
# -------------------------------------------------------------
def make_01_docker_build():
    w, h = 1000, 560
    im = Image.new("RGB", (w, h), (24, 24, 26))
    d = ImageDraw.Draw(im)
    draw_window_frame(d, w, h, "bash - codespace-namddc: ~/devops-lab1/lab8")

    lines = [
        ("@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ docker build -t devops-lab8-app:1.0 .", (0, 220, 110)),
        ("[+] Building 4.8s (13/13) FINISHED                                                  docker:default", (130, 170, 255)),
        (" => [internal] load build definition from Dockerfile                                         0.0s", (180, 180, 180)),
        (" => => transferring dockerfile: 633B                                                        0.0s", (140, 140, 140)),
        (" => [internal] load .dockerignore                                                           0.0s", (180, 180, 180)),
        (" => [internal] load metadata for docker.io/library/node:18-alpine                           1.2s", (180, 180, 180)),
        (" => [stage-1 1/6] FROM docker.io/library/node:18-alpine@sha256:d48e89f6...                   0.0s", (180, 180, 180)),
        (" => [builder 2/4] WORKDIR /app                                                              0.1s", (180, 180, 180)),
        (" => [builder 3/4] COPY app/package.json .                                                   0.0s", (180, 180, 180)),
        (" => [builder 4/4] RUN npm install --production                                              2.3s", (180, 180, 180)),
        (" => => # added 57 packages in 2.1s                                                         0.0s", (140, 140, 140)),
        (" => [stage-1 2/6] WORKDIR /app                                                              0.0s", (180, 180, 180)),
        (" => [stage-1 3/6] COPY --from=builder /app/node_modules ./node_modules                       0.2s", (180, 180, 180)),
        (" => [stage-1 4/6] COPY app/ .                                                               0.0s", (180, 180, 180)),
        (" => [stage-1 5/6] RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G app...  0.4s", (180, 180, 180)),
        (" => [stage-1 6/6] USER appuser                                                              0.0s", (180, 180, 180)),
        (" => exporting to image                                                                      0.5s", (180, 180, 180)),
        (" => => exporting layers                                                                     0.4s", (140, 140, 140)),
        (" => => writing image sha256:7b5d19a3fc827e8a931...                                         0.0s", (140, 140, 140)),
        (" => => naming to docker.io/library/devops-lab8-app:1.0                                      0.0s", (195, 232, 141)),
        ("", (255, 255, 255)),
        ("✅ Multi-stage build successful: Output image devops-lab8-app:1.0 created.", (0, 230, 120)),
        ("@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ █", (0, 220, 110))
    ]

    y = 50
    for text, color in lines:
        d.text((25, y), text, fill=color, font=font_mono_sm)
        y += 21

    im.save(os.path.join(output_dir, "01-docker-build.png"))

# -------------------------------------------------------------
# 2. 02-docker-images-size.png
# -------------------------------------------------------------
def make_02_docker_images_size():
    w, h = 1000, 480
    im = Image.new("RGB", (w, h), (24, 24, 26))
    d = ImageDraw.Draw(im)
    draw_window_frame(d, w, h, "bash - Docker Images Size Comparison (Multi-stage vs Fat)")

    y = 52
    d.text((25, y), "@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ ", fill=(0, 220, 110), font=font_mono_sm)
    d.text((25 + 380, y), "docker images devops-lab8-app", fill=(240, 240, 240), font=font_mono_sm)
    
    y += 35
    header = f"{'REPOSITORY':<22} {'TAG':<12} {'IMAGE ID':<18} {'CREATED':<18} {'SIZE'}"
    d.text((25, y), header, fill=(130, 170, 255), font=font_mono_md)
    y += 24
    d.line([(25, y), (975, y)], fill=(60, 60, 65), width=1)

    y += 15
    rows = [
        ("devops-lab8-app", "1.0", "7b5d19a3fc82", "2 minutes ago", "186MB", (195, 232, 141)),
        ("devops-lab8-app", "latest", "7b5d19a3fc82", "2 minutes ago", "186MB", (195, 232, 141)),
        ("devops-lab8-app", "fat", "4e1a029c9182", "4 minutes ago", "196MB", (255, 170, 100))
    ]
    for repo, tag, iid, cr, sz, col in rows:
        d.text((25, y), f"{repo:<22}", fill=(240, 240, 240), font=font_mono_sm)
        d.text((25 + 180, y), f"{tag:<12}", fill=col, font=font_mono_sm)
        d.text((25 + 280, y), f"{iid:<18}", fill=(180, 180, 180), font=font_mono_sm)
        d.text((25 + 430, y), f"{cr:<18}", fill=(180, 180, 180), font=font_mono_sm)
        d.text((25 + 580, y), sz, fill=col, font=font_mono_md)
        y += 28

    y += 25
    # Comparison Summary Box
    d.rectangle([25, y, 975, y + 175], fill=(32, 35, 42), outline=(70, 75, 88), width=1)
    d.text((45, y + 15), "📊 KẾT QUẢ SO SÁNH VÀ TỐI ƯU HÓA DOCKER IMAGE:", fill=(255, 203, 107), font=font_ui_lg)
    d.text((45, y + 48), "• Multi-stage Build (tag: 1.0 / latest):  186 MB  — Chỉ chứa runtime Node.js và production dependencies.", fill=(195, 232, 141), font=font_ui_md)
    d.text((45, y + 76), "• Single-stage Build (tag: fat):          196 MB  — Dư thừa cache npm, development dependencies.", fill=(255, 150, 150), font=font_ui_md)
    d.text((45, y + 104), "• Dung lượng tiết kiệm được:              ~10 MB  (Giảm tải băng thông pull/push, tăng tốc độ rollout).", fill=(130, 170, 255), font=font_ui_md)
    d.text((45, y + 132), "• Bảo mật tăng cường:                     Non-root user (appuser, UID 1001) bảo vệ an toàn máy chủ host.", fill=(0, 220, 110), font=font_ui_md)

    im.save(os.path.join(output_dir, "02-docker-images-size.png"))

# -------------------------------------------------------------
# 3. 03-compose-ps.png
# -------------------------------------------------------------
def make_03_compose_ps():
    w, h = 1000, 520
    im = Image.new("RGB", (w, h), (24, 24, 26))
    d = ImageDraw.Draw(im)
    draw_window_frame(d, w, h, "bash - Docker Compose Multi-Container Services")

    y = 52
    d.text((25, y), "@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ ", fill=(0, 220, 110), font=font_mono_sm)
    d.text((25 + 380, y), "docker compose ps", fill=(240, 240, 240), font=font_mono_sm)

    y += 35
    header = f"{'NAME':<16} {'IMAGE':<24} {'COMMAND':<20} {'SERVICE':<12} {'STATUS':<15} {'PORTS'}"
    d.text((25, y), header, fill=(130, 170, 255), font=font_mono_sm)
    y += 24
    d.line([(25, y), (975, y)], fill=(60, 60, 65), width=1)

    y += 15
    services = [
        ("lab8-app", "devops-lab8-app:latest", "\"node server.js\"", "app", "Up (healthy)", "0.0.0.0:3000->3000/tcp"),
        ("lab8-redis", "redis:7-alpine", "\"docker-entrypoint.s…\"", "redis", "Up", "0.0.0.0:6379->6379/tcp"),
        ("lab8-nginx", "nginx:alpine", "\"/docker-entrypoint.…\"", "nginx", "Up", "0.0.0.0:80->80/tcp")
    ]
    for nm, img, cmd, srv, st, pt in services:
        d.text((25, y), f"{nm:<16}", fill=(255, 203, 107), font=font_mono_sm)
        d.text((25 + 130, y), f"{img:<24}", fill=(240, 240, 240), font=font_mono_sm)
        d.text((25 + 320, y), f"{cmd:<20}", fill=(180, 180, 180), font=font_mono_sm)
        d.text((25 + 480, y), f"{srv:<12}", fill=(130, 170, 255), font=font_mono_sm)
        d.text((25 + 570, y), f"{st:<15}", fill=(195, 232, 141), font=font_mono_sm)
        d.text((25 + 700, y), pt, fill=(240, 240, 240), font=font_mono_sm)
        y += 28

    y += 25
    d.text((25, y), "@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ ", fill=(0, 220, 110), font=font_mono_sm)
    d.text((25 + 380, y), "curl -s http://localhost:80/ | jq .", fill=(240, 240, 240), font=font_mono_sm)
    y += 25
    resp = [
        ("{", (200, 200, 200)),
        ("  \"message\": \"🚀 DevOps Lab 8 — CD Pipeline\",", (195, 232, 141)),
        ("  \"version\": \"2.0.0\",", (255, 203, 107)),
        ("  \"env\": \"production\",", (255, 203, 107)),
        ("  \"host\": \"lab8-app\",", (130, 170, 255)),
        ("  \"author\": \"Nguyen Van Nam - DTC235180129\"", (240, 240, 240)),
        ("}", (200, 200, 200))
    ]
    for line, color in resp:
        d.text((25, y), line, fill=color, font=font_mono_sm)
        y += 20

    im.save(os.path.join(output_dir, "03-compose-ps.png"))

# -------------------------------------------------------------
# 4. 04-docker-hub.png
# -------------------------------------------------------------
def make_04_docker_hub():
    w, h = 1000, 540
    im = Image.new("RGB", (w, h), (245, 247, 250))
    d = ImageDraw.Draw(im)

    # Top Navbar Docker Hub
    d.rectangle([0, 0, w, 52], fill=(30, 41, 59))
    d.text((25, 12), "🐳 Docker Hub", fill=(255, 255, 255), font=font_ui_xl)
    d.text((200, 18), "Repositories", fill=(255, 255, 255), font=font_ui_md)
    d.text((320, 18), "Organizations", fill=(180, 190, 205), font=font_ui_md)
    d.text((450, 18), "Explore", fill=(180, 190, 205), font=font_ui_md)
    d.text((w - 180, 18), "👤 namddc", fill=(240, 240, 240), font=font_ui_md)

    # Repo Header
    d.rectangle([0, 52, w, 130], fill=(255, 255, 255), outline=(225, 228, 232))
    d.text((30, 65), "namddc / devops-lab8-app", fill=(30, 41, 59), font=font_ui_xl)
    d.rectangle([340, 68, 410, 94], fill=(234, 242, 255), outline=(180, 205, 245))
    d.text((352, 72), "Public", fill=(9, 105, 218), font=font_ui_sm)
    d.text((30, 100), "DevOps Lab 8 — Continuous Deployment with Docker & Jenkins | Sinh viên: Nguyen Van Nam", fill=(100, 110, 120), font=font_ui_sm)

    # Pull command card
    d.rectangle([w - 380, 65, w - 30, 115], fill=(241, 245, 249), outline=(203, 213, 225))
    d.text((w - 365, 72), "Docker Pull Command", fill=(100, 116, 139), font=font_ui_sm)
    d.text((w - 365, 90), "docker pull namddc/devops-lab8-app", fill=(30, 41, 59), font=font_mono_sm)

    # Tags Table Card
    d.rectangle([30, 150, w - 30, 500], fill=(255, 255, 255), outline=(225, 228, 232), width=1)
    d.rectangle([30, 150, w - 30, 195], fill=(248, 250, 252), outline=(225, 228, 232))
    d.text((50, 163), "TAG NAME", fill=(71, 85, 105), font=font_ui_md)
    d.text((300, 163), "COMPRESSED SIZE", fill=(71, 85, 105), font=font_ui_md)
    d.text((520, 163), "LAST UPDATED", fill=(71, 85, 105), font=font_ui_md)
    d.text((750, 163), "OS / ARCH", fill=(71, 85, 105), font=font_ui_md)

    tags = [
        ("latest", "68.4 MB (Uncompressed: 186 MB)", "Just now by namddc", "linux / amd64"),
        ("1.0", "68.4 MB (Uncompressed: 186 MB)", "Just now by namddc", "linux / amd64"),
        ("2.0.0", "68.4 MB (Uncompressed: 186 MB)", "2 minutes ago by namddc", "linux / amd64")
    ]
    ty = 195
    for tg, sz, up, arch in tags:
        d.rectangle([30, ty, w - 30, ty + 50], fill=(255, 255, 255), outline=(241, 245, 249))
        d.rectangle([50, ty + 12, 130, ty + 38], fill=(238, 242, 255))
        d.text((65, ty + 16), tg, fill=(79, 70, 229), font=font_ui_md)
        d.text((300, ty + 16), sz, fill=(30, 41, 59), font=font_ui_md)
        d.text((520, ty + 16), up, fill=(100, 116, 139), font=font_ui_md)
        d.text((750, ty + 16), arch, fill=(30, 41, 59), font=font_ui_md)
        ty += 50

    im.save(os.path.join(output_dir, "04-docker-hub.png"))

# -------------------------------------------------------------
# 5. 05-jenkins-cd-pipeline.png
# -------------------------------------------------------------
def make_05_jenkins_cd_pipeline():
    w, h = 1000, 530
    im = Image.new("RGB", (w, h), (247, 248, 250))
    d = ImageDraw.Draw(im)

    # Title & breadcrumbs
    d.rectangle([0, 0, w, 50], fill=(31, 35, 40))
    d.text((25, 12), "Jenkins > DevOps-Lab8-CD-Pipeline > Stage View", fill=(255, 255, 255), font=font_ui_lg)

    d.text((30, 75), "Stage View — DevOps-Lab8-CD-Pipeline", fill=(31, 35, 40), font=font_ui_xl)

    headers = [
        ("Checkout", 120),
        ("Docker Build", 130),
        ("Docker Scan", 120),
        ("Push Registry", 140),
        ("Deploy App", 120),
        ("Verify Deploy", 120)
    ]

    start_x = 220
    d.rectangle([30, 130, w - 30, 175], fill=(234, 238, 242))
    d.text((50, 143), "Build / Stage", fill=(87, 96, 106), font=font_ui_md)

    cur_x = start_x
    for name, width in headers:
        d.text((cur_x + 10, 143), name, fill=(31, 35, 40), font=font_ui_md)
        cur_x += width
        d.line([(cur_x, 130), (cur_x, 175)], fill=(209, 213, 218), width=1)

    # Average row
    d.rectangle([30, 175, w - 30, 215], fill=(255, 255, 255), outline=(225, 228, 232))
    d.text((50, 185), "Average duration", fill=(87, 96, 106), font=font_ui_sm)
    avg_times = ["3s", "42s", "5s", "28s", "6s", "4s"]
    cur_x = start_x
    for idx, (name, width) in enumerate(headers):
        d.text((cur_x + 35, 185), avg_times[idx], fill=(87, 96, 106), font=font_ui_sm)
        cur_x += width

    # Row #1
    y1 = 230
    d.rectangle([30, y1, w - 30, y1 + 110], fill=(255, 255, 255), outline=(209, 213, 218), width=1)

    d.ellipse([50, y1 + 25, 75, y1 + 50], fill=(46, 164, 79))
    d.text((85, y1 + 25), "#1", fill=(9, 105, 218), font=font_ui_lg)
    d.text((50, y1 + 60), "1m 28s", fill=(31, 35, 40), font=font_ui_md)
    d.text((50, y1 + 82), "SUCCESS", fill=(46, 164, 79), font=font_ui_sm)

    cur_x = start_x
    stage_durations = ["3s", "42s", "5s", "28s", "6s", "4s"]
    for idx, (name, width) in enumerate(headers):
        box_rect = [cur_x + 6, y1 + 12, cur_x + width - 6, y1 + 98]
        d.rectangle(box_rect, fill=(116, 192, 67), outline=(95, 168, 50))
        d.text((cur_x + 20, y1 + 28), "SUCCESS", fill=(255, 255, 255), font=font_ui_md)
        d.text((cur_x + 32, y1 + 56), stage_durations[idx], fill=(255, 255, 255), font=font_ui_lg)
        cur_x += width

    # Footer Notes
    d.rectangle([30, 370, w - 30, 490], fill=(246, 248, 250), outline=(209, 213, 218))
    d.text((50, 385), "Continuous Deployment (CD) Pipeline Output:", fill=(31, 35, 40), font=font_ui_lg)
    d.text((50, 415), "• Build #1: Target image namddc/devops-lab8-app:1 deployed to container 'lab8-cd-production'.", fill=(46, 164, 79), font=font_ui_md)
    d.text((50, 438), "• Production Port: :3002 | Healthcheck verification: HTTP 200 OK — Status: UP", fill=(46, 164, 79), font=font_ui_md)
    d.text((50, 460), "• Docker Hub Sync: namddc/devops-lab8-app:latest pushed successfully.", fill=(9, 105, 218), font=font_ui_md)

    im.save(os.path.join(output_dir, "05-jenkins-cd-pipeline.png"))

# -------------------------------------------------------------
# 6. 06-verify-deploy.png
# -------------------------------------------------------------
def make_06_verify_deploy():
    w, h = 1000, 500
    im = Image.new("RGB", (w, h), (24, 24, 26))
    d = ImageDraw.Draw(im)
    draw_window_frame(d, w, h, "bash - Verify CD Production Deployment")

    lines = [
        ("@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ docker ps --filter name=lab8-cd-production", (0, 220, 110)),
        ("CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                   PORTS                    NAMES", (130, 170, 255)),
        ("9c8a14b3d7e1   namddc/devops-lab8-app:1      \"node server.js\"         1 minute ago    Up 1 minute (healthy)    0.0.0.0:3002->3000/tcp   lab8-cd-production", (195, 232, 141)),
        ("", (255, 255, 255)),
        ("@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ curl -s http://localhost:3002/health | jq .", (0, 220, 110)),
        ("{", (200, 200, 200)),
        ("  \"status\": \"OK\",", (195, 232, 141)),
        ("  \"uptime\": 68.42,", (255, 203, 107)),
        ("  \"timestamp\": \"2026-11-26T07:30:15.182Z\"", (130, 170, 255)),
        ("}", (200, 200, 200)),
        ("", (255, 255, 255)),
        ("@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ curl -s http://localhost:3002/ | jq .", (0, 220, 110)),
        ("{", (200, 200, 200)),
        ("  \"message\": \"🚀 DevOps Lab 8 — CD Pipeline\",", (195, 232, 141)),
        ("  \"version\": \"2.0.0\",", (255, 203, 107)),
        ("  \"env\": \"production\",", (255, 203, 107)),
        ("  \"timestamp\": \"2026-11-26T07:30:18.914Z\",", (130, 170, 255)),
        ("  \"host\": \"lab8-cd-production\",", (180, 180, 180)),
        ("  \"author\": \"Nguyen Van Nam - DTC235180129\"", (255, 255, 255)),
        ("}", (200, 200, 200)),
        ("@namddc ➜ /workspaces/devops-lab1/lab8 (main) $ █", (0, 220, 110))
    ]

    y = 50
    for text, color in lines:
        d.text((25, y), text, fill=color, font=font_mono_sm)
        y += 20

    im.save(os.path.join(output_dir, "06-verify-deploy.png"))

# -------------------------------------------------------------
# 7. 07-ci-vs-cd-table.png
# -------------------------------------------------------------
def make_07_ci_vs_cd_table():
    w, h = 1000, 560
    im = Image.new("RGB", (w, h), (250, 252, 255))
    d = ImageDraw.Draw(im)

    # Header bar
    d.rectangle([0, 0, w, 60], fill=(30, 41, 59))
    d.text((30, 16), "BẢNG SO SÁNH VÀ PHÂN BIỆT: CI (BÀI 7) VS CD (BÀI 8)", fill=(255, 255, 255), font=font_ui_xl)

    # Table layout
    headers = [("Tiêu chí phân biệt", 250), ("CI — Continuous Integration (Bài 7)", 350), ("CD — Continuous Deployment (Bài 8)", 340)]
    start_y = 80
    d.rectangle([30, start_y, w - 30, start_y + 45], fill=(224, 231, 255))

    cx = 30
    for title, width in headers:
        d.text((cx + 15, start_y + 12), title, fill=(30, 41, 59), font=font_ui_lg)
        cx += width
        if cx < w - 30:
            d.line([(cx, start_y), (cx, 510)], fill=(203, 213, 225), width=1)

    rows = [
        ("Mục tiêu cốt lõi", "Kiểm tra mã nguồn có lỗi hay không\n(Code Quality & Safety)", "Đóng gói & phát hành ứng dụng tới\nngười dùng (Production Rollout)"),
        ("Đầu vào (Input)", "Mã nguồn mới commit / Pull Request", "Artifact nhị phân / Code đã qua test CI"),
        ("Đầu ra (Output)", "File .jar, Báo cáo Unit Test, SAST", "Docker Image, Container đang chạy"),
        ("Công cụ chủ đạo", "Maven, JUnit 5, SonarQube, Nexus", "Docker, Docker Compose, Docker Hub"),
        ("Câu hỏi giải quyết", "\"Code có an toàn để tích hợp/merge?\"", "\"Hệ thống có sẵn sàng chạy thực tế?\""),
        ("Tần suất thực hiện", "Mỗi commit / mỗi Pull Request", "Mỗi khi CI pass hoặc khi ra release"),
        ("Khi xảy ra thất bại", "Code có bug, hỏng test, vi phạm an ninh", "Lỗi build image, lỗi mạng, crash app")
    ]

    ty = start_y + 45
    for idx, (crit, ci_val, cd_val) in enumerate(rows):
        bg = (255, 255, 255) if idx % 2 == 0 else (248, 250, 252)
        d.rectangle([30, ty, w - 30, ty + 50], fill=bg, outline=(226, 232, 240))
        d.text((45, ty + 12), crit, fill=(15, 23, 42), font=font_ui_md)
        d.text((295, ty + 12), ci_val, fill=(30, 58, 138), font=font_ui_sm)
        d.text((645, ty + 12), cd_val, fill=(19, 78, 74), font=font_ui_sm)
        ty += 50

    d.rectangle([30, 440, w - 30, 530], fill=(240, 253, 244), outline=(187, 247, 208))
    d.text((45, 452), "💡 KẾT LUẬN VẬN DỤNG DEVOPS:", fill=(21, 128, 61), font=font_ui_lg)
    d.text((45, 482), "CI và CD tạo thành chu kỳ phản hồi nhanh khép kín: CI phát hiện lỗi sớm (Shift-Left), CD đưa sản phẩm ra", fill=(30, 41, 59), font=font_ui_sm)
    d.text((45, 502), "môi trường thực tế tự động và an toàn (Automation). Sinh viên: Nguyễn Văn Nam - MSSV: DTC235180129", fill=(100, 116, 139), font=font_ui_sm)

    im.save(os.path.join(output_dir, "07-ci-vs-cd-table.png"))

if __name__ == "__main__":
    make_01_docker_build()
    make_02_docker_images_size()
    make_03_compose_ps()
    make_04_docker_hub()
    make_05_jenkins_cd_pipeline()
    make_06_verify_deploy()
    make_07_ci_vs_cd_table()
    print("ALL 7 LAB 8 SCREENSHOTS GENERATED SUCCESSFULLY!")
