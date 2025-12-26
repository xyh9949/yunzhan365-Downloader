##下载链接支持以下两种
## https://book.eol.cn/books/xxxx/mobile/index.html
## https://book.yunzhan365.com/xxxx/xxxx/mobile/index.html

##自行安装相关库

## 注意：某些文件并未匹配

from PIL import Image
from io import BytesIO
import requests
import re
import os
import PIL


# 设置请求头
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}

# 创建会话
session = requests.session()

def download_image(image_url, base_url, page_num, total_pages):
    """
    下载单个图片并显示进度
    """
    # 构造完整的图片URL
    full_url = f"{base_url}/files/large/{image_url}"
    
    try:
        response = session.get(full_url, headers=headers)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        
        # 显示下载进度
        progress = (page_num + 1) / total_pages
        bar_length = 50
        filled_length = int(round(bar_length * progress))
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(f"\r下载进度: [{bar}] {progress:.2%}", end='', flush=True)
        
        return img
    except (requests.RequestException, PIL.UnidentifiedImageError):
        # 如果第一次尝试失败，进行第二次尝试
        image_url = image_url.replace('..\\', '').replace('\\', '/').replace('//', '/')
        image_url = image_url.lstrip('/')
        if image_url.startswith('files/large/'):
            image_url = image_url[len('files/large/'):]
        second_url = f'{base_url}/files/large/{image_url}'
        
        try:
            response = session.get(second_url, headers=headers)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            
            # 显示下载进度
            progress = (page_num + 1) / total_pages
            bar_length = 50
            filled_length = int(round(bar_length * progress))
            bar = "#" * filled_length + "-" * (bar_length - filled_length)
            print(f"\r下载进度: [{bar}] {progress:.2%}", end='', flush=True)
            
            return img
        except (requests.RequestException, PIL.UnidentifiedImageError) as e:
            print(f"\n下载图片 {page_num} 时出错: {str(e)}")
            return None

def process_book(book_url):
    """
    处理单本书籍的下载和PDF生成
    """
    try:
        # 获取初始页面
        response = session.get(book_url, headers=headers)
        response.raise_for_status()
        base_url = '/'.join(book_url.split('/')[:5])
        
        # 提取配置文件URL
        config_match = re.findall('src="javascript/config.js\?(.+?)"></script>', response.text, re.S)
        if config_match:
            config_url = f'{book_url.rsplit("/", 1)[0]}/javascript/config.js?{config_match[0]}'
            config_response = session.get(config_url, headers=headers)
            config_response.raise_for_status()
            
            # 提取书籍标题和图片URL
            title = re.findall('"title":"(.+?)"', config_response.text)[0]
            image_urls = re.findall('"n":\[\"(.+?)\"\]', config_response.text)
            
            print(f"{title}.pdf / 共{len(image_urls)}页")
            
            # 下载图片
            images = []
            for page_num, image_url in enumerate(image_urls):
                img = download_image(image_url, base_url, page_num, len(image_urls))
                if img:
                    images.append(img)
            
            print('\n开始制作并合并成PDF...')
            if images:
                images[0].save(f"./{title}.pdf", "PDF", resolution=100.0, save_all=True, append_images=images[1:])
                print(f"{os.getcwd()}/{title}.pdf")
            else:
                print("没有成功下载任何图片")
        else:
            print(book_url, '识别错误')
    except requests.RequestException as e:
        print(f"访问网站时出错: {str(e)}")
    except Exception as e:
        print(f"发生意外错误: {str(e)}")

if __name__ == '__main__':
    while True:
        book_url = input("输入书本网址:[例:https://book.eol.cn/books/xxxx/mobile/index.html] (输入 'q' 退出)\n下载链接：")
        if book_url.lower() == 'q':
            break
        process_book(book_url)
        choice = input("是否继续下载其他书本? (y/n): ")
        if choice.lower() != 'y':
            break
    print("程序已退出")