import json

with open("pts_taigi_news.json", "r") as f:
    pts_news = json.load(f)

with open("pts_one_article_per_line.txt", "w") as f:
    for item in pts_news:
        title = item['title']
        article = item['content']
        title = title.replace(" ", "，") + "。"
        f.write(title+article+'\n\n')

    