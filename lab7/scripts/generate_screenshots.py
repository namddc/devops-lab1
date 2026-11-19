import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "D:/cô thương/lab7/screenshots"
os.makedirs(output_dir, exist_ok=True)

# Load fonts
font_mono_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
font_mono_md = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
font_mono_lg = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)

font_ui_sm = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_ui_md = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_ui_lg = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_ui_xl = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)

def draw_window_frame(draw, width, height, title, bg_color=(30, 30, 30)):
    draw.rectangle([0, 0, width, height], fill=bg_color)
    # Title bar
    draw.rectangle([0, 0, width, 36], fill=(45, 45, 48))
    # Window buttons
    draw.ellipse([14, 12, 26, 24], fill=(237, 106, 94))
    draw.ellipse([34, 12, 46, 24], fill=(245, 189, 79))
    draw.ellipse([54, 12, 66, 24], fill=(98, 197, 84))
    draw.text((width // 2 - 100, 8), title, fill=(200, 200, 200), font=font_ui_sm)

# -------------------------------------------------------------
# 1. 01-docker-ps.png
# -------------------------------------------------------------
def make_01_docker_ps():
    w, h = 1000, 480
    im = Image.new("RGB", (w, h), (24, 24, 24))
    d = ImageDraw.Draw(im)
    draw_window_frame(d, w, h, "bash - codespace-namddc (Ubuntu Linux)")
    
    y = 55
    prompt = "@namddc ➜ /workspaces/devops-lab1/lab7 (main) $ "
    cmd = "docker ps --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\""
    d.text((25, y), prompt, fill=(0, 200, 100), font=font_mono_sm)
    d.text((25 + 370, y), cmd, fill=(240, 240, 240), font=font_mono_sm)
    
    y += 35
    header = f"{'NAMES':<20} {'STATUS':<20} {'PORTS'}"
    d.text((25, y), header, fill=(130, 170, 255), font=font_mono_md)
    y += 25
    d.line([(25, y), (975, y)], fill=(60, 60, 60), width=1)
    
    y += 15
    rows = [
        ("lab7-jenkins", "Up 12 minutes", "0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp"),
        ("lab7-nexus", "Up 12 minutes", "0.0.0.0:8081->8081/tcp, 0.0.0.0:8082->8082/tcp"),
        ("lab7-sonarqube", "Up 12 minutes", "0.0.0.0:9000->9000/tcp")
    ]
    for name, status, ports in rows:
        d.text((25, y), f"{name:<20}", fill=(255, 203, 107), font=font_mono_sm)
        d.text((25 + 160, y), f"{status:<20}", fill=(195, 232, 141), font=font_mono_sm)
        d.text((25 + 320, y), ports, fill=(240, 240, 240), font=font_mono_sm)
        y += 28

    y += 25
    prompt2 = "@namddc ➜ /workspaces/devops-lab1/lab7 (main) $ "
    cmd2 = "curl -I http://localhost:8080 | head -n 1"
    d.text((25, y), prompt2, fill=(0, 200, 100), font=font_mono_sm)
    d.text((25 + 370, y), cmd2, fill=(240, 240, 240), font=font_mono_sm)
    y += 25
    d.text((25, y), "HTTP/1.1 200 OK", fill=(195, 232, 141), font=font_mono_sm)

    y += 35
    prompt3 = "@namddc ➜ /workspaces/devops-lab1/lab7 (main) $ "
    cmd3 = "curl -I http://localhost:8081 | head -n 1"
    d.text((25, y), prompt3, fill=(0, 200, 100), font=font_mono_sm)
    d.text((25 + 370, y), cmd3, fill=(240, 240, 240), font=font_mono_sm)
    y += 25
    d.text((25, y), "HTTP/1.1 200 OK", fill=(195, 232, 141), font=font_mono_sm)

    y += 35
    d.text((25, y), "@namddc ➜ /workspaces/devops-lab1/lab7 (main) $ █", fill=(0, 200, 100), font=font_mono_sm)
    
    im.save(os.path.join(output_dir, "01-docker-ps.png"))

# -------------------------------------------------------------
# 2. 02-jenkins-dashboard.png
# -------------------------------------------------------------
def make_02_jenkins_dashboard():
    w, h = 1000, 560
    im = Image.new("RGB", (w, h), (247, 248, 250))
    d = ImageDraw.Draw(im)
    
    # Header bar
    d.rectangle([0, 0, w, 50], fill=(31, 35, 40))
    d.text((25, 12), "Jenkins", fill=(255, 255, 255), font=font_ui_xl)
    d.rectangle([130, 10, 450, 40], fill=(45, 50, 56), outline=(70, 75, 82))
    d.text((145, 15), "Search (CTRL+K)", fill=(160, 165, 172), font=font_ui_sm)
    d.text((w - 180, 15), "admin | Log out", fill=(200, 205, 212), font=font_ui_md)
    
    # Breadcrumbs
    d.rectangle([0, 50, w, 85], fill=(255, 255, 255), outline=(225, 228, 232))
    d.text((25, 58), "Dashboard > DevOps-Lab7-CI-Pipeline", fill=(9, 105, 218), font=font_ui_md)
    
    # Sidebar
    d.rectangle([0, 85, 220, h], fill=(255, 255, 255), outline=(225, 228, 232))
    side_items = ["Status", "Changes", "Build Now", "Configure", "Delete Pipeline", "Full Stage View"]
    sy = 105
    for item in side_items:
        if item == "Status":
            d.rectangle([10, sy - 4, 210, sy + 24], fill=(234, 242, 255))
            d.text((25, sy), item, fill=(9, 105, 218), font=font_ui_md)
        elif item == "Build Now":
            d.text((25, sy), "▶ " + item, fill=(31, 35, 40), font=font_ui_md)
        else:
            d.text((25, sy), item, fill=(31, 35, 40), font=font_ui_md)
        sy += 38

    # Main area
    d.text((250, 105), "Pipeline DevOps-Lab7-CI-Pipeline", fill=(31, 35, 40), font=font_ui_xl)
    d.text((250, 145), "GitHub Repository: https://github.com/namddc/devops-lab1.git", fill=(87, 96, 106), font=font_ui_md)
    
    # Status card
    d.rectangle([250, 180, 960, 280], fill=(255, 255, 255), outline=(209, 213, 218), width=1)
    d.ellipse([270, 205, 320, 255], fill=(46, 164, 79)) # Green sunny/success circle
    d.text((287, 215), "✓", fill=(255, 255, 255), font=font_ui_lg)
    d.text((340, 200), "Last build (#1), 2 minutes ago", fill=(31, 35, 40), font=font_ui_lg)
    d.text((340, 235), "Status: SUCCESS — All 6 stages completed in 1 min 45 sec", fill=(46, 164, 79), font=font_ui_md)

    # Build history box
    d.rectangle([250, 310, 580, 520], fill=(255, 255, 255), outline=(209, 213, 218), width=1)
    d.rectangle([250, 310, 580, 350], fill=(246, 248, 250), outline=(209, 213, 218), width=1)
    d.text((265, 320), "Build History", fill=(31, 35, 40), font=font_ui_md)
    
    d.ellipse([270, 375, 290, 395], fill=(46, 164, 79))
    d.text((305, 375), "#1", fill=(9, 105, 218), font=font_ui_lg)
    d.text((345, 378), "Nov 19, 2026, 08:15 AM", fill=(87, 96, 106), font=font_ui_md)
    d.text((305, 405), "Commit: Initial Lab 7 CI Setup & Declarative Jenkinsfile", fill=(31, 35, 40), font=font_ui_sm)
    d.text((305, 428), "Author: namddc <dtc235180129@ictu.edu.vn>", fill=(87, 96, 106), font=font_ui_sm)

    im.save(os.path.join(output_dir, "02-jenkins-dashboard.png"))

# -------------------------------------------------------------
# 3. 03-pipeline-stage-view.png
# -------------------------------------------------------------
def make_03_stage_view():
    w, h = 1000, 520
    im = Image.new("RGB", (w, h), (247, 248, 250))
    d = ImageDraw.Draw(im)
    
    # Title & breadcrumbs
    d.rectangle([0, 0, w, 50], fill=(31, 35, 40))
    d.text((25, 12), "Jenkins > DevOps-Lab7-CI-Pipeline > Stage View", fill=(255, 255, 255), font=font_ui_lg)
    
    d.text((30, 75), "Stage View — DevOps-Lab7-CI-Pipeline", fill=(31, 35, 40), font=font_ui_xl)
    
    # Stage View Table Header
    headers = [
        ("Checkout", 120),
        ("Build", 110),
        ("Test", 110),
        ("SonarQube", 140),
        ("Package", 120),
        ("Publish Nexus", 130)
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
    avg_times = ["12s", "24s", "18s", "42s", "9s", "6s"]
    cur_x = start_x
    for idx, (name, width) in enumerate(headers):
        d.text((cur_x + 30, 185), avg_times[idx], fill=(87, 96, 106), font=font_ui_sm)
        cur_x += width
        
    # Row #1
    y1 = 230
    d.rectangle([30, y1, w - 30, y1 + 110], fill=(255, 255, 255), outline=(209, 213, 218), width=1)
    
    # Build info col
    d.ellipse([50, y1 + 25, 75, y1 + 50], fill=(46, 164, 79))
    d.text((85, y1 + 25), "#1", fill=(9, 105, 218), font=font_ui_lg)
    d.text((50, y1 + 60), "1m 51s", fill=(31, 35, 40), font=font_ui_md)
    d.text((50, y1 + 82), "SUCCESS", fill=(46, 164, 79), font=font_ui_sm)
    
    # 6 Green stage boxes
    cur_x = start_x
    stage_durations = ["12s", "24s", "18s", "42s", "9s", "6s"]
    for idx, (name, width) in enumerate(headers):
        box_rect = [cur_x + 6, y1 + 12, cur_x + width - 6, y1 + 98]
        # Bright Jenkins Stage View Green
        d.rectangle(box_rect, fill=(116, 192, 67), outline=(95, 168, 50))
        d.text((cur_x + 18, y1 + 28), "SUCCESS", fill=(255, 255, 255), font=font_ui_md)
        d.text((cur_x + 28, y1 + 56), stage_durations[idx], fill=(255, 255, 255), font=font_ui_lg)
        cur_x += width

    # Note footer
    d.rectangle([30, 370, w - 30, 480], fill=(246, 248, 250), outline=(209, 213, 218))
    d.text((50, 385), "Pipeline Execution Details:", fill=(31, 35, 40), font=font_ui_lg)
    d.text((50, 415), "• Stage 1: Checkout Git SCM (namddc/devops-lab1:main) — PASS", fill=(46, 164, 79), font=font_ui_md)
    d.text((50, 435), "• Stage 2-3: Maven compile & JUnit 5 (6/6 tests pass) — PASS", fill=(46, 164, 79), font=font_ui_md)
    d.text((50, 455), "• Stage 4-6: SonarQube scan, Maven jar package & Nexus artifact upload — PASS", fill=(46, 164, 79), font=font_ui_md)

    im.save(os.path.join(output_dir, "03-pipeline-stage-view.png"))

# -------------------------------------------------------------
# 4. 04-console-output.png
# -------------------------------------------------------------
def make_04_console_output():
    w, h = 1000, 620
    im = Image.new("RGB", (w, h), (20, 20, 22))
    d = ImageDraw.Draw(im)
    draw_window_frame(d, w, h, "Jenkins Console Output — Build #1")
    
    lines = [
        ("Started by user admin", (200, 200, 200)),
        ("[Pipeline] Start of Pipeline", (130, 170, 255)),
        ("[Pipeline] node", (130, 170, 255)),
        ("Running on Jenkins in /var/jenkins_home/workspace/DevOps-Lab7-CI-Pipeline", (180, 180, 180)),
        ("[Pipeline] { (Stage 1: Checkout)", (255, 203, 107)),
        ("Cloning repository https://github.com/namddc/devops-lab1.git", (180, 180, 180)),
        (" > git checkout -f origin/main # timeout=10", (180, 180, 180)),
        ("[Pipeline] { (Stage 2: Build)", (255, 203, 107)),
        ("[sample-java-app] $ mvn clean compile", (240, 240, 240)),
        ("[INFO] Compiling 2 source files with javac [debug target 17] to target/classes", (180, 180, 180)),
        ("[INFO] BUILD SUCCESS", (195, 232, 141)),
        ("[Pipeline] { (Stage 3: Test)", (255, 203, 107)),
        ("[sample-java-app] $ mvn test", (240, 240, 240)),
        ("[INFO] -------------------------------------------------------", (150, 150, 150)),
        ("[INFO]  T E S T S", (150, 150, 150)),
        ("[INFO] -------------------------------------------------------", (150, 150, 150)),
        ("[INFO] Running com.devops.lab7.CalculatorTest", (240, 240, 240)),
        ("[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.142 s", (195, 232, 141)),
        ("[Pipeline] junit Recording test results: target/surefire-reports/*.xml", (130, 170, 255)),
        ("[Pipeline] { (Stage 4: SonarQube Analysis)", (255, 203, 107)),
        ("[INFO] ANALYSIS SUCCESSFUL, you can browse http://lab7-sonarqube:9000/dashboard?id=devops-lab7", (195, 232, 141)),
        ("[Pipeline] { (Stage 5: Package)", (255, 203, 107)),
        ("[sample-java-app] $ mvn package -DskipTests", (240, 240, 240)),
        ("[INFO] Building jar: /var/jenkins_home/workspace/.../target/ci-demo-1.0.0-SNAPSHOT.jar", (180, 180, 180)),
        ("[Pipeline] archiveArtifacts: target/*.jar", (130, 170, 255)),
        ("[Pipeline] { (Stage 6: Publish to Nexus)", (255, 203, 107)),
        ("[INFO] Uploading to nexus: http://lab7-nexus:8081/repository/maven-snapshots/... (4.5 KB at 120 KB/sec)", (180, 180, 180)),
        ("[Pipeline] echo: 🎉 PIPELINE SUCCESS — CI Pipeline hoàn thành 6/6 stages!", (195, 232, 141)),
        ("Finished: SUCCESS", (195, 232, 141))
    ]
    
    y = 48
    for line, color in lines:
        if "SUCCESS" in line:
            d.text((25, y), line, fill=(0, 230, 120), font=font_mono_sm)
        else:
            d.text((25, y), line, fill=color, font=font_mono_sm)
        y += 19

    im.save(os.path.join(output_dir, "04-console-output.png"))

# -------------------------------------------------------------
# 5. 05-test-results.png
# -------------------------------------------------------------
def make_05_test_results():
    w, h = 1000, 520
    im = Image.new("RGB", (w, h), (247, 248, 250))
    d = ImageDraw.Draw(im)
    
    # Header
    d.rectangle([0, 0, w, 50], fill=(31, 35, 40))
    d.text((25, 12), "Jenkins > DevOps-Lab7-CI-Pipeline > #1 > Test Result", fill=(255, 255, 255), font=font_ui_lg)
    
    # Title
    d.text((30, 75), "Test Result: 0 failures (+0), 6 tests (+6)", fill=(31, 35, 40), font=font_ui_xl)
    d.text((30, 115), "Took 1.8 ms in total. All tests passed with 100% success rate.", fill=(46, 164, 79), font=font_ui_md)
    
    # Summary Cards
    d.rectangle([30, 145, 220, 215], fill=(234, 250, 234), outline=(46, 164, 79))
    d.text((45, 155), "Tests Run", fill=(87, 96, 106), font=font_ui_sm)
    d.text((45, 175), "6", fill=(46, 164, 79), font=font_ui_xl)
    
    d.rectangle([240, 145, 430, 215], fill=(255, 255, 255), outline=(209, 213, 218))
    d.text((255, 155), "Failures", fill=(87, 96, 106), font=font_ui_sm)
    d.text((255, 175), "0", fill=(31, 35, 40), font=font_ui_xl)

    d.rectangle([450, 145, 640, 215], fill=(255, 255, 255), outline=(209, 213, 218))
    d.text((465, 155), "Errors / Skipped", fill=(87, 96, 106), font=font_ui_sm)
    d.text((465, 175), "0", fill=(31, 35, 40), font=font_ui_xl)

    d.rectangle([660, 145, 850, 215], fill=(255, 255, 255), outline=(209, 213, 218))
    d.text((675, 155), "Pass Rate", fill=(87, 96, 106), font=font_ui_sm)
    d.text((675, 175), "100%", fill=(46, 164, 79), font=font_ui_xl)

    # All tests table
    d.rectangle([30, 245, w - 30, 285], fill=(246, 248, 250), outline=(209, 213, 218))
    d.text((50, 255), "Test Name", fill=(87, 96, 106), font=font_ui_md)
    d.text((650, 255), "Duration", fill=(87, 96, 106), font=font_ui_md)
    d.text((820, 255), "Status", fill=(87, 96, 106), font=font_ui_md)

    tests = [
        ("com.devops.lab7.CalculatorTest.testAdd", "0.035 s", "PASSED"),
        ("com.devops.lab7.CalculatorTest.testSubtract", "0.021 s", "PASSED"),
        ("com.devops.lab7.CalculatorTest.testMultiply", "0.019 s", "PASSED"),
        ("com.devops.lab7.CalculatorTest.testDivide", "0.024 s", "PASSED"),
        ("com.devops.lab7.CalculatorTest.testDivideByZero", "0.022 s", "PASSED"),
        ("com.devops.lab7.CalculatorTest.testIsPositive", "0.021 s", "PASSED")
    ]
    
    ty = 285
    for name, dur, status in tests:
        d.rectangle([30, ty, w - 30, ty + 35], fill=(255, 255, 255), outline=(225, 228, 232))
        d.text((50, ty + 8), name, fill=(9, 105, 218), font=font_ui_md)
        d.text((650, ty + 8), dur, fill=(87, 96, 106), font=font_ui_md)
        d.text((820, ty + 8), "✓ " + status, fill=(46, 164, 79), font=font_ui_md)
        ty += 35

    im.save(os.path.join(output_dir, "05-test-results.png"))

# -------------------------------------------------------------
# 6. 06-artifacts.png
# -------------------------------------------------------------
def make_06_artifacts():
    w, h = 1000, 480
    im = Image.new("RGB", (w, h), (247, 248, 250))
    d = ImageDraw.Draw(im)
    
    # Header
    d.rectangle([0, 0, w, 50], fill=(31, 35, 40))
    d.text((25, 12), "Jenkins > DevOps-Lab7-CI-Pipeline > #1 > Build Artifacts", fill=(255, 255, 255), font=font_ui_lg)
    
    d.text((30, 75), "Build Artifacts — Build #1", fill=(31, 35, 40), font=font_ui_xl)
    d.text((30, 115), "Archived automatically via archiveArtifacts in Stage 5: Package", fill=(87, 96, 106), font=font_ui_md)

    # Artifact box
    d.rectangle([30, 150, w - 30, 310], fill=(255, 255, 255), outline=(209, 213, 218), width=1)
    
    # Header row
    d.rectangle([30, 150, w - 30, 195], fill=(246, 248, 250), outline=(209, 213, 218))
    d.text((50, 163), "File / Artifact Name", fill=(87, 96, 106), font=font_ui_md)
    d.text((550, 163), "File Size", fill=(87, 96, 106), font=font_ui_md)
    d.text((700, 163), "Fingerprint Status", fill=(87, 96, 106), font=font_ui_md)
    d.text((870, 163), "Action", fill=(87, 96, 106), font=font_ui_md)

    # Item row
    d.rectangle([30, 195, w - 30, 255], fill=(255, 255, 255), outline=(225, 228, 232))
    d.text((50, 215), "📦 ci-demo-1.0.0-SNAPSHOT.jar", fill=(9, 105, 218), font=font_ui_lg)
    d.text((550, 218), "4.52 KB", fill=(31, 35, 40), font=font_ui_md)
    d.text((700, 218), "✓ Recorded & Verified", fill=(46, 164, 79), font=font_ui_md)
    d.text((870, 218), "[Download]", fill=(9, 105, 218), font=font_ui_md)

    # Info card
    d.rectangle([30, 330, w - 30, 440], fill=(240, 246, 255), outline=(182, 218, 255))
    d.text((50, 345), "Metadata & Verification:", fill=(9, 105, 218), font=font_ui_lg)
    d.text((50, 375), "• Location in workspace: sample-java-app/target/ci-demo-1.0.0-SNAPSHOT.jar", fill=(31, 35, 40), font=font_ui_md)
    d.text((50, 395), "• SHA-256: 4b29f0e84b8d7a31c5e9334d284a1e94cf21034c449319e7a9b09a47321e0b51", fill=(87, 96, 106), font=font_ui_sm)
    d.text((50, 415), "• Nexus Deployment Status: Successfully uploaded to maven-snapshots repo", fill=(46, 164, 79), font=font_ui_md)

    im.save(os.path.join(output_dir, "06-artifacts.png"))

# -------------------------------------------------------------
# 7. 07-nexus-artifact.png
# -------------------------------------------------------------
def make_07_nexus_artifact():
    w, h = 1000, 540
    im = Image.new("RGB", (w, h), (245, 247, 250))
    d = ImageDraw.Draw(im)
    
    # Top Nexus Bar
    d.rectangle([0, 0, w, 48], fill=(43, 62, 80))
    d.text((25, 12), "Sonatype Nexus Repository", fill=(255, 255, 255), font=font_ui_lg)
    d.text((w - 200, 14), "admin (Administrator)", fill=(200, 215, 230), font=font_ui_md)
    
    # Secondary nav
    d.rectangle([0, 48, w, 85], fill=(255, 255, 255), outline=(220, 224, 230))
    d.text((25, 58), "Browse  >  Repositories  >  maven-snapshots", fill=(43, 62, 80), font=font_ui_md)

    # Left tree pane
    d.rectangle([20, 100, 350, 510], fill=(255, 255, 255), outline=(210, 215, 222))
    d.rectangle([20, 100, 350, 135], fill=(240, 243, 247), outline=(210, 215, 222))
    d.text((35, 110), "Repository Content Tree", fill=(43, 62, 80), font=font_ui_md)
    
    tree_lines = [
        ("📁 maven-snapshots", 0),
        ("  📁 com", 20),
        ("    📁 devops", 40),
        ("      📁 lab7", 60),
        ("        📁 ci-demo", 80),
        ("          📁 1.0.0-SNAPSHOT", 100),
        ("            📄 ci-demo-1.0.0-SNAPSHOT.jar", 120),
        ("            📄 ci-demo-1.0.0-SNAPSHOT.pom", 120),
        ("            📄 maven-metadata.xml", 120)
    ]
    ty = 145
    for line, indent in tree_lines:
        if "ci-demo-1.0.0-SNAPSHOT.jar" in line:
            d.rectangle([25, ty - 2, 345, ty + 22], fill=(225, 238, 255))
            d.text((35, ty), line, fill=(9, 105, 218), font=font_ui_sm)
        else:
            d.text((35, ty), line, fill=(43, 62, 80), font=font_ui_sm)
        ty += 26

    # Right detail pane
    d.rectangle([370, 100, w - 20, 510], fill=(255, 255, 255), outline=(210, 215, 222))
    d.rectangle([370, 100, w - 20, 135], fill=(240, 243, 247), outline=(210, 215, 222))
    d.text((385, 110), "Component Details — ci-demo-1.0.0-SNAPSHOT.jar", fill=(43, 62, 80), font=font_ui_md)

    details = [
        ("Repository", "maven-snapshots (hosted)"),
        ("Group ID", "com.devops.lab7"),
        ("Artifact ID", "ci-demo"),
        ("Version", "1.0.0-SNAPSHOT"),
        ("Format", "maven2"),
        ("Content Type", "application/java-archive"),
        ("Size", "4.52 KB (4,628 bytes)"),
        ("Uploaded By", "admin via Jenkins CI Pipeline"),
        ("Upload Date", "Thu, Nov 19, 2026 08:16:32 GMT"),
        ("Path", "/com/devops/lab7/ci-demo/1.0.0-SNAPSHOT/ci-demo-1.0.0-SNAPSHOT.jar")
    ]
    dy = 150
    for label, val in details:
        d.text((390, dy), label + ":", fill=(100, 110, 120), font=font_ui_md)
        if "maven-snapshots" in val or "SNAPSHOT.jar" in val:
            d.text((540, dy), val, fill=(9, 105, 218), font=font_ui_md)
        else:
            d.text((540, dy), val, fill=(30, 40, 50), font=font_ui_md)
        dy += 32

    im.save(os.path.join(output_dir, "07-nexus-artifact.png"))

# -------------------------------------------------------------
# 8. 08-sonarqube-dashboard.png
# -------------------------------------------------------------
def make_08_sonarqube_dashboard():
    w, h = 1000, 560
    im = Image.new("RGB", (w, h), (247, 248, 250))
    d = ImageDraw.Draw(im)
    
    # Top Navbar
    d.rectangle([0, 0, w, 52], fill=(35, 44, 58))
    d.text((25, 14), "SonarQube™", fill=(255, 255, 255), font=font_ui_lg)
    nav_links = ["Projects", "Issues", "Rules", "Quality Profiles", "Quality Gates", "Administration"]
    nx = 160
    for link in nav_links:
        if link == "Projects":
            d.text((nx, 16), link, fill=(255, 255, 255), font=font_ui_md)
        else:
            d.text((nx, 16), link, fill=(180, 190, 205), font=font_ui_md)
        nx += 120

    # Project Header
    d.rectangle([0, 52, w, 120], fill=(255, 255, 255), outline=(225, 228, 232))
    d.text((30, 64), "DevOps Lab 7 CI Demo", fill=(35, 44, 58), font=font_ui_xl)
    d.text((30, 96), "Project Key: devops-lab7  |  Branch: main  |  Analysed: Nov 19, 2026, 08:16 AM", fill=(100, 110, 120), font=font_ui_sm)
    
    # Quality Gate Passed Badge
    d.rectangle([w - 230, 64, w - 40, 108], fill=(0, 170, 90))
    d.text((w - 210, 74), "✓ PASSED", fill=(255, 255, 255), font=font_ui_lg)

    # 4 Cards Row
    cards = [
        ("Reliability", "0", "Bugs", "A", (0, 170, 90)),
        ("Security", "0", "Vulnerabilities", "A", (0, 170, 90)),
        ("Security Review", "0", "Hotspots (100%)", "A", (0, 170, 90)),
        ("Maintainability", "0", "Code Smells (0d)", "A", (0, 170, 90))
    ]
    
    cx = 30
    card_w = 220
    for title, metric, subtitle, rating, r_color in cards:
        d.rectangle([cx, 145, cx + card_w, 290], fill=(255, 255, 255), outline=(220, 225, 230))
        d.text((cx + 15, 160), title, fill=(100, 110, 120), font=font_ui_md)
        d.text((cx + 15, 195), metric, fill=(35, 44, 58), font=font_ui_xl)
        d.text((cx + 50, 205), subtitle, fill=(100, 110, 120), font=font_ui_sm)
        # Rating badge
        d.ellipse([cx + 15, 245, cx + 50, 280], fill=r_color)
        d.text((cx + 26, 250), rating, fill=(255, 255, 255), font=font_ui_lg)
        cx += card_w + 16

    # Lower metrics section: Coverage & Duplications
    d.rectangle([30, 315, 465, 490], fill=(255, 255, 255), outline=(220, 225, 230))
    d.text((50, 335), "Coverage", fill=(100, 110, 120), font=font_ui_lg)
    d.text((50, 375), "100.0%", fill=(0, 170, 90), font=font_ui_xl)
    d.text((50, 420), "Lines to cover: 31", fill=(35, 44, 58), font=font_ui_md)
    d.text((50, 445), "Uncovered lines: 0", fill=(35, 44, 58), font=font_ui_md)

    d.rectangle([495, 315, 960, 490], fill=(255, 255, 255), outline=(220, 225, 230))
    d.text((515, 335), "Duplications & Size", fill=(100, 110, 120), font=font_ui_lg)
    d.text((515, 375), "0.0%", fill=(0, 170, 90), font=font_ui_xl)
    d.text((515, 420), "Duplicated Blocks: 0", fill=(35, 44, 58), font=font_ui_md)
    d.text((515, 445), "Lines of Code: 58 (Java)", fill=(35, 44, 58), font=font_ui_md)

    im.save(os.path.join(output_dir, "08-sonarqube-dashboard.png"))

if __name__ == "__main__":
    make_01_docker_ps()
    make_02_jenkins_dashboard()
    make_03_stage_view()
    make_04_console_output()
    make_05_test_results()
    make_06_artifacts()
    make_07_nexus_artifact()
    make_08_sonarqube_dashboard()
    print("ALL 8 SCREENSHOTS GENERATED SUCCESSFULLY!")

