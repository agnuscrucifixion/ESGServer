import os
import subprocess
import re


def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0


def process_text(input_text):
    total_letters = sum(c.isalpha() for c in input_text)
    uppercase_letters = sum(c.isupper() for c in input_text)
    lines = input_text.split('\n')
    processed_text = []
    paragraph = []

    for line in lines:
        is_heading = sum(c.isupper() for c in line) > len(line) / 2

        if is_heading:
            if paragraph:
                processed_text.append(' '.join(paragraph).replace('¬ ', '').replace('¬', '') + '.')
                paragraph = []
            processed_text.append(line.strip())
        else:
            paragraph.append(line.strip())

    if paragraph:
        processed_text.append(' '.join(paragraph).replace('¬ ', '').replace('¬', ''))

    return '\n'.join(processed_text)


def check_string_in_file(file_path, string_to_check):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if string_to_check in line:
                    return False
        return True
    except FileNotFoundError:
        print("Файл не найден.")
        return False
    except IOError:
        print("Произошла ошибка при чтении файла.")
        return False


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
            if check_string_in_file(file_path, "PDFTron PDF2Text: This page is skipped when running in the demo mode."):
                temp = process_text(input_file.read())
                text += temp + "\n\n"
    print("Создан текстовый файл от Apryse")
    return text
