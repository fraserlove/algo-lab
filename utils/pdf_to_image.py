'''
PDF to Image Converter
Author: Fraser Love, me@fraser.love
Created: 2020-06-13
Latest Release: v1.0.2, 2023-08-10
Python: v3.10.12
Dependencies: pdf2image

Converts multiple pdf's to images (JPEG format) and stores them in a logical folder structure under the desired image directory.

Usage:  Update the pdf_dir and img_dir paths to point to the directory that holds the pdf files and the directory that the
        generated images should be placed under.
'''

import pdf2image, os

pdf_dir = 'pdfs/' # Include trailing forward slash
img_dir = 'images/'
first_page_only = True # Only convert the first page of the pdf to an image

pdf_names = [pdf_name.split('.')[0] for pdf_name in os.listdir(pdf_dir) if pdf_name[-4:] == ".pdf"]

for pdf_name in pdf_names:
    pages = pdf2image.convert_from_path('{}{}.pdf'.format(pdf_dir, pdf_name))

    if first_page_only:
        pages[0].save('{}/{}.jpg'.format(img_dir, pdf_name), 'JPEG')

    else:
        directory = '{}{}'.format(img_dir, pdf_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        for i, page in enumerate(pages):
            page.save('{}{}/{}-{}.jpg'.format(img_dir, pdf_name, pdf_name, i), 'JPEG')