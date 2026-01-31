# Thay thế cho cả cell cài đặt và chạy
import os
import time
import subprocess

# 1. Cài đặt
print("--- 1. Cài đặt OpenSSH & Tailscale ---")
os.system("apt-get update -y > /dev/null")
os.system("apt-get install -y openssh-server curl > /dev/null")
os.system("curl -fsSL https://tailscale.com/install.sh | sh")

# 2. Cấu hình & Chạy Daemon (FIX LỖI QUAN TRỌNG TẠI ĐÂY)
print("--- 2. Khởi động Tailscaled (Userspace Mode) ---")
os.system("mkdir -p /var/run/tailscale")
os.system("mkdir -p /var/lib/tailscale")

# Chạy tailscaled với cờ --tun=userspace-networking để tránh lỗi thiếu device
# Dùng nohup để đảm bảo process không bị kill
subprocess.Popen(
    ["nohup", "tailscaled", "--tun=userspace-networking", "--socket=/var/run/tailscale/tailscaled.sock", "--port=41641"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    preexec_fn=os.setpgrp
)

# Đợi daemon khởi động thật sự
print("Đang đợi dịch vụ khởi chạy...", end="")
for i in range(10):
    if os.path.exists("/var/run/tailscale/tailscaled.sock"):
        print(" OK!")
        break
    time.sleep(1)
    print(".", end="")
else:
    print("\nLỖI: Tailscaled không chịu chạy. Vui lòng thử lại.")

# 3. Kết nối
print("\n--- 3. Đăng ký máy ---")
auth_cmd = f"tailscale up --authkey={TAILSCALE_AUTH_KEY} --ssh --hostname={HOSTNAME} --accept-routes"
status = os.system(auth_cmd)

if status == 0:
    print("\n" + "="*40)
    print(f"✅ THÀNH CÔNG THẬT SỰ RỒI!")
    print(f"SSH Command: ssh root@{HOSTNAME}")
    print("="*40)
else:
    print("\n❌ Vẫn lỗi ở bước xác thực. Kiểm tra lại Key của bạn.")
