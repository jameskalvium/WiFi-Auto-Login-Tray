# Wi-Fi Auto Login Tray App

A lightweight Python-based system tray application that automatically logs in to your university Wi-Fi portal after checking internet connectivity. Designed to run silently in the background, it also integrates with Cloudflare WARP, provides manual controls from the tray menu, and delivers real-time system notifications.

---

## 🚀 Features

- ✅ **Auto login** to university Wi-Fi when internet is down
- 🌐 Detects and auto-connects **Cloudflare WARP**
- 🖥️ Runs silently from the **system tray**
- 🔁 **Manual re-login** available from tray menu
- 📢 System **notifications** using `plyer`
- 🧠 Option to **toggle auto-check** on/off
- 🪪 Configured to run on **Windows startup** using Task Scheduler

---

## 🛠️ Technologies Used

- **Python 3**
- [`pystray`](https://pypi.org/project/pystray/) – for system tray integration
- [`PIL`](https://pypi.org/project/Pillow/) – for icon handling
- [`plyer`](https://pypi.org/project/plyer/) – for system notifications
- [`requests`](https://pypi.org/project/requests/) – for HTTP login
- Windows **Task Scheduler** – for startup configuration

---

✨ Key Features
✅ Automatic Wi-Fi Login
Detects loss of internet connectivity and re-authenticates with the university portal.

Uses secure certificate-based HTTPS login.

🌐 WARP VPN Management
Automatically disconnects WARP before logging in (to avoid interference with captive portal).

Reconnects WARP after successful login.

🖥️ System Tray Application
Runs silently in the background with a tray icon.

Right-click menu includes:

Manual Re-Login

Toggle Auto Check On/Off

Exit Application

🔐 Singleton Instance Lock
Prevents multiple instances of the app from running using a temporary lock file.

🧩 Cross-Platform Structure (Windows focused)
Fully self-contained .exe build supported via PyInstaller.

Bundles resources (icon, certificate) using resource_path().

🛡️ SSL Certificate Handling
Secure login with a locally trusted .pem certificate file.

Uses requests with a custom certificate path for HTTPS verification.

📦 Lightweight and Dependency-Free Runtime
Background checks only every hour (configurable).

Minimal memory and CPU usage.



