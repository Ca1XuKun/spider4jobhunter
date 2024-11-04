from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_job_description(url):
    # 启动 Edge 浏览器
    browser = webdriver.Edge()
    # 打开 URL
    browser.get(url)
    try:
        # 如果内容在 iframe 中，先切换到 iframe（根据实际情况修改）
        # browser.switch_to.frame("iframe的名称或ID")

        # 等待特定的<div>标签加载完成
        description_content = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "describtion__detail-content"))
        )

        # 获取文本内容
        job_description = description_content.text
        print("职位描述:", job_description)
    except Exception as e:
        print("未找到指定的内容:", e)
    finally:
        # 关闭浏览器
        browser.quit()

def main():
    # 替换为目标页面的URL
    url = "http://jobs.zhaopin.com/CCL1206970160J40589170310.htm?refcode=4019&srccode=401901&preactionid=35972025-1077-41d5-b5e2-2e26145f573e"
    scrape_job_description(url)

if __name__ == "__main__":
    main()