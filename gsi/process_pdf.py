
# to tiff or png
# use pypdf

from pathlib import Path

import io
import os
#from wand.image import Image #wraps image-magick
#import PythonMagick
import PyPDF2

from pdf2image import convert_from_path
from PIL import Image
import numpy as np

# pdftoppm -png 28ZdbRJKGKtXJ6kAM-grs.ecomm.pdf > a.png

def path2im (src_pdf, fmt):
    images = convert_from_path(src_pdf, fmt = fmt)
    print (images[0])
    # im = images[0].load()
    # print im
    # np_arrs = [np.transpose(np.array(im), (1, 0, 2) ) for im in images]
    np_arrs = [np.array(im) for im in images]
    #print (np_arrs[0].shape)

    return images, np_arrs


def pdf2png (src_pdf_path, out_dir = None, save_fmt = None):
    src_pdf = str(src_pdf_path)

    pdf_im = PyPDF2.PdfFileReader(open(src_pdf, "rb"))
    npage = pdf_im.getNumPages()

    #if npage < 2: return

    print ("--- pdf2png: ", npage, src_pdf)

    images, img_np_arrs = path2im(src_pdf, fmt='ppm')
    print ('num images created = ', len(images))

    if save_fmt:
        fname = src_pdf_path.parts[-1]
        for i, im in enumerate(images):
            tail = fname + '_' + str(i) + '.' + save_fmt
            im.save(str(out_dir / tail), save_fmt)

    return img_np_arrs


if __name__ == '__main__':
    #base = Path('/Users/nishant/UP/ocr-text-tmpl-match/data/1 - user uploaded pdfs/')
    base = Path('/WS/data/1 - user uploaded pdfs/')
    print (base)
    for p in list(base.glob('*.pdf')):
        #pdf2png (p, out_dir = Path('../data/1-pngs'), save_fmt = 'png')
        pdf2png (p, out_dir = Path('../data/1-pngs'), save_fmt = None)



'''

def pdf2png2(src_pdf, resolution = 72,):
    """
    Returns specified PDF as a list of images.
    :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
    :param int resolution: Resolution for resulting png in DPI.
    """
    src_pdf = str(src_pdf)

    print ("---")

    pdf_im = PyPDF2.PdfFileReader(file(src_pdf, "rb"))
    npage = pdf_im.getNumPages()
    print npage

    for pagenum in range(npage):
        page = src_pdf.getPage(pagenum)


        dst_pdf = PyPDF2.PdfFileWriter()
        dst_pdf.addPage(page)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        # pdf_bytes.seek(0)

        images = bytes2im(pdf_bytes.getvalue())

    #img = Image(file = pdf_bytes, resolution = resolution)
    #img.convert("png")

    return images



'''
