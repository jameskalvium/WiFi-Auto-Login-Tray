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



