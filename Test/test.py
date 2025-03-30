import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from urllib.parse import urljoin
import time
import os

# --- 配置 ---
# 基础 URL (根据之前的 HTML 注释推断)
BASE_URL = "https://iot.mi.com"
# 输出文件名
OUTPUT_FILE = "xiaomi_iot_documentation.md"
# 输出目录 (如果选择按文件输出)
# OUTPUT_DIR = "xiaomi_iot_docs_md"

# 延时（秒），避免过于频繁访问服务器
REQUEST_DELAY = 1

# --- 从之前提供的 HTML 中提取的结构 ---
# 注意：这里的 URL 是相对路径，需要与 BASE_URL 拼接
documentation_structure = [
    {
        "step_title": "01 了解",
        "categories": [
            {
                "category_title": "关于平台",
                "pages": [
                    {"title": "平台简介", "url": "/v2/new/doc/introduction/openness"},
                    {"title": "接入方式", "url": "/v2/new/doc/introduction/preparation/access_mode"},
                    {"title": "服务商接入", "url": "/v2/new/doc/introduction/solution/service"},
                    {"title": "解决方案中心", "url": "/v2/new/doc/introduction/solution/development-free"},
                    {"title": "模组选型", "url": "/v2/new/doc/introduction/knowledge/select_module"},
                ]
            },
            {
                "category_title": "基础知识",
                "pages": [
                    {"title": "平台架构", "url": "/v2/new/doc/introduction/tech_arch"},
                    {"title": "名词解释", "url": "/v2/new/doc/introduction/knowledge/explanation"},
                    {"title": "Spec 基础", "url": "/v2/new/doc/introduction/knowledge/spec"},
                    {"title": "BLE 基础", "url": "/v2/new/doc/introduction/knowledge/ble_basic"},
                    {"title": "BLE Mesh 基础", "url": "/v2/new/doc/introduction/knowledge/mesh_basic"},
                ]
            },
            {
                "category_title": "动手操作",
                "pages": [
                    {"title": "快速入门", "url": "/v2/new/doc/quick-started/standard-module"},
                ]
            }
        ]
    },
    {
        "step_title": "02 准备工作",
        "categories": [
            {
                "category_title": "平台接入准备",
                "pages": [
                    {"title": "明确产品类型", "url": "/v2/new/doc/introduction/preparation/product_type"},
                    {"title": "选择接入方式", "url": "/v2/new/doc/introduction/preparation/access_mode"}, # 注意：这个链接在步骤1也出现过
                    {"title": "确认接入方案", "url": "/v2/new/doc/introduction/preparation/access_type"},
                ]
            },
            {
                "category_title": "产品开发准备",
                "pages": [
                    {"title": "成为开发者", "url": "/v2/new/doc/configuration/signin/create-enterprise"},
                    {"title": "创建产品", "url": "/v2/new/doc/configuration/create"},
                    {"title": "定义功能", "url": "/v2/new/doc/resources-and-services/design/feature-define/feature-define"},
                    {"title": "其他产品设计规范", "url": "/v2/new/doc/resources-and-services/design/UED"},
                    {"title": "隐私协议", "url": "/v2/new/doc/resources-and-services/policy/secret"},
                ]
            }
        ]
    },
    {
        "step_title": "03 开发产品",
        "categories": [
            {
                "category_title": "平台配置",
                "pages": [
                    {"title": "基础配置", "url": "/v2/new/doc/configuration/configuration"},
                    {"title": "功能定义", "url": "/v2/new/doc/configuration/define-features"},
                    {"title": "扩展程序配置", "url": "/v2/new/doc/configuration/extension-development/extension-development"},
                    {"title": "固件配置", "url": "/v2/new/doc/configuration/firmware/firmware"},
                    {"title": "高阶配置", "url": "/v2/new/doc/configuration/advance-configure/network-distribution"},
                ]
            },
            {
                "category_title": "固件开发",
                "pages": [
                    {"title": "Wi-Fi 通用模组开发", "url": "/v2/new/doc/embedded-dev/module-dev/quickstart"},
                    {"title": "Wi-Fi SDK 开发", "url": "/v2/new/doc/embedded-dev/sdk-dev/quickstart"},
                    {"title": "Wi-Fi INC SDK 开发", "url": "/v2/new/doc/embedded-dev/inc-dev/c3_inc_quickstart"},
                    {"title": "Linux OT SDK 开发", "url": "/v2/new/doc/embedded-dev/linux-ot/quickstart"},
                    {"title": "BLE SDK 开发", "url": "/v2/new/doc/embedded-dev/ble-sdk/quickstart"},
                    {"title": "BLE Mesh SDK 开发", "url": "/v2/new/doc/embedded-dev/ble-mesh/quickstart"},
                ]
            },
            {
                "category_title": "扩展程序开发",
                "pages": [
                    {"title": "快速入门", "url": "/v2/new/doc/plugin/quickstart/quick-start"},
                    {"title": "扩展程序基本功能开发", "url": "/v2/new/doc/plugin/basic/basic-info"},
                    {"title": "API + Demo", "url": "/v2/new/doc/plugin/quickstart/plugin-principle#API%20和%20DEMO"}, # 注意 URL 中的 #
                    {"title": "组件", "url": "/v2/new/doc/plugin/basic/ui-component"},
                ]
            }
        ]
    },
    {
        "step_title": "04 自测与上线",
        "pages": [ # 没有子分类，直接列出页面
            {"title": "自测与预约（上线前完成）", "url": "/v2/new/doc/configuration/test-reservation"},
            {"title": "申请上线", "url": "/v2/new/doc/configuration/publish-product"},
        ]
    },
    {
        "step_title": "05 用户运营",
        "pages": [ # 没有子分类，直接列出页面
             {"title": "数据服务", "url": "/v2/new/doc/configuration/others/data"},
             {"title": "用户运营", "url": "/v2/new/doc/configuration/others/operate"},
             {"title": "日志查询", "url": "/v2/new/doc/configuration/others/log"},
        ]
    }
]

