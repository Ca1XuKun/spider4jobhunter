# 仅完成了爬取链接，将链接中的内容爬取下来并进行了简单的文本处理
# 仍然存在问题：爬取的内容中包含了大量的无用信息，需要进一步处理

import os
import re
from operator import index
from random import random

import jieba
import nltk
from matplotlib import pyplot as plt
from nltk import word_tokenize
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wordcloud import WordCloud

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

def fetch_text_from_url(url, index):
    # 启动 Edge 浏览器
    browser = webdriver.Edge()
    # 打开 URL
    browser.get(url)
    try:
        # 定义可能的选择器列表
        selectors = [
            (By.CLASS_NAME, "describtion__detail-content"),
            (By.CSS_SELECTOR, ".main-body__block.main-body__block--pb32")
        ]

        job_description = None

        for selector in selectors:
            try:
                # 等待特定的<div>标签加载完成
                description_content = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located(selector)
                )
                # 获取文本内容
                job_description = description_content.text
                break  # 如果找到内容，跳出循环
            except:
                # 如果未找到当前选择器的元素，继续尝试下一个
                continue

        if job_description:
            return job_description
        else:
            print(f"处理URL失败: {url}\n错误信息: 未找到指定的元素。")
            # 保存出错时的页面截图，方便调试
            browser.save_screenshot(f'screenshot_{index}.png')
            return None
    except Exception as e:
        print(f"处理URL失败: {url}\n错误信息: {e}")
        # 保存出错时的页面截图，方便调试
        browser.save_screenshot(f'screenshot_{index}.png')
        return None
    finally:
        # 关闭浏览器
        browser.quit()
regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '天津']
def clean_text(text):
    # Tokenization
    tokens_zh = jieba.lcut(text)  # Chinese tokenization
    tokens_en = word_tokenize(text)  # English tokenization

    # Normalization
    tokens_zh = [token.lower() for token in tokens_zh if token.isalnum()]
    tokens_en = [token.lower() for token in tokens_en if token.isalnum()]

    # Stop Words Removal
    stop_words_zh = {
        '的', '了', '在', '和', '与', '及', '等', '上', '下', '以上', '以下', '能够', '具有',
        '相关', '熟练', '掌握', '熟悉', '负责', '参与', '要求', '进行', '良好', '工作', '能力',
        '优先', '背景', '等等', '等级', '主要', '岗位', '招聘', '单位', '经验', '专业', '知识',
        '技能', '本科', '学士', '学历', '职责', '任职', '资格', '精通', '使用', '语言', '工具',
        '了解', '善于', '团队', '协作', '沟通', '思维', '热爱', '有强烈', '意识', '具备', '精神',
        '独立', '完成', '基础', '我', '也', '就', '不', '人', '都', '一个', '我们', '你', '到',
        '说', '要', '会', '着', '没有', '看', '好', '自己', '这', '那', '还', '可以', '对', '很',
        '但', '去', '她', '他', '它', '里', '后', '而', '又', '能', '过', '得', '做', '让', '给',
        '从', '想', '用', '地', '再', '只', '如', '被', '并', '其', '此', '已', '些', '什么', '来',
        '因为', '所以', '而且', '或者', '如果', '虽然', '但是', '然后', '那么', '就是', '还有', '以及',
        '并且', '而是', '需要', '将', '例如', '任务', '通过', '包括', '岗位职责', '任职要求',
        '职位描述', '职位职责', '描述', '上', '下', '与', '下', '过', '等', '等', '上', '下', '以上',
        '以下', '上', '下', '能', '下', '过', '得', '做', '让', '给', '从', '想', '用', '地','熟练掌握','年龄',
        '任职要求','的', '和', '有', '在', '是', '了', '我', '也', '就', '不', '人', '都', '一个', '上', '我们',
        '你', '到', '说', '要', '会', '着', '没有', '看', '好', '自己', '这', '那', '还', '可以', '对', '很',
        '但', '去', '与', '她', '他', '它', '里', '后', '而', '又', '能', '下', '过', '得', '做', '让', '给',
        '从', '想', '用', '地', '再', '只', '如', '被', '并', '其', '此', '已', '些', '什么', '来', '因为',
        '所以', '而且', '或者', '或', '如果', '虽然', '但是', '然后', '那么', '就是', '还有', '以及', '并且',
        '以上学历','业务'

    }
    stop_words_en = set(nltk.corpus.stopwords.words('english'))

    tokens_zh = [token for token in tokens_zh if token not in stop_words_zh and token not in regions]
    tokens_en = [token for token in tokens_en if token not in stop_words_en]

    # Remove Meaningless Words
    meaningless_words = re.compile(r'\b\d+\b|\b[a-zA-Z]{5,}\b')
    tokens_zh = [token for token in tokens_zh if not meaningless_words.match(token)]
    tokens_en = [token for token in tokens_en if not meaningless_words.match(token)]

    # Combine tokens
    cleaned_text = ' '.join(tokens_zh + tokens_en)
    return cleaned_text
def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned_line = clean_text(line)
            outfile.write(cleaned_line + '\n')

def extract_keywords(input_path, output_path, topK=50):
    # 读取文件内容
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 数据清洗
    text = text.replace('\n', '').replace('\r', '').replace(' ', '')

    # 关键词提取
    keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)

    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        for keyword, weight in keywords:
            f.write(f"{keyword} {weight}\n")

    return keywords

def generate_wordcloud(keywords, output_image_path):
    # 生成词云
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        background_color='white',
        width=800,
        height=600,
        max_words=100,
        max_font_size=80,
        colormap='viridis',
        margin=2
    )
    wordcloud.generate_from_frequencies(dict(keywords))

    # 显示词云
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_image_path)
    plt.show()
# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    input_path = r'D:\大学\学习\软件需求工程\spider\cleanedtext.txt'
    output_path = r'D:\大学\学习\软件需求工程\spider\upperProcess.txt'
    output_image_path = r'D:\大学\学习\软件需求工程\spider\wordcloud.png'
    spider4url()
    filepath = r"D:\大学\学习\软件需求工程\spider\linkList.txt"
    urls = read_urls(filepath)

    input_file = r"D:\大学\学习\软件需求工程\spider\linkList.txt"
    output_file = r"D:\大学\学习\软件需求工程\spider\jobinfo2.txt"

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        urls = f.readlines()

    total = len(urls)
    print(f"共有 {total} 个URL需要处理。")

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for index, url in enumerate(urls, 1):
                url = url.strip()
                if not url:
                    continue
                print(f"正在处理第 {index}/{total} 个URL: {url}")
                job_description = fetch_text_from_url(url, index)
                if job_description:
                    outfile.write(job_description + '\n\n')
                else:
                    outfile.write(f"URL {url} 解析失败。\n\n")
                # 刷新缓冲区，确保数据写入磁盘
                outfile.flush()
                # 为了防止触发反爬虫机制，添加随机延时
                time.sleep(random.uniform(1, 3))
    except KeyboardInterrupt:
        print("\n程序被手动中止，已保存已获取的数据。")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        print("文本详情爬取结束。")

    process_file(input_path, output_path)

    keywords = extract_keywords(input_path, output_path)
    generate_wordcloud(keywords, output_image_path)
    print(f"Keywords have been saved to: {output_path}")
    print(f"Word cloud image has been saved to: {output_image_path}")
    print("程序结束。")