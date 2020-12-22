import os 
import glob
import pdftotext
from pathlib import Path

all_file_path = glob.glob("PDF/*/*")
total_file_count = 0
converted_file_count = 0

for file_path in all_file_path:
    file_path_without_extention = os.path.splitext(file_path)[0]
    file_path_without_first_folder = Path(file_path_without_extention).parts[1:]
    year = Path(file_path_without_extention).parts[1]
    converted_file_path = os.path.join("Plain_text", *file_path_without_first_folder) + ".txt"
    print(f"original  path: {file_path}")
    print(f"converted path: {converted_file_path}")
    with open(file_path, "rb") as f:
        pdf = pdftotext.PDF(f)
    

    Path(converted_file_path).parent.mkdir(parents=True, exist_ok=True)
    # for page in pdf:
        # print(page.rsplit("\n", 2)[0])
    with open(converted_file_path, "w") as f:
        for idx, page in enumerate(pdf):
            if year in ["2010", "2011", "2012"] and idx == 0:
                continue
            f.write(page.rsplit("\n", 2)[0])
    
    total_file_count += 1
    if os.stat(converted_file_path).st_size == 0:  
        print("Empty file, removing ",converted_file_path)  
        os.remove(converted_file_path)  
    else:
        converted_file_count += 1

print(f"total files: {total_file_count}")
print(f"converted files: {converted_file_count}")
print(f"empty and removed files: {total_file_count - converted_file_count}")