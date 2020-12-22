import json

with open("people_taigi_news.json", "r") as f:
    people_news = json.load(f)

with open("people_one_article_per_line.txt", "w") as f:
    for item in people_news:
        title = item['title']
        HLarticle = item["HLcontent"]
        POJarticle = item["POJcontent"]
        title = title.replace("【台語世界／錄音】", "").replace("【台語世界】", "")
        title = title + "。"
        HLarticle = HLarticle.replace("是按怎欲揀這篇：", "")
        f.write(title)
        if HLarticle.strip() != "":
            f.write(HLarticle + '\n\n')
        if POJarticle.strip() != "":
            f.write(POJarticle + '\n\n')

    