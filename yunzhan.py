import requests
import os
import time
from PIL import Image
from io import BytesIO

# ================= 配置区域 =================
MAX_PAGES = 300  # 最大尝试页数
# ===========================================

def parse_url_to_base(user_url):
    """
    智能解析用户输入的URL，提取出书籍的根目录
    """
    user_url = user_url.split('?')[0]  # 去掉参数
    
    if "/mobile/" in user_url:
        root_url = user_url.split("/mobile/")[0]
    elif "/files/" in user_url:
        root_url = user_url.split("/files/")[0]
    else:
        root_url = user_url.rstrip("/")

    # 1. 高清大图路径 (通常是 jpg)
    high_res_template = f"{root_url}/files/large/{{}}.jpg"
    # 2. 手机端路径 (通常是 webp 或 jpg)
    mobile_template_webp = f"{root_url}/files/mobile/{{}}.webp"
    mobile_template_jpg = f"{root_url}/files/mobile/{{}}.jpg"
    
    return high_res_template, [mobile_template_webp, mobile_template_jpg]

def download_book(url):
    print(f"正在解析链接: {url}")
    high_res_url, mobile_urls = parse_url_to_base(url)
    
    # 生成唯一标识
    timestamp = int(time.time())
    # 提取书本ID作为名称一部分
    book_id = url.split('/')[-3] if len(url.split('/')) > 3 else "book"
    
    # 1. 创建存放图片的专属文件夹
    folder_name = f"{book_id}_图片集_{timestamp}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📂 已创建图片文件夹: {folder_name}")

    # PDF 文件名放在外面
    pdf_filename = f"{book_id}_{timestamp}.pdf"
    
    images = []
    print(f"🚀 准备下载... (图片存于 '{folder_name}'，PDF 存于当前目录)")
    print("-" * 40)

    for page in range(1, MAX_PAGES + 1):
        # 优先尝试高清版
        target_url = high_res_url.format(page)
        status_msg = "高清(Large)"
        file_ext = "jpg" # 默认后缀
        
        try:
            # 请求图片
            response = requests.get(target_url, timeout=5)
            
            # 如果高清版失败，尝试手机版
            if response.status_code != 200:
                for m_url in mobile_urls:
                    target_url = m_url.format(page)
                    response = requests.get(target_url, timeout=5)
                    if response.status_code == 200:
                        status_msg = "普通(Mobile)"
                        # 检查是 webp 还是 jpg
                        if target_url.endswith(".webp"):
                            file_ext = "webp"
                        else:
                            file_ext = "jpg"
                        break
            
            # 处理下载结果
            if response.status_code == 200:
                # A. 保存图片文件到文件夹
                image_filename = f"{page}.{file_ext}"
                image_path = os.path.join(folder_name, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(response.content)

                # B. 准备 PDF 数据 (在内存中转换，不影响保存的文件)
                img = Image.open(BytesIO(response.content))
                if img.mode != "RGB":
                    img = img.convert("RGB")
                images.append(img)
                
                print(f"✅ 第 {page} 页: 已保存为 {image_filename} [{status_msg}]")
            else:
                print(f"🏁 第 {page} 页下载失败，判定书籍结束。")
                break
                
        except Exception as e:
            print(f"❌ 第 {page} 页发生错误: {e}")
            break

    # 合成 PDF
    if images:
        print("-" * 40)
        print(f"正在将 {len(images)} 张图片合成为 PDF...")
        try:
            images[0].save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
            print(f"🎉 大功告成！")
            print(f"📄 PDF文件: {os.path.abspath(pdf_filename)}")
            print(f"📂 图片文件夹: {os.path.abspath(folder_name)}")
        except Exception as e:
            print(f"❌ 生成 PDF 失败: {e}")
    else:
        # 如果没下载到东西，把空文件夹删了免得占地方
        try:
            os.rmdir(folder_name)
        except:
            pass
        print("⚠️ 未找到任何页面，请检查链接是否正确。")
    print("\n" + "="*40 + "\n")

# 主循环
if __name__ == "__main__":
    print("云展网/电子书 PDF下载器 (含图片备份版)")
    print("功能：自动下载图片存入文件夹 + 生成 PDF")
    print("="*40)
    
    while True:
        user_input = input("输入书本网址:[例:https://.../mobile/index.html] (输入 'q' 退出)\n下载链接：").strip()
        
        if user_input.lower() == 'q':
            print("退出程序。")
            break
            
        if not user_input:
            continue
            
        try:
            download_book(user_input)
        except Exception as e:
            print(f"发生未知错误: {e}")