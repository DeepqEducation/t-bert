from pathlib import Path

p = Path("./Ungian_2005_guliau-supin/轉換後資料")

writer = open("guliau_one_article_per_line.txt", "w")

# I skip "tbts-53-死人犯.txt" because it contains many weird characters.

for filename in p.rglob("*.txt"):
    print(filename)
    if filename.name == "tbts-53-死人犯.txt":
        continue
    with open(filename, "r") as f:
        for line in f:
            writer.write(line.strip() + ' ')
    writer.write('\n\n')

