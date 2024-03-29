import os
import subprocess
import re


def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0


def process_text(input_text):
    lines = input_text.split('\n')
    processed_text = []
    paragraph = []

    for line in lines:
        if len(line) > 2:
            is_heading = sum(c.isupper() for c in line) > len(line) / 2

            if is_heading:
                if paragraph:
                    point = ''
                    if paragraph[len(paragraph) - 1] == '':
                        point = '.'
                    processed_text.append(' '.join(paragraph).replace('¬ ', '').replace('¬', '') + point)
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
    name_pdf = path.split('\\')[len(path.split('\\')) - 1].split('.')[0]
    text = ""
    apryse_text_dir = "temp/apryse_text"
    demo_string = "PDFTron PDF2Text: This page is skipped when running in the demo mode."

    try:
        subprocess.run(["pdf2text", "--output", apryse_text_dir, path], check=True)
        print("Файл PDF успешно конвертирован в текст и сохранен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации файла PDF: {e}")
        return

    text_files = [f for f in os.listdir(apryse_text_dir) if f.endswith(".txt")]
    text_files_sorted = sorted(text_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
    print(text_files_sorted)
    for text_file in text_files_sorted:
        file_path = os.path.join(apryse_text_dir, text_file)
        while True:
            content = ""
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            if demo_string in content:
                page_number = text_file.split('_')[1].split('.')[0]
                os.remove(file_path)
                print(page_number)
                subprocess.run(
                    ["pdf2text", "--output", apryse_text_dir, "--pages", page_number, path],
                    check=True)
                os.rename(os.path.join(apryse_text_dir, name_pdf + ".txt"),
                          os.path.join(apryse_text_dir, name_pdf + "_" + page_number + ".txt"))
            else:
                break
    for text_file in text_files_sorted:
        file_path = os.path.join(apryse_text_dir, text_file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                if demo_string not in content:
                    text += process_text(content) + "\n\n"
                else:
                    print(content)

    print("Создан текстовый файл от Apryse")
    return text
