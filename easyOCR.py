import os
from PIL import Image, ImageEnhance

from apryse_sdk.PDFNetPython import PDFNet, PDFDoc, OCRModule, OCROptions
from pdf2image import convert_from_path
import easyocr
from apryse_sdk import *
import apryse


def readOCR(path):
    final_text = ""
    PDFNet.Initialize("demo:1711213936836:7f0d66cd0300000000556913c63374cbc751215276bb2b70995b128e09")
    doc = PDFDoc()
    opts = OCROptions()
    opts.AddLang("rus")
    to_png(path)
    convert_folder_to_grayscale("temp/images")
    text_files = [f for f in os.listdir("temp/images") if f.endswith(".jpg")]
    text_files_sorted = sorted(text_files, key=lambda x: int(x.split('page')[1].split('.')[0]))
    for i in text_files_sorted:
        print(i)
        OCRModule.ImageToPDF(doc, f"temp/images/{i}", opts)
    doc.Save(f"uploads/gray.pdf", 0)
    final_text = apryse.convert_to_text("uploads/gray.pdf")
    return final_text


def to_png(path):
    images = convert_from_path(path)
    for i, image in enumerate(images):
        image_path = f'temp/images/page{i}.jpg'
        image.save(image_path, 'JPEG')
        print(f'Saved image: {image_path}')


def convert_folder_to_grayscale(folder_path):
    from PIL import Image
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(full_path)
                grayscale_image = image.convert("L")

                enhancer = ImageEnhance.Contrast(grayscale_image)
                enhanced_image = enhancer.enhance(2)

                enhanced_image.save(full_path, dpi=(300, 300))
                print(
                    f'Изображение {filename} успешно преобразовано в оттенки серого с повышенной контрастностью и сохранено.')
            except Exception as e:
                print(f'Ошибка при обработке изображения {filename}: {e}')


def process_images(path):
    to_png(path)
    convert_folder_to_grayscale("temp/images")
    text = ""
    reader = easyocr.Reader(['ru', 'en'], gpu=True)
    sorted_list = sorted(os.listdir('temp/images'), key=lambda x: int(x.split('.')[0][4:]))
    for filename in sorted_list:
        if filename.endswith('.jpg'):
            image_path = os.path.join('temp/images', filename)
            result = reader.readtext(image_path, detail=0, paragraph=True)
            print(image_path)
            temp = ""
            for paragraph in result:
                if len(paragraph) > 2:
                    temp += paragraph + "\n"
            text += (apryse.process_text(temp) + '\n\n')

    return text
