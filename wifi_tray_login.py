import os
import sys
import time
import threading
import subprocess
import requests
import psutil
from pystray import Icon, MenuItem, Menu
from PIL import Image
from plyer import notification

# ===============================
# Configuration
# ===============================
USERNAME = "246320"
PASSWORD = "66354038"
LOGIN_URL = "https://sophoscukc.christuniversity.in:8090/login.xml"
CHECK_INTERVAL = 3600  # 1 hour

# Global flag to toggle auto-check
auto_check_enabled = True

# ===============================
# Resource path helper for .exe builds
# ===============================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ===============================
# Set SSL certificate path
# ===============================
cert_path = resource_path("ssl_ca_kengeri.pem")
os.environ["SSL_CERT_FILE"] = cert_path

# ===============================
# Tray icon image loader
# ===============================
def create_image():
    return Image.open(resource_path("wifi_icon.ico"))

# ===============================
# Check for internet connection (lightweight)
# ===============================
def is_connected():
    try:
        res = requests.head("http://clients3.google.com/generate_204", timeout=5)
        return res.status_code == 204
    except:
        return False

# ===============================
# Login request
# ===============================
def login():
    try:
        payload = {
            'mode': '191',
            'username': USERNAME,
            'password': PASSWORD,
            'a': int(time.time() * 1000),
            'producttype': '0'
        }
        print(f"Using cert file: {cert_path}")
        response = requests.post(
            LOGIN_URL,
            data=payload,
            timeout=10,
            verify=cert_path
        )
        if response.status_code == 200 and "successfully logged in" in response.text:
            print("✅ Login successful")
            ensure_warp_connected()
        else:
            print("❌ Login failed")
    except Exception as e:
        print(f"⚠️ Login exception: {e}")

# ===============================
# WARP management
# ===============================

def ensure_warp_running():
    try:
        subprocess.run(["warp-cli", "enable-always-on"], timeout=5)
    except Exception as e:
        print(f"⚠️ WARP service not ready: {e}")


def ensure_warp_connected():
    try:
        print("🔍 Checking WARP status...")
        status = subprocess.run(["warp-cli", "status"], capture_output=True, text=True, timeout=5)
        print("⚙️ WARP status output:\n", status.stdout)

        if "Connected" in status.stdout:
            print("🌐 WARP is already connected.")
        else:
            print("🔌 WARP not connected. Trying to reconnect...")

            # Step 1: Ensure WARP is enabled
            subprocess.run(["warp-cli", "enable-always-on"], capture_output=True, text=True, timeout=5)

            # Step 2: Connect WARP
            connect = subprocess.run(["warp-cli", "connect"], capture_output=True, text=True, timeout=10)
            print("📡 WARP connect stdout:", connect.stdout)
            print("📡 WARP connect stderr:", connect.stderr)

            # Step 3: Recheck status
            recheck = subprocess.run(["warp-cli", "status"], capture_output=True, text=True, timeout=5)
            print("🔄 WARP recheck:\n", recheck.stdout)
    except Exception as e:
        print(f"⚠️ WARP connect error: {e}")



def disconnect_warp():
    try:
        subprocess.run(["warp-cli", "disconnect"], timeout=5)
        print("🔌 WARP disconnected")
    except Exception as e:
        print(f"⚠️ Failed to disconnect WARP: {e}")

# ===============================
# Background Auto Login Thread
# ===============================
def auto_login_loop():
    while True:
        if auto_check_enabled:
            if not is_connected():
                print("🔌 Internet disconnected. Disconnecting WARP before login...")
                disconnect_warp()

                time.sleep(3)  # wait for WARP to fully disconnect

                login()

                time.sleep(3)  # give the network time to stabilize

                ensure_warp_connected()
            else:
                print("✅ Internet active")
        time.sleep(CHECK_INTERVAL)


# ===============================
# System Tray Icon Setup
# ===============================
def start_tray_icon():
    def on_exit(icon, item):
        icon.stop()

    def on_manual_login(icon, item):
        login()

    def on_toggle_auto_check(icon, item):
        global auto_check_enabled
        auto_check_enabled = not auto_check_enabled
        # notify("Auto Check Toggled", f"Now: {'On' if auto_check_enabled else 'Off'}")

    icon = Icon("Wi-Fi Auto Login")
    icon.icon = create_image()
    icon.menu = Menu(
        MenuItem("Manual Re-Login", on_manual_login),
        MenuItem(lambda item: f"Auto Check: {'On' if auto_check_enabled else 'Off'}", on_toggle_auto_check),
        MenuItem("Exit", on_exit)
    )
    threading.Thread(target=auto_login_loop, daemon=True).start()
    icon.run()

# ===============================
# Singleton Lock to prevent multiple instances
# ===============================
def check_already_running():
    lockfile = os.path.join(os.getenv("TEMP"), "wifi_autologin.lock")
    if os.path.exists(lockfile):
        try:
            with open(lockfile, 'r') as f:
                old_pid = int(f.read().strip())
            if psutil.pid_exists(old_pid):
                print("🚫 Another instance is already running.")
                sys.exit(0)
            else:
                print("⚠️ Stale lock detected. Removing and continuing...")
                os.remove(lockfile)
        except Exception as e:
            print(f"⚠️ Error checking lock file: {e}")
            os.remove(lockfile)
    with open(lockfile, 'w') as f:
        f.write(str(os.getpid()))

# ===============================
# Entry point
# ===============================
if __name__ == "__main__":
    check_already_running()
    start_tray_icon()
