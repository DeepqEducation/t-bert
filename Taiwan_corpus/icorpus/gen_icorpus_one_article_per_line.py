import json
import yaml

with open("icorpus/icorpus.yaml") as f:
    data = yaml.load(f)

icorpus_original = open("icorpus_ka1_han3-ji7/語料/自動標人工改漢字.txt", "r")

shift = [0] * len(data)
shift[0] = -1
shift[2] = 2
shift[260] = 1
shift[417] = -1
shift[473] = -1

out_f = open("icorpus_one_article_per_line.txt", "w")
for article_idx, item in enumerate(data):
    if article_idx > 2566:
        break
    sentence_count = len(item['華語'])
    
    article = ""
    for i in range(sentence_count+shift[article_idx]):
        line = icorpus_original.readline().replace(" ", "").strip()
        if i == 1:
            continue
        article += line
        
        if i == 0:
            article += "。"

        # Because first article does not have punctuations
        if article_idx == 0:
            article += "，"

    out_f.write(article + "\n\n")