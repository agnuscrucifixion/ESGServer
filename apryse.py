import os
import subprocess
import re


def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0


def convert_to_text(path):
    text = ""
    apryse_text_dir = "temp/apryse_text"
    try:
        subprocess.run(["pdf2text", "-o", apryse_text_dir, path], check=True)
        print("Файл PDF успешно конвертирован в текст и сохранен в множество.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации файла PDF: {e}")
        return

    text_files = [f for f in os.listdir(apryse_text_dir) if f.endswith(".txt")]
    text_files_sorted = sorted(text_files, key=lambda x: int(x.split('_')[1].split('.')[0]))

    for text_file in text_files_sorted:
        file_path = os.path.join(apryse_text_dir, text_file)
        with open(file_path, "r", encoding="utf-8") as input_file:
            text += input_file.read().strip() + "\n\n"

    print("Создан текстовый файл от Apryse")
    return text
