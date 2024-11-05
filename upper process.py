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


if __name__ == '__main__':
    input_path = r'D:\大学\学习\软件需求工程\spider\jobinfo.txt'
    output_path = r'D:\大学\学习\软件需求工程\spider\cleanedtext.txt'
    process_file(input_path, output_path)
