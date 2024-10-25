# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:33:14 2024

@author:
"""


import pandas as pd
import jieba
import jieba.posseg as pseg
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as image
import csv


# 读取Excel文件
df = pd.read_excel("C:\\Users\\Lenovo_yishu\\Desktop\\rmw_ai_pages.xlsx")

# 加载词库
jieba.load_userdict('AI dictionary.txt')

# 加载停用词
with open('stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# 分词与词性标注
def segment_text(text):
    words = pseg.cut(text)
    return [(word, flag) for word, flag in words if word not in stopwords]

# 提取News Title和News Summary
texts = df['News Title'].tolist() + df['News Summary'].tolist()

# 分词和词性标注
segments = [segment_text(text) for text in texts]

# 统计词频
word_freq = {}
for seg in segments:
    for word, flag in seg:
        if '\n' not in word and len(word)>1:
            word_freq[word] = word_freq.get(word,0)+1


#将词频结果导入excel中
df = pd.DataFrame([word_freq])

# 转置DataFrame
df_transposed = df.transpose()

# 将转置后的DataFrame写入Excel文件
df_transposed.to_excel('output.xlsx',  header=False, index=True, engine='openpyxl')

print("data has been saved in output.xlsx")
    

mask = np.array(image.open('graph.png'))  
# 生成词云
wc = WordCloud(
    font_path='simhei.ttf',  # 需要提供中文字体
    width=800, height=400,
    background_color='white',
    stopwords=stopwords,
    mask=mask
).generate_from_frequencies(word_freq)

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
##########################################################
# Part Ⅱ: Pre-process and vectorize the documents
##########################################################

