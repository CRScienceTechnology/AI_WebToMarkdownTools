import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging
import os

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# 设置代理（如果需要）
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def fetch_dynamic_content(url):
    """使用 Selenium 获取动态加载的内容"""

    # 使用 webdriver_manager 自动管理 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)
        logging.info(f"Opened URL: {url}")
        # 使用显式等待代替固定时间的 sleep
        wait = WebDriverWait(driver, 20)
        # 等待页面加载完成
        time.sleep(3)

        content_area = wait.until(EC.presence_of_element_located((By.ID, 'reactMarkDownContent')))

        # 获取渲染后的 HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 查找目标内容
        content_area = soup.find('div', id='reactMarkDownContent')

        if content_area:
            return str(content_area)
        else:
            logging.warning("Content area not found.")
            return None

    except Exception as e:
        logging.error(f"Error fetching dynamic content: {e}")
        return None

    finally:
        driver.quit()
        logging.info("Browser closed.")

# 示例用法
url = "https://iot.mi.com/v2/new/doc/introduction/openness"  # 替换为你要抓取的 URL
content = fetch_dynamic_content(url)

if content:
    print(content)
    # 将content保存到文件
else:
    print("Could not find content.")