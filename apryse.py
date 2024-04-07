import os
import subprocess
import re


def clean_text_if_needed(text, ocr):
    cleaned_text = re.sub(r" {3,}", "\n", text)
    cleaned_text_lines = cleaned_text.splitlines(keepends=True)
    if ocr:
        cleaned_text = '\n\n'.join(line for line in cleaned_text_lines if len(line.strip()) >= 4
                                   and re.search(r"[а-яА-Яa-zA-Z]", line)
                                   and not re.fullmatch(r"[0-9.,\s]+", line.strip()))
        return cleaned_text
    else:
        cleaned_text = '\n'.join(line for line in cleaned_text_lines if len(line.strip()) >= 4
                                 and re.search(r"[а-яА-Яa-zA-Z]", line)
                                 and not re.fullmatch(r"[0-9.,\s]+", line.strip()))
        return cleaned_text


def merge_lines(text):
    lines = text.split('\n')
    merged_text = ""
    lines = list(filter(lambda s: s.strip(), lines))
    print(lines)
    for i in range(len(lines) - 1):
        current_line = lines[i].strip()
        next_line = lines[i + 1].strip()
        if (current_line.endswith(tuple('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя,:')) and
            not next_line.startswith(tuple('0123456789'))) or \
                (current_line.endswith(',') and next_line[0].isupper()):
            merged_text += current_line + ' '
        else:
            merged_text += current_line + '\n'
    merged_text += lines[-1].strip()
    return merged_text


def convert_to_text(path):
    print(path)
    name_pdf = os.path.splitext(os.path.basename(path))[0]
    print(name_pdf)
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
                print(content)
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
                    text += re.sub(r"[^\w\s,.?!]", "", content + "\n")
                else:
                    print(content)

    print("Создан текстовый файл от Apryse")
    text = clean_text_if_needed(text, False)
    text = merge_lines(text)
    return text
