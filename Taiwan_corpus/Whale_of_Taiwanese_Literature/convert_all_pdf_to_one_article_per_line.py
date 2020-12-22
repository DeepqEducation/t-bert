import re
import os
import glob
import pdftotext
from pathlib import Path

all_file_path = glob.glob("PDF/*/*")
total_file_count = 0
converted_file_count = 0

converted_file_path = open("whale_one_article_per_line.txt", "w")

for file_path in all_file_path:
    file_path_without_extention = os.path.splitext(file_path)[0]
    file_path_without_first_folder = Path(
        file_path_without_extention).parts[1:]
    year = Path(file_path_without_extention).parts[1]
    print(f"original  path: {file_path}")
    with open(file_path, "rb") as f:
        pdf = pdftotext.PDF(f)

    for idx, page in enumerate(pdf):
        if year in ["2010", "2011", "2012"] and idx == 0:
            continue
        page = page.rsplit("\n", 2)[0]
        for line in page.split('\n'):
            converted_file_path.write(re.sub(r' +', ' ', line+' '))
    if page.strip() != "":
        converted_file_path.write('\n\n')
    total_file_count += 1


print(f"total files: {total_file_count}")
