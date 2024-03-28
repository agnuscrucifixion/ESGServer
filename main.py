import os
import easyOCR
import apryse
import util
from flask import Flask, request, send_file
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


#def remove_unwanted_lines(text):
    #unwanted_text = "PDFTron PDF2Text: This page is skipped when running in the demo mode."
    #lines = text.splitlines()
    #filtered_lines = [line for line in lines if unwanted_text not in line]
    #print(filtered_lines)
    #return "\n".join(filtered_lines)


def write_texts_to_files(textapryse, easyOCRtext):
    textapryse_filename = os.path.join("final", 'textapryse_output.txt')
    easyOCRtext_filename = os.path.join("final", 'easyOCR_output.txt')
    with open(textapryse_filename, 'w', encoding='utf-8') as file:
        file.write(textapryse)

    with open(easyOCRtext_filename, 'w', encoding='utf-8') as file:
        file.write(easyOCRtext)


@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    text_filename = 'final/final.txt'
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        print(filepath)
        file.save(filepath)
        textapryse = apryse.convert_to_text(filepath)
        #textapryse = remove_unwanted_lines(textapryse)
        #easyOCRtext = easyOCR.process_images(filepath)
        easyOCRtext = ""
        write_texts_to_files(textapryse, easyOCRtext)

        util.clean_after()
        final = util.final_coupling(textapryse, easyOCRtext)
        with open(text_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(final)
        return send_file(text_filename, as_attachment=True, download_name=text_filename)


if __name__ == '__main__':
    if not os.path.exists("temp"):
        os.mkdir("temp")
        os.mkdir("final")
        os.mkdir("temp/images")
    app.run(debug=True, host='0.0.0.0', port=5000)
