import os
import shutil


def check_argument(path):
    if os.path.exists(path):
        return True
    else:
        print(f"Путь '{path}' не существует.")
        return False


def clean_after():
    try:
        shutil.rmtree("temp")
        shutil.rmtree("uploads")
        print("Временная папка и все ее содержимое успешно удалены.")
    except FileNotFoundError:
        print("Временная папка не существует.")


def final_coupling(pathtexteasyocr, pathtextapryse):
    return pathtexteasyocr
