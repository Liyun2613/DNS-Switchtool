import tkinter as tk
import subprocess
import socket
import sys
import os
import ctypes

# --- 0. 自动管理员提权 ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def request_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

# --- 1. DNS 数据库 ---
DNS_DATA = {
    "🌐 公共推荐 DNS": {
        "114 DNS (首选)": ["114.114.114.114"],
        "114 DNS (备选)": ["114.114.115.115"],
        "阿里 AliDNS (首选)": ["223.5.5.5"],
        "阿里 AliDNS (备选)": ["223.6.6.6"],
        "百度 BaiduDNS": ["180.76.76.76"],
        "腾讯 DNSPod": ["119.29.29.29"],
        "CNNIC SDNS (首选)": ["1.2.4.8"],
        "CNNIC SDNS (备选)": ["210.2.4.8"],
        "Google DNS (首选)": ["8.8.8.8"],
        "Google DNS (备选)": ["8.8.4.4"],
        "IBM Quad9": ["9.9.9.9"]
    },
    "📡 全国各地电信": {
        "北京电信 1": ["219.141.136.10"],
        "广东电信 1": ["202.96.128.86"],
        "上海电信 1": ["202.96.209.133"],
        "江苏电信 1": ["218.2.2.2"],
        "浙江电信 1": ["202.101.172.35"],
        "湖南电信 1": ["222.246.129.80"]
    },
    "📡 全国各地联通": {
        "北京联通 1": ["123.123.123.123"],
        "广东联通 1": ["210.21.196.6"],
        "上海联通 1": ["210.22.70.3"],
        "四川联通 1": ["119.6.6.6"],
        "江苏联通 1": ["221.6.4.66"]
    },
    "📡 全国各地移动": {
        "江苏移动 1": ["221.131.143.69"],
        "安徽移动 1": ["211.138.180.2"],
        "山东移动 1": ["218.201.96.130"],
        "山东移动 2": ["211.137.191.26"]
    },
    "🎮 特殊优化 / Apple TV": {
        "Apple TV (上海电信)": ["180.153.225.136"],
        "Apple TV (杭州电信)": ["115.29.189.118"]
    }
}

# --- 2. 获取在线物理网卡 ---
def get_active_network_adapters():
    active_adapters = []
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        if local_ip != "127.0.0.1":
            ps_cmd = f"(Get-NetIPAddress -IPAddress '{local_ip}').InterfaceAlias"
            result = subprocess.run(['powershell', '-Command', ps_cmd],
                                    capture_output=True, text=True,
                                    encoding='utf-8', errors='ignore',
                                    startupinfo=startupinfo)
            default_iface = result.stdout.strip()
            if default_iface and len(default_iface) > 1:
                active_adapters.append(default_iface)
        virtual_keywords = ["VMware", "VirtualBox", "VPN", "Loopback", "Hyper-V", "Radmin", "Sakura", "vEthernet"]
        result = subprocess.run('wmic path Win32_NetworkAdapter where "NetConnectionStatus=2" get NetConnectionID /value',
                                shell=True, capture_output=True, text=True, encoding='gbk', errors='ignore',
                                startupinfo=startupinfo)
        for line in result.stdout.split('\n'):
            if 'NetConnectionID=' in line:
                name = line.split('=')[1].strip()
                if name and not any(kw in name for kw in virtual_keywords):
                    if name not in active_adapters:
                        active_adapters.append(name)
    except Exception:
        pass
    if not active_adapters:
        return ["WLAN", "以太网", "本地连接"]
    return active_adapters

