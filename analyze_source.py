"""
分析 Django3-Web 源码结构 - 详细读取 chapter11 和其他章节
"""
import paramiko

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
SRC_DIR = '/home/ubuntu/django3web_src/extracted'

def run_cmd(ssh, cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out, err

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
    print("Connected")

    # 1. Full directory tree of chapter11
    print("\n========== CHAPTER 11 FULL TREE ==========")
    out, _ = run_cmd(ssh, f'cd {SRC_DIR}/chapter11/babys && find . -type f | grep -v __pycache__ | grep -v .idea | grep -v migrations | sort')
    print(out)

    # 2. Read chapter11 models
    for app in ['index', 'commodity', 'shopper']:
        print(f"\n========== chapter11/babys/{app}/models.py ==========")
        out, _ = run_cmd(ssh, f'cat {SRC_DIR}/chapter11/babys/{app}/models.py')
        print(out)

    # 3. Read chapter11 views
    for app in ['index', 'commodity', 'shopper']:
        print(f"\n========== chapter11/babys/{app}/views.py ==========")
        out, _ = run_cmd(ssh, f'cat {SRC_DIR}/chapter11/babys/{app}/views.py')
        print(out)

    # 4. Read chapter11 urls
    for app in ['index', 'commodity', 'shopper']:
        print(f"\n========== chapter11/babys/{app}/urls.py ==========")
        out, _ = run_cmd(ssh, f'cat {SRC_DIR}/chapter11/babys/{app}/urls.py')
        print(out)

    # 5. Read chapter11 main urls
    print("\n========== chapter11/babys/babys/urls.py ==========")
    out, _ = run_cmd(ssh, f'cat {SRC_DIR}/chapter11/babys/babys/urls.py')
    print(out)

    # 6. Read chapter11 settings
    print("\n========== chapter11/babys/babys/settings.py ==========")
    out, _ = run_cmd(ssh, f'cat {SRC_DIR}/chapter11/babys/babys/settings.py')
    print(out)

    # 7. Check templates
    print("\n========== chapter11 templates ==========")
    out, _ = run_cmd(ssh, f'cd {SRC_DIR}/chapter11/babys && find . -name "*.html" | grep -v __pycache__ | sort')
    print(out)

    # 8. Check for other chapters with unique apps (not babys)
    print("\n========== Other chapter directories (not babys) ==========")
    out, _ = run_cmd(ssh, f'cd {SRC_DIR} && for d in chapter*/; do echo "=== $d ==="; find "$d" -maxdepth 3 -type d | grep -v __pycache__ | grep -v .idea | grep -v babys | head -20; done')
    print(out)

    # 9. chapter6 sub-projects (6.4, 6.5, 6.6)
    print("\n========== Chapter 6 special projects ==========")
    out, _ = run_cmd(ssh, f'cd {SRC_DIR}/chapter6 && find . -type f | grep -v __pycache__ | grep -v .idea | grep -v migrations | sort')
    print(out)

    # 10. chapter1 and chapter2 unique content
    for ch in ['chapter1', 'chapter2', 'chapter3']:
        print(f"\n========== {ch} structure ==========")
        out, _ = run_cmd(ssh, f'cd {SRC_DIR}/{ch} && find . -type f | grep -v __pycache__ | grep -v .idea | grep -v migrations | sort')
        print(out)

    ssh.close()

if __name__ == '__main__':
    main()
