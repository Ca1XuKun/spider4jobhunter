import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_job_description(url, index):
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

def main():
    input_file = r"D:\大学\学习\软件需求工程\spider\linkList.txt"
    output_file = r"D:\大学\学习\软件需求工程\spider\jobinfo2.txt"

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")
        return

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
                job_description = scrape_job_description(url, index)
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
        print("程序结束。")

if __name__ == "__main__":
    main()