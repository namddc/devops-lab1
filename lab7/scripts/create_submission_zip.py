import os
import zipfile

base_dir = "D:/cô thương/lab7"
zip_path = "D:/cô thương/Lab7_NguyenVanNam_DTC235180129.zip"

files_to_pack = [
    "docker-compose.yml",
    "Jenkinsfile",
    "ho_ten_mssv.txt",
    "README.md"
]

dirs_to_pack = [
    "sample-java-app",
    "screenshots",
    "scripts"
]

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files_to_pack:
        full_path = os.path.join(base_dir, f)
        if os.path.exists(full_path):
            z.write(full_path, arcname=f)
            print(f"Added: {f}")
            
    for d in dirs_to_pack:
        full_dir = os.path.join(base_dir, d)
        for root, _, filenames in os.walk(full_dir):
            for fn in filenames:
                file_full = os.path.join(root, fn)
                rel_path = os.path.relpath(file_full, base_dir)
                z.write(file_full, arcname=rel_path)
                print(f"Added: {rel_path}")

print("ZIP PACKAGING COMPLETED:", zip_path)

