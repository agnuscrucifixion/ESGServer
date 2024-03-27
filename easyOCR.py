import os
from pdf2image import convert_from_path
import easyocr


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
                text += (paragraph + '\n\n')

    return text
