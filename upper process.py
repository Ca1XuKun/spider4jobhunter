import re
import jieba
import nltk
from nltk import word_tokenize

# Define a list of known regions to filter out
regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '天津']

def clean_text(text):
    # Tokenization
    tokens_zh = jieba.lcut(text)  # Chinese tokenization
    tokens_en = word_tokenize(text)  # English tokenization

    # Normalization
    tokens_zh = [token.lower() for token in tokens_zh if token.isalnum()]
    tokens_en = [token.lower() for token in tokens_en if token.isalnum()]

    # Stop Words Removal
    stop_words_zh = {'的', '和', '有', '在', '是', '了', '我', '也', '就', '不', '人', '都', '一个', '上', '我们', '你', '到', '说', '要', '会', '着', '没有', '看', '好', '自己', '这', '那', '还', '可以', '对', '很', '但', '去', '与', '她', '他', '它', '里', '后', '而', '又', '能', '下', '过', '得', '做', '让', '给', '从', '想', '用', '地', '再', '只', '如', '被', '并', '其', '此', '已', '些', '什么', '来', '因为', '所以', '而且', '或者', '如果', '虽然', '但是', '然后', '那么', '就是', '还有', '以及', '而且', '并且', '而是'}
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

if __name__ == '__main__':
    input_path = r'D:\大学\学习\软件需求工程\spider\text.txt'
    output_path = r'D:\大学\学习\软件需求工程\spider\cleaned_text.txt'
    process_file(input_path, output_path)

