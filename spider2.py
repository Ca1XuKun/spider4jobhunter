import requests
from bs4 import BeautifulSoup

def scrape_job_descriptions(urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for url in urls:
            url = url.strip()
            try:
                response = requests.get(url)
                response.raise_for_status()  # 检查请求是否成功
                soup = BeautifulSoup(response.text, 'html.parser')

                # 找到包含职位描述的div元素
                job_description_div = soup.find('div', class_='describtion__detail-content')

                if job_description_div:
                    # 提取岗位职责和任职要求
                    job_description_text = job_description_div.get_text(separator='\n', strip=True)

                    file.write(f"URL: {url}\n")
                    file.write("职位描述:\n")
                    file.write(job_description_text + "\n")
                    file.write("="*80 + "\n")
                    print(f"URL: {url} - 爬取成功")
                else:
                    print(f"URL: {url} - 职位描述未找到")
            except Exception as e:
                print(f"URL: {url} - 请求失败: {e}")

def main():
    # 读取链接列表
    with open(r'D:\大学\学习\软件需求工程\spider\linkList.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # 爬取职位描述并进行处理
    output_file = r'D:\大学\学习\软件需求工程\spider\spider4txt.txt'
    scrape_job_descriptions(urls, output_file)

if __name__ == "__main__":
    main()