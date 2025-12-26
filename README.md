# 📚 Yunzhan365 Book Downloader (云展网电子书下载器)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一个轻量级、交互式的 Python 命令行工具，用于从云展网（及类似架构网站）下载电子书。它能够自动抓取高清图片，将其归档保存，并最终合成高质量的 PDF 文档。

> **注意**：本项目仅供个人学习和技术研究使用，请勿用于商业用途或侵犯版权。

## ✨ 主要功能

* **🔍 智能链接解析**：支持输入电子书的阅读页链接（`index.html`）或任意一张图片的链接，脚本会自动推导资源路径。
* **💎 高清画质优先**：自动优先尝试下载 `/large/` 目录下的高清 JPG 图片；如果失败，则自动降级下载 `/mobile/` 目录下的普通图片（WebP/JPG）。
* **📂 自动归档管理**：
    * 自动为每本书创建独立的图片文件夹（防止图片散乱）。
    * 生成的 PDF 文件保存在根目录，方便查找。
* **🔄 格式自动转换**：支持自动将 `.webp` 格式转换为兼容性更好的 PDF 格式。
* **🚀 批量处理**：支持交互式循环下载，无需重启程序即可连续下载多本书籍。

## 🛠️ 环境要求

* Python 3.x
* 依赖库：`requests`, `Pillow`

## 🚀 快速开始

### 1. 克隆或下载本项目

```bash
git clone [https://github.com/yourusername/yunzhan-downloader.git](https://github.com/yourusername/yunzhan-downloader.git)
cd yunzhan-downloader

```

### 2. 安装依赖

使用 pip 安装所需的 Python 库：

```bash
pip install requests pillow

```

### 3. 运行工具

```bash
python download_book.py

```

## 📖 使用指南

1. 运行脚本后，程序会提示输入书籍网址。
2. **支持的链接格式示例**：
* 阅读页：`https://book.yunzhan365.com/qsrm/tsab/mobile/index.html`
* 图片链：`https://book.yunzhan365.com/qsrm/tsab/files/mobile/1.webp`


3. 输入链接并回车，程序将自动开始下载。
4. 下载完成后，您可以输入新的链接继续下载，或输入 `q` 退出。

## 📂 输出文件结构

脚本运行后，您的目录将会变得整洁有序：

```text
Project/
├── download_book.py          # 主程序
├── tsab_1672531200.pdf       # 生成的 PDF 文件 (位于根目录)
└── tsab_图片集_1672531200/    # 图片存放文件夹
    ├── 1.jpg
    ├── 2.webp
    ├── 3.jpg
    └── ...

```

## ⚙️ 高级配置

如果需要调整参数（如最大页数限制），请在代码顶部修改配置区域：

```python
# ================= 配置区域 =================
MAX_PAGES = 300  # 最大尝试页数，如果书很厚建议改大
# ===========================================

```

## 🤝 贡献 (Contributing)

欢迎提交 Issue 或 Pull Request 来改进代码！

## ⚠️ 免责声明 (Disclaimer)

本工具仅用于自动化下载公开可访问的资源以进行离线阅读。使用者应对下载内容的使用方式负责。请尊重版权所有者，切勿传播受版权保护的付费内容。
