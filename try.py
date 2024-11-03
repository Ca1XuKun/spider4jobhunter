import requests
from bs4 import BeautifulSoup


def scrape_job_description(url):
    # 请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    # 发起请求
    response = requests.get(url, headers=headers)
    requests.encoding = "utf-8"
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 定位到特定的<div>标签
        description_content = soup.find("div", class_="job-info__desc job-info__desc-mt12")

        # 获取文本内容
        if description_content:
            job_description = description_content.get_text(strip=True)
            print("职位描述:", job_description)
        else:
            print("未找到指定的内容")
    else:
        print("请求失败，状态码:", response.status_code)
        


def main():
    # 替换为目标页面的URL
    url = "https://xiaoyuan.zhaopin.com/job/CC578396330J40609655612?refcode=4019&srccode=401901&preactionid=35972025-1077-41d5-b5e2-2e26145f573e"
    scrape_job_description(url)


if __name__ == "__main__":
    main()
