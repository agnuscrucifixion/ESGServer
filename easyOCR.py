import os

from apryse_sdk.PDFNetPython import PDFNet, PDFDoc, OCRModule, OCROptions
from pdf2image import convert_from_path
import easyocr
from apryse_sdk import *
import apryse

def readOCR(path):
    PDFNet.Initialize("demo:1711213936836:7f0d66cd0300000000556913c63374cbc751215276bb2b70995b128e09")
    doc = PDFDoc()
    opts = OCROptions()
    opts.AddLang("rus")
    to_png(path)
    OCRModule.ImageToPDF(doc, "temp/images/page54.jpg", opts)
    doc.Save("uploads/page.pdf", 0)
    return apryse.convert_to_text("uploads/page.pdf")


def to_png(path):
    images = convert_from_path(path)
    for i, image in enumerate(images):
        image_path = f'temp/images/page{i}.jpg'
        image.save(image_path, 'JPEG')
        print(f'Saved image: {image_path}')


def process_images(path):
    to_png(path)
    text = ""
    reader = easyocr.Reader(['ru', 'en'], gpu=True)
    sorted_list = sorted(os.listdir('temp/images'), key=lambda x: int(x.split('.')[0][4:]))
    for filename in sorted_list:
        if filename.endswith('.jpg'):
            image_path = os.path.join('temp/images', filename)
            result = reader.readtext(image_path, detail=0, paragraph=True)
            print(image_path)
            for paragraph in result:
                if len(paragraph) > 2:
                    text += (paragraph + '\n\n')

    return text
