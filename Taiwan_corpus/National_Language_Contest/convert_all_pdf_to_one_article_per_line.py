import os 
import glob
import pdftotext
from pathlib import Path

all_file_path = glob.glob("contest_articles_pdf/*")
converted_filename = "contest_one_article_per_line.txt"
total_file_count = 0
converted_file_count = 0

converted_f = open(converted_filename, "w")

for file_path in all_file_path:
    file_path_without_extention = os.path.splitext(file_path)[0]
    file_path_without_first_folder = Path(file_path_without_extention).parts[1:]
    year = Path(file_path_without_extention).parts[1]
    print(f"Converting: {file_path}")

    with open(file_path, "rb") as f:
        pdf = pdftotext.PDF(f)
    
    
    for idx, page in enumerate(pdf):
        page = page.rsplit("\n", 2)[0]
        page = page.replace(" ", "").replace("\n", "")
        # print(page)
        converted_f.write(page)

    converted_f.write('\n\n')

    total_file_count += 1

print(f"total files: {total_file_count}")
print(f"converted files: {converted_file_count}")
print(f"empty and removed files: {total_file_count - converted_file_count}")