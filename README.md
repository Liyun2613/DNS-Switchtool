[Uploading README.md…]()
# DNS-Switchtool

> 一个简单好用的 Windows DNS 切换工具，帮你快速切换网络配置。
> A simple and easy-to-use DNS switching tool for Windows to quickly switch network configurations.

---

## 功能特点 / Features

- **一键切换** - 预设多组 DNS 方案，双击即可切换，无需繁琐配置
- **轻量高效** - 纯 Python 实现，无需安装额外依赖
- **简单易用** - 图形化/命令行操作，小白也能轻松上手
- **灵活配置** - 支持自定义 DNS 服务器地址

---

## 使用方法 / Usage

### 快速开始

1. 确保你的电脑已安装 [Python](https://www.python.org/downloads/)（建议 3.8+）
2. 将本仓库克隆到本地：
   ```bash
   git clone https://github.com/Liyun2613/DNS-Switchtool.git
   ```
3. 进入项目目录，运行主程序：
   ```bash
   cd DNS-Switchtool
   python Switchtool.py
   ```

### 配置 DNS 方案

在工具界面中，你可以预设多组 DNS 配置（如：电信、联通、移动、Google DNS 等），需要时一键切换。

---

## 项目结构 / Project Structure

```
DNS-Switchtool/
├── Switchtool.py          # 主程序入口
├── ...                    # 配置文件与资源
└── README.md              # 项目说明文档
```

---

## 常用 DNS 参考 / DNS Reference

| 服务商 | 首选 DNS | 备选 DNS |
|--------|----------|----------|
| 阿里 | 223.5.5.5 | 223.6.6.6 |
| 腾讯 | 119.29.29.29 | 182.254.116.116 |
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |

---

## 注意事项 / Notes

- 切换 DNS 需要 **管理员权限**，请以管理员身份运行程序
- 部分网络环境可能限制 DNS 修改，工具会自动检测并提示
- 修改后如未立即生效，可尝试刷新 DNS 缓存：`ipconfig /flushdns`

---

## 许可 / License

本项目仅供学习交流使用。

---

## 作者 / Author

**Liyun2613**

如果这个项目对你有帮助，欢迎点个 Star 支持一下！
