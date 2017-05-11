#!/bin/env python
# -*- encoding=utf8 -*-

import os,sys
from PIL import Image

if __name__ == "__main__":
    im = Image.open("./img.jpg")
    im.convert("1")
    im.save("1.jpg", "JPEG")
