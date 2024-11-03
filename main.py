# 仅完成了爬取链接，将链接中的内容爬取下来并进行了简单的文本处理
# 仍然存在问题：爬取的内容中包含了大量的无用信息，需要进一步处理

import os
import re
import time
import jieba
import nltk
from nltk import word_tokenize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 设置爬取后的文件名
filename = "linkList.txt"
# 设置爬取后的文件存储路径
filepath = r"D:\大学\学习\软件需求工程\spider"
# 设置爬取后的文件的完整路径
full_path = os.path.join(filepath, filename)

textfile = "text.txt"
text_full_path = os.path.join(filepath, textfile)

def spider4url():
    # 启动 Edge 浏览器
    browser = webdriver.Edge()
    # 设置要访问的 URL
    url_base = "https://www.zhaopin.com/sou/jl736/kwCLO66RJ32PHPG/p"
    uer_page = 1
    url = url_base + str(uer_page)
    # 打开 URL
    browser.get(url)
    # 等待 3 秒以确保页面加载完成
    time.sleep(3)
    # 设置浏览器编码为 utf-8
    browser.encoding = "utf-8"
    # 使用 BeautifulSoup 解析页面源代码
    soup = BeautifulSoup(browser.page_source, "html.parser")
    # 查找所有 class 为 'jobinfo__top' 的 div 标签
    div_tags = soup.find_all("div", class_='jobinfo__top')
    # 打开一个文件进行写入
    with open(full_path, 'w', encoding='utf-8') as file:
        count = 0
        # 爬取20页数据（20*10）
        for uer_page in range(1, 21):
            # 遍历所有找到的 div 标签
            for i in div_tags:
                print("正在爬取第", count, "条数据")
                # 获取第一个 a 标签的 href 属性
                href = i.find_all("a")[0]["href"]
                # 将 href 写入文件
                file.write(href + '\n')
                count += 1
        print("共爬取到", count, "条数据")

def read_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def fetch_text_from_url(url):
    # Initialize the WebDriver (Edge in this case)
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')  # Run in headless mode
    browser = webdriver.Edge(options=options)

    try:
        # Open the URL
        browser.get(url)

        # Wait for the page to load and the specific element to be present
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        return soup.get_text()
    finally:
        browser.quit()

def clean_text(text):
    # Check if stopwords and punkt are already downloaded
    nltk_data_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'nltk_data')
    if not os.path.exists(os.path.join(nltk_data_path, 'corpora', 'stopwords')):
        nltk.download('stopwords')
    if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers', 'punkt')):
        nltk.download('punkt')
    if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers', 'punkt_tab')):
        nltk.download('punkt_tab')

    # Tokenization
    tokens_zh = jieba.lcut(text)  # Chinese tokenization
    tokens_en = word_tokenize(text)  # English tokenization

    # Normalization
    tokens_zh = [token.lower() for token in tokens_zh if token.isalnum()]
    tokens_en = [token.lower() for token in tokens_en if token.isalnum()]

    # Stop Words Removal
    stop_words_zh = {'的', '和', '有'}  # Add more Chinese stop words as needed
    stop_words_en = set(nltk.corpus.stopwords.words('english'))

    tokens_zh = [token for token in tokens_zh if token not in stop_words_zh]
    tokens_en = [token for token in tokens_en if token not in stop_words_en]

    # Remove Meaningless Words
    meaningless_words = re.compile(r'\b\d+\b|\b[a-zA-Z]{5,}\b')
    tokens_zh = [token for token in tokens_zh if not meaningless_words.match(token)]
    tokens_en = [token for token in tokens_en if not meaningless_words.match(token)]

    # Combine tokens
    cleaned_text = ' '.join(tokens_zh + tokens_en)
    return cleaned_text

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    spider4url()
    filepath = r"D:\大学\学习\软件需求工程\spider\linkList.txt"
    urls = read_urls(filepath)

    for url in urls:
        print(f"Processing URL: {url}")
        text = fetch_text_from_url(url)
        cleaned_text = clean_text(text)
        with open(text_full_path, 'a', encoding='utf-8') as file:
            file.write(cleaned_text + '\n')