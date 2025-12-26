import os
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor

# 图片处理库 (用于合成 PDF)
from PIL import Image

# 自动化浏览器模块
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ================= 配置区域 =================
MAX_THREADS = 16
# ===========================================

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

def fetch_book_data(url):
    print(f"🕵️‍♂️ 正在启动隐形浏览器 (分析页面)...")
    options = Options()
    
    # 【修改点1】开启无头模式 (隐身)
    options.add_argument("--headless") 
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        
        print("⏳ 等待加密模块解密 (10 秒)...")
        time.sleep(2) 
        
        # 万能提取脚本
        extract_script = """
        try {
            var candidates = [
                window.fliphtml5_pages, window.configForPages,
                (window.bookConfig && window.bookConfig.pages),
                (window.htmlConfig && window.htmlConfig.pages),
                (window.sliderConfig && window.sliderConfig.pages)
            ];
            var pages = [];
            for(var i=0; i<candidates.length; i++) {
                if(candidates[i] && Array.isArray(candidates[i]) && candidates[i].length > 0) {
                    pages = candidates[i]; break;
                }
            }
            if(pages.length === 0 && window.bookConfig) {
                 for(var key in window.bookConfig) {
                    if(Array.isArray(window.bookConfig[key]) && window.bookConfig[key].length > 0) {
                        var first = window.bookConfig[key][0];
                        if(first && (first.path || first.url || first.image)) {
                            pages = window.bookConfig[key]; break;
                        }
                    }
                }
            }
            var result = [];
            for(var i=0; i<pages.length; i++) {
                var p = pages[i];
                if(typeof p === 'string') result.push(p);
                else if(p.path) result.push(p.path);
                else if(p.url) result.push(p.url);
                else if(p.image) result.push(p.image);
                else if(p.n && p.n[0]) result.push(p.n[0]);
            }
            return { title: document.title, pages: result };
        } catch(e) { return null; }
        """
        return driver.execute_script(extract_script)
    except Exception as e:
        print(f"❌ 浏览器错误: {e}")
        return None
    finally:
        if driver: driver.quit()

def probe_correct_url(base_url, first_path):
    # 去掉文件名中的参数
    clean_name = first_path.split('?')[0].lstrip("/")
    
    print(f"🔍 正在探测路径 (测试文件: {clean_name})...")
    
    base_urls = [base_url]
    if "bookh." in base_url:
        base_urls.append(base_url.replace("bookh.", "book."))

    patterns = [
        "{base}/files/large/{path}",
        "{base}/files/mobile/{path}",
        "{base}/{path}",
        "{base}/large/{path}",
        "{base}/mobile/{path}"
    ]

    for base in base_urls:
        for pattern in patterns:
            test_url = pattern.format(base=base, path=clean_name)
            try:
                r = requests.get(test_url, headers=get_headers(), timeout=5, stream=True, allow_redirects=True)
                if r.status_code == 200:
                    print(f"✅ 路径通了！")
                    return pattern.format(base=base, path="{path}")
            except:
                pass
    return None

def download_image_task(args):
    url_template, filename, save_path, index = args
    try:
        clean_name = filename.split('?')[0].lstrip("/")
        final_url = url_template.format(path=clean_name)
        
        r = requests.get(final_url, headers=get_headers(), timeout=15)
        
        if r.status_code == 200:
            with open(save_path, "wb") as f: f.write(r.content)
            print(f"✅ P{index} OK")
            return
        else:
            print(f"❌ P{index} 失败 ({r.status_code})")
    except Exception as e:
        print(f"❌ P{index} 错误: {e}")

# 【修改点2】新增 PDF 生成函数
def generate_pdf(folder_path, pdf_name):
    print("-" * 30)
    print(f"📑 正在合成 PDF: {pdf_name}")
    
    images = []
    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.webp', '.png'))]
    # 按文件名排序 (确保 001, 002 顺序正确)
    files.sort()
    
    if not files:
        print("❌ 文件夹为空，无法生成 PDF")
        return

    for f in files:
        try:
            full_path = os.path.join(folder_path, f)
            img = Image.open(full_path)
            # PDF 不支持 RGBA (透明通道)，如果是 WebP 需要转 RGB
            if img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
        except Exception as e:
            print(f"⚠️ 跳过损坏图片: {f}")

    if images:
        try:
            output_path = os.path.join(folder_path, pdf_name)
            images[0].save(output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
            print(f"🎉 PDF 生成成功！文件位于: {output_path}")
        except Exception as e:
            print(f"❌ PDF 生成失败: {e}")
    else:
        print("❌ 没有有效的图片用于合成 PDF")

def main():
    print("云展网下载器 v11.0 (全自动隐身 + PDF)")
    print("="*40)
    
    while True:
        url = input("请输入链接 (q 退出):\n>>> ").strip()
        if url.lower() == 'q': break
        if not url: continue
        
        # 1. 解密
        data = fetch_book_data(url)
        if not data or not data.get("pages"):
            print("❌ 解密失败，未获取到页面。")
            continue
            
        pages = data["pages"]
        title = data.get("title", "book")
        print(f"✅ 提取到 {len(pages)} 页。")
        
        # 2. 确定基准 URL
        base_url = url.split("?")[0]
        if "/mobile/" in base_url: base_url = base_url.split("/mobile/")[0]
        elif "/files/" in base_url: base_url = base_url.split("/files/")[0]
        else: base_url = os.path.dirname(base_url)
        
        # 3. 智能探测
        url_template = ""
        if not pages[0].startswith("http"):
            url_template = probe_correct_url(base_url, pages[0])
            if not url_template:
                print("❌ 所有路径尝试均失败。")
                continue
        else:
            url_template = "{path}" 
        
        # 4. 准备下载
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
        folder = f"{safe_title}_{int(time.time())}"
        os.makedirs(folder, exist_ok=True)
        
        tasks = []
        for i, p in enumerate(pages):
            ext = "webp"
            if ".jpg" in p: ext = "jpg"
            if ".png" in p: ext = "png"
            
            save_path = os.path.join(folder, f"{i+1:03d}.{ext}")
            tasks.append((url_template, p, save_path, i+1))
            
        print(f"🚀 启动下载...")
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(download_image_task, tasks)
        
        # 5. 生成 PDF
        generate_pdf(folder, f"{safe_title}.pdf")
        
        print("🎉 全部流程结束！\n")

if __name__ == "__main__":
    main()