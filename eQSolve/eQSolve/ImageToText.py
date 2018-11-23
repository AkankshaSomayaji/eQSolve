from PIL import Image
import pytesseract
import argparse
import os

class GetImageData(object):
        def m(self):
            image = Image.open("cover.jpg")
            text = pytesseract.image_to_string(image)
            return text
