import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    input_path = r'D:\大学\学习\软件需求工程\spider\cleanedtext.txt'
    output_path = r'D:\大学\学习\软件需求工程\spider\upperProcess.txt'
    output_image_path = r'D:\大学\学习\软件需求工程\spider\wordcloud.png'

    keywords = extract_keywords(input_path, output_path)
    generate_wordcloud(keywords, output_image_path)
    print(f"Keywords have been saved to: {output_path}")
    print(f"Word cloud image has been saved to: {output_image_path}")