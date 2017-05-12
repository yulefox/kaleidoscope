#!/bin/env python
# -*- encoding=utf8 -*-

'''
hello
'''

#from __future__ import print_function
from PIL import Image
import numpy
from scipy.misc import imsave

def binarize(input_path, output_path, threshold):
    '''
    binarize
    '''
    image = Image.open(input_path).convert("L")
    image.load()
    _h, _w = image.size
    array = numpy.array(image)
    print(image.size, image.mode, (len(array), len(array[0])))
    for i in range(_w):
        for j in range(_h):
            if array[i][j] > threshold:
                array[i][j] = 255
            else:
                array[i][j] = 0
    imsave(output_path, array)

def get_parser():
    '''
    Get parser object
    '''
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="read input file",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-o", "--output",
                        dest="output",
                        help="write output file",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-t", "--threshold",
                        dest="threshold",
                        help="threshold when to show white/black",
                        default=200,
                        type=int)
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    binarize(args.input, args.output, args.threshold)
    Image.open(args.input).show()
    Image.open(args.output).show()
