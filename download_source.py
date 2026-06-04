"""
通过腾讯云服务器下载并解压 Django3-Web 源码
"""
import paramiko
import time

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
REMOTE_DIR = '/home/ubuntu/django3web_src'

FILES = [
    'https://raw.githubusercontent.com/xyjw/Django3-Web/master/%E7%B2%BE%E9%80%9ADjango3%20web%E5%BC%80%E5%8F%91-1.zip',
    'https://raw.githubusercontent.com/xyjw/Django3-Web/master/%E7%B2%BE%E9%80%9ADjango3%20web%E5%BC%80%E5%8F%91-2.zip',
    'https://raw.githubusercontent.com/xyjw/Django3-Web/master/%E7%B2%BE%E9%80%9ADjango3%20web%E5%BC%80%E5%8F%91-3.zip',
    'https://raw.githubusercontent.com/xyjw/Django3-Web/master/%E7%B2%BE%E9%80%9ADjango3%20web%E5%BC%80%E5%8F%91-4.zip',
    'https://raw.githubusercontent.com/xyjw/Django3-Web/master/%E7%B2%BE%E9%80%9ADjango3%20web%E5%BC%80%E5%8F%91-5.zip',
]

def run_cmd(ssh, cmd, timeout=60):
    print(f"  CMD: {cmd[:120]}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out.strip():
        print(f"  OUT: {out.strip()[:500]}")
    if err.strip():
        print(f"  ERR: {err.strip()[:500]}")
    return out, err

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
    print("SSH connected")

    # Step 1: Create directory and download all parts
    run_cmd(ssh, f'mkdir -p {REMOTE_DIR}')

    for i, url in enumerate(FILES):
        print(f"\nDownloading part {i+1}/5...")
        run_cmd(ssh, f'curl -L -o {REMOTE_DIR}/part{i+1}.zip "{url}"', timeout=120)

    # Step 2: Check downloaded files
    print("\n=== Downloaded files ===")
    run_cmd(ssh, f'ls -lh {REMOTE_DIR}/')

    # Step 3: Try to extract each zip individually (they might be independent chapters)
    print("\n=== Trying to extract ===")
    run_cmd(ssh, f'cd {REMOTE_DIR} && for f in part*.zip; do echo "--- Extracting $f ---"; unzip -o -q "$f" -d extracted 2>&1 | tail -3; done')

    # Step 4: Show extracted structure
    print("\n=== Extracted structure ===")
    run_cmd(ssh, f'cd {REMOTE_DIR}/extracted && find . -maxdepth 3 -type d 2>/dev/null | head -60')

    # Step 5: Look for Django apps (directories with models.py)
    print("\n=== Django apps (models.py locations) ===")
    run_cmd(ssh, f'cd {REMOTE_DIR}/extracted && find . -name "models.py" -type f 2>/dev/null')

    # Step 6: Look for settings.py to understand project structure
    print("\n=== settings.py files ===")
    run_cmd(ssh, f'cd {REMOTE_DIR}/extracted && find . -name "settings.py" -type f 2>/dev/null')

    # Step 7: Look for manage.py to find project roots
    print("\n=== manage.py files ===")
    run_cmd(ssh, f'cd {REMOTE_DIR}/extracted && find . -name "manage.py" -type f 2>/dev/null')

    # Step 8: Look for requirements.txt
    print("\n=== requirements.txt ===")
    run_cmd(ssh, f'cd {REMOTE_DIR}/extracted && find . -name "requirements.txt" -type f 2>/dev/null')

    # Step 9: Look for urls.py
    print("\n=== urls.py files ===")
    run_cmd(ssh, f'cd {REMOTE_DIR}/extracted && find . -name "urls.py" -type f 2>/dev/null')

    ssh.close()
    print("\nDone!")

if __name__ == '__main__':
    main()
