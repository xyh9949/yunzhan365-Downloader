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
---

## 🛠️ 方式二：浏览器油猴脚本

**无需安装 Python，无需配置环境，在浏览器中直接点击按钮即可下载。**

<https://greasyfork.org/zh-CN/scripts/560278-%E4%BA%91%E5%B1%95%E7%BD%91-yunzhan365-%E4%B8%80%E9%94%AE%E4%B8%8B%E8%BD%BD%E5%99%A8-v3-0-%E9%80%9A%E7%94%A8%E7%89%88>

### 1. 安装管理器
首先，请为您的浏览器安装 **Tampermonkey (篡改猴)** 扩展：
* [Chrome / Edge 版本](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
* [Firefox 版本](https://addons.mozilla.org/zh-CN/firefox/addon/tampermonkey/)

### 2. 安装脚本
1.  点击 Tampermonkey 图标 -> **“添加新脚本”**。
2.  删除编辑器中的所有默认代码。
3.  复制本项目提供的 `userscript.js` (或 v3.0+ 版本代码) 内容并粘贴。
4.  按 `Ctrl+S` 保存。

### 3. 如何使用
1.  在浏览器中打开任意云展网电子书阅读页面（例如：`https://book.yunzhan365.com/...`）。
2.  等待页面加载完毕，页面**右下角**会出现两个悬浮按钮：
    * **📦 下载图片打包 (ZIP)**
    * **📄 下载电子书 (PDF)**
3.  点击对应按钮，等待进度条走完，文件将自动保存到您的电脑。

---

## 🤝 贡献 (Contributing)

欢迎提交 Issue 或 Pull Request 来改进代码！

## ⚠️ 免责声明 (Disclaimer)

本工具仅用于自动化下载公开可访问的资源以进行离线阅读。使用者应对下载内容的使用方式负责。请尊重版权所有者，切勿传播受版权保护的付费内容。