# --- 爬虫函数 ---
def fetch_and_convert_page(page_url):
    """获取单个页面的 HTML，提取内容并转换为 Markdown"""
    absolute_url = urljoin(BASE_URL, page_url)
    print(f"  Fetching: {absolute_url}")
    try:
        # 显式传入空的 proxies 字典来禁用代理
        proxies = {
          "http": None,
          "https": None,
        }
        response = requests.get(absolute_url, timeout=15,proxies=proxies)
        response.raise_for_status()  # 检查 HTTP 错误 (如 404, 500)
        response.encoding = response.apparent_encoding # 尝试正确解码

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- !!! 关键步骤：定位主要内容区域 !!! ---
        # 你需要检查实际页面的 HTML 结构来找到正确的选择器。
        # 常见的可能性包括：
        # - <main>...</main>
        # - <article>...</article>
        # - <div id="content">...</div>
        # - <div class="main-content">...</div>
        # - <div class="article-body">...</div>
        # 这里的 'div.doc-content-wrapper' 是一个基于之前代码片段的猜测，很可能需要修改！
        content_area = soup.find('div', id='reactMarkDownContent', class_='default_cursor_cs') # <--- ***需要验证和调整***

        if not content_area:
            # 如果找不到，尝试其他可能的选择器
            content_area = soup.find('main')
            if not content_area:
                 content_area = soup.find('article')
                 # 可以添加更多备选方案
            

        if content_area:
            # 清理可能不需要的部分（如导航按钮、编辑链接等），可选
            # for unwanted in content_area.find_all(['button', '.edit-link']):
            #     unwanted.decompose()

            html_content = str(content_area)
            # 转换为 Markdown，ATX 风格的标题 (#, ##)
            markdown_content = markdownify(html_content, heading_style="ATX").strip()
            return markdown_content
        else:
            print(f"  [Warning] Could not find main content area for {absolute_url}")
            return "*Error: Content area not found.*"

    except requests.exceptions.RequestException as e:
        print(f"  [Error] Failed to fetch {absolute_url}: {e}")
        return f"*Error fetching page: {e}*"
    except Exception as e:
        print(f"  [Error] Processing error for {absolute_url}: {e}")
        return f"*Error processing page: {e}*"

# --- 主逻辑 ---
final_markdown = f"# {BASE_URL} Documentation\n\n"

# 遍历结构并生成 Markdown
for step in documentation_structure:
    final_markdown += f"## {step['step_title']}\n\n"
    print(f"Processing Step: {step['step_title']}")

    if "categories" in step:
        for category in step['categories']:
            final_markdown += f"### {category['category_title']}\n\n"
            print(f"- Category: {category['category_title']}")
            for page in category['pages']:
                markdown_content = fetch_and_convert_page(page['url'])
                final_markdown += f"#### {page['title']}\n\n{markdown_content}\n\n"
                time.sleep(REQUEST_DELAY) # 等待一下
    elif "pages" in step: # 处理没有分类的步骤 (如 04, 05)
         for page in step['pages']:
            print(f"- Page: {page['title']}")
            markdown_content = fetch_and_convert_page(page['url'])
            # 注意：这里使用三级标题，因为它们直接隶属于二级步骤标题
            final_markdown += f"### {page['title']}\n\n{markdown_content}\n\n"
            time.sleep(REQUEST_DELAY) # 等待一下

# --- 写入文件 ---
try:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_markdown)
    print(f"\nSuccessfully generated Markdown file: {OUTPUT_FILE}")
except IOError as e:
    print(f"\n[Error] Could not write to output file {OUTPUT_FILE}: {e}")