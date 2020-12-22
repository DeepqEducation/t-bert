import json

with open("Khin-hoan_2010_pojbh/pojbh.json", "r") as f:
    pojbh_json = json.load(f)


writer = open("pojbh_one_article_per_line.txt", "w")
for item in pojbh_json:
    HL = item['hanlo']
    TL = item['tailo']
    if len(HL):
        HL_content = " ".join(HL)
        writer.write(HL_content + '\n\n')
    if len(TL):
        TL_content = " ".join(TL)
        writer.write(TL_content + '\n\n')
    