# --- 3. 启动检查 ---
def startup_check():
    if not is_admin():
        request_admin()
    perm_root = tk.Tk()
    perm_root.withdraw()
    dialog = tk.Toplevel(perm_root)
    dialog.title("环境准备")
    dialog.geometry("400x180")
    dialog.overrideredirect(True)
    dialog.configure(bg="#16213e")
    dialog.attributes("-topmost", True)
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - 200
    y = (dialog.winfo_screenheight() // 2) - 90
    dialog.geometry(f"400x180+{x}+{y}")
    tk.Label(dialog, text="正在检测管理员权限...\n已自动提权，准备启动核心工具",
             bg="#16213e", fg="white", font=("微软雅黑", 11, "bold")).pack(pady=30)
    btn_frame = tk.Frame(dialog, bg="#16213e")
    btn_frame.pack(pady=10)
    def on_ok():
        dialog.destroy()
        perm_root.destroy()
    btn = tk.Button(btn_frame, text="确 定 (进入主程序)",
                    bg="#4CAF50", fg="white", font=("微软雅黑", 10),
                    activebackground="#45a049", relief="flat", cursor="hand2",
                    width=25, height=1, command=on_ok)
    btn.pack()
    dialog.bind("<Escape>", lambda e: on_ok())
    dialog.bind("<Button-1>", lambda e: on_ok())
    perm_root.mainloop()

# --- 4. 主界面 ---
class ModernDNSSwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("全能 DNS 切换工具")
        self.root.geometry("800x850")  # 加高，容纳恢复自动按钮
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0e1a")

        tk.Label(root, text="全网 DNS 解析服务器分选项工具", bg="#0f0e1a", fg="#FFFFFF",
                 font=("微软雅黑", 18, "bold")).place(x=400, y=30, anchor="center")

        active_adapters = get_active_network_adapters()
        self.iface_var = tk.StringVar(value=active_adapters[0])
        self.iface_menu = tk.OptionMenu(root, self.iface_var, *active_adapters)
        self.iface_menu.config(bg="#16213e", fg="white", font=("微软雅黑", 10),
                               activebackground="#16213e", relief="flat", highlightthickness=0, bd=0)
        self.iface_menu.place(x=230, y=80, width=180, anchor="center")

        self.combo_var = tk.StringVar(value=list(DNS_DATA.keys())[0])
        self.combo_menu = tk.OptionMenu(root, self.combo_var, *list(DNS_DATA.keys()))
        self.combo_menu.config(bg="#16213e", fg="white", font=("微软雅黑", 10),
                               activebackground="#16213e", relief="flat", highlightthickness=0, bd=0)
        self.combo_menu.place(x=570, y=80, width=200, anchor="center")
        self.combo_var.trace_add("write", self.update_list)

        self.list_data = []
        self.selected_index = -1
        self.scroll_offset = 0
        self.ROW_HEIGHT = 45
        self.is_dragging = False
        self.drag_start_y = 0

        list_container = tk.Frame(root, bg="#111126", width=700, height=450)
        list_container.place(x=400, y=360, anchor="center")
        list_container.pack_propagate(False)

        header_frame = tk.Frame(list_container, bg="#111126", height=40)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="DNS 名称", bg="#111126", fg="#4cc9f0",
                 font=("微软雅黑", 11, "bold"), anchor="w").place(x=30, y=10, width=300)
        tk.Label(header_frame, text="IP 解析地址", bg="#111126", fg="#4cc9f0",
                 font=("微软雅黑", 11, "bold"), anchor="w").place(x=360, y=10, width=300)

        self.canvas = tk.Canvas(list_container, bg="#111126", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_canvas = tk.Canvas(list_container, bg="#111126", width=16, highlightthickness=0)
        self.scrollbar_canvas.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollbar_canvas.bind("<Button-1>", self._start_drag)
        self.scrollbar_canvas.bind("<B1-Motion>", self._do_drag)
        self.scrollbar_canvas.bind("<ButtonRelease-1>", self._end_drag)

        # 主切换按钮
        self.btn_text = tk.StringVar(value="一键切换选中 DNS")
        self.btn = tk.Button(root, textvariable=self.btn_text, font=("微软雅黑", 12, "bold"),
                             bg="#4CAF50", fg="white", relief="flat", cursor="hand2",
                             command=self.change_dns)
        self.btn.place(x=400, y=660, width=220, height=45, anchor="center")

        # 新增：恢复 DHCP 自动 DNS 按钮
        self.btn_dhcp = tk.Button(root, text="恢复自动获取 DNS (DHCP)", font=("微软雅黑", 11, "bold"),
                                  bg="#3a5a8c", fg="white", relief="flat", cursor="hand2",
                                  command=self.restore_dhcp)
        self.btn_dhcp.place(x=400, y=725, width=220, height=42, anchor="center")

        # 高亮状态栏
        self.status_frame = tk.Frame(root, bg="#111126", bd=1, relief="solid")
        self.status_frame.place(x=400, y=795, anchor="center", width=650, height=32)
        self.status_label = tk.Label(self.status_frame, text="就绪 | 请从上方选择并切换 DNS",
                                     bg="#111126", fg="#6a7c92", font=("微软雅黑", 10, "bold"))
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        self.selected_dns = None
        self.update_list()

    def update_list(self, *args):
        self.list_data.clear()
        self.selected_index = -1
        self.scroll_offset = 0
        self.set_btn_state("一键切换选中 DNS")
        self.set_status("就绪 | 请从上方选择并切换 DNS", "normal")
        category = self.combo_var.get()
        if category in DNS_DATA:
            for name, ips in DNS_DATA[category].items():
                self.list_data.append((name, ips[0]))
        self._redraw()

    def _on_resize(self, event):
        self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        self.scrollbar_canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w == 1: w = 700
        if h == 1: h = 410
        total_height = len(self.list_data) * self.ROW_HEIGHT
        max_offset = max(0, total_height - h)
        self.scroll_offset = max(0, min(self.scroll_offset, max_offset))
        start_index = self.scroll_offset // self.ROW_HEIGHT
        end_index = min(len(self.list_data), (self.scroll_offset + h) // self.ROW_HEIGHT + 1)
        for i in range(start_index, end_index):
            name, ip = self.list_data[i]
            y = i * self.ROW_HEIGHT - self.scroll_offset
            bg_color = "#e94560" if i == self.selected_index else "#111126"
            txt_color = "white" if i == self.selected_index else "#e0e0e0"
            self.canvas.create_rectangle(0, y, w, y + self.ROW_HEIGHT, fill=bg_color, outline="")
            self.canvas.create_text(30, y + self.ROW_HEIGHT // 2, anchor="w", text=name,
                                    fill=txt_color, font=("微软雅黑", 11))
            self.canvas.create_text(360, y + self.ROW_HEIGHT // 2, anchor="w", text=ip,
                                    fill=txt_color, font=("微软雅黑", 11))
        if total_height > h:
            scroll_h = max(40, h * h / total_height)
            scroll_y = self.scroll_offset * (h - scroll_h) / max_offset
            self.scrollbar_canvas.create_rectangle(2, scroll_y, 14, scroll_y + scroll_h, fill="#4cc9f0", outline="")

    def _on_click(self, event):
        click_index = (event.y + self.scroll_offset) // self.ROW_HEIGHT
        if 0 <= click_index < len(self.list_data):
            self.selected_index = click_index
            self.selected_dns = self.list_data[click_index]
            self.set_btn_state(f"准备切换至: {self.selected_dns[0]}")
            self._redraw()

    def _on_mousewheel(self, event):
        self.scroll_offset -= (event.delta // 120) * 20
        self._redraw()

    def _start_drag(self, event):
        self.is_dragging = True
        self.drag_start_y = event.y

    def _do_drag(self, event):
        if not self.is_dragging:
            return
        y_offset = event.y - self.drag_start_y
        self.drag_start_y = event.y
        h = self.canvas.winfo_height()
        total_height = len(self.list_data) * self.ROW_HEIGHT
        if total_height <= h:
            return
        max_offset = total_height - h
        self.scroll_offset += y_offset * max_offset / h
        self._redraw()

    def _end_drag(self, event):
        self.is_dragging = False

    def set_btn_state(self, text):
        self.btn_text.set(text)
        actual_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff' or '\u0030' <= c <= '\u0039' or '\u0041' <= c <= '\u007a')
        new_width = max(200, actual_chars * 15 + 60)
        new_width = min(new_width, 700)
        self.btn.place_configure(width=new_width, x=400, y=660, anchor="center")
        self.btn.config(bg="#e94560" if "准备切换" in text else "#4CAF50")

    def set_status(self, text, state="normal"):
        self.status_label.config(text=text)
        if state == "success":
            self.status_frame.config(bg="#2ecc71")
            self.status_label.config(bg="#2ecc71", fg="#ffffff")
        elif state == "error":
            self.status_frame.config(bg="#e74c3c")
            self.status_label.config(bg="#e74c3c", fg="#ffffff")
        else:
            self.status_frame.config(bg="#111126")
            self.status_label.config(bg="#111126", fg="#6a7c92")

    def _run(self, cmd, hide=True):
        startupinfo = subprocess.STARTUPINFO()
        if hide:
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              encoding='gbk', errors='ignore', startupinfo=startupinfo)

    def change_dns(self):
        if self.selected_dns is None:
            self.set_status("⚠ 请先在下方列表中点击选择一行 DNS", "error")
            self.root.after(3000, lambda: self.set_status("就绪 | 请从上方选择并切换 DNS", "normal"))
            return
        dns_name, primary_ip = self.selected_dns
        target_iface = self.iface_var.get()
        if not target_iface or len(target_iface) < 1:
            self.set_status("⚠ 未检测到有效的物理网卡，请检查网络", "error")
            return
        try:
            self._run(f'netsh interface ip set dns name="{target_iface}" source=static addr={primary_ip} register=PRIMARY')
            self._run(f'netsh interface ip add dns name="{target_iface}" addr=8.8.8.8 index=2')
            self._run('ipconfig /flushdns')
            self.set_status(f"✔ 成功: 网卡 [{target_iface}] 已应用 {dns_name} : {primary_ip}", "success")
            self.root.after(5000, lambda: self.set_status("就绪 | 请从上方选择并切换 DNS", "normal"))
        except Exception as e:
            self.set_status("❌ 失败: 请以管理员身份运行该软件！", "error")
            self.root.after(5000, lambda: self.set_status("就绪 | 请从上方选择并切换 DNS", "normal"))

    def restore_dhcp(self):
        target_iface = self.iface_var.get()
        if not target_iface or len(target_iface) < 1:
            self.set_status("⚠ 未检测到有效的物理网卡，请检查网络", "error")
            return
        try:
            self._run(f'netsh interface ip delete dns name="{target_iface}" all')
            self._run(f'netsh interface ip set dns name="{target_iface}" source=dhcp')
            self._run('ipconfig /flushdns')
            self.set_status(f"✔ 成功: 网卡 [{target_iface}] 已恢复为 DHCP 自动获取 DNS", "success")
            self.root.after(5000, lambda: self.set_status("就绪 | 请从上方选择并切换 DNS", "normal"))
        except Exception as e:
            self.set_status("❌ 恢复失败: 请以管理员身份运行该软件！", "error")
            self.root.after(5000, lambda: self.set_status("就绪 | 请从上方选择并切换 DNS", "normal"))

if __name__ == "__main__":
    startup_check()
    root = tk.Tk()
    app = ModernDNSSwitcher(root)
    root.mainloop()