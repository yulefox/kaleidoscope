#!/bin/env python
# -*- encoding=utf8 -*-

import sys
import getopt

version = "1.0.0"

class Usage(Exception):
    '''
    Usage
    '''
    def __init__(self, msg):
        self.msg = msg
        print "生成文档目录结构。"
        print ""
        print "用法:"
        print "    -a,--all:        全部"
        print "    -h,--help:       输出帮助用法"
        print "    -v,--version:    打印当前版本"
        print ""

def main(argv=None):
    '''
    main
    '''
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:],
                                       "a:d:hv",
                                       ["all=", "directory=", "help", "version"])
            for k, val in opts:
                if k in ("-a", "--all"):
                    print val, args
                    return 0
                elif k in ("-h", "--help"):
                    Usage(k)
                    return 0
                elif k in ("-d", "--directory"):
                    print val
                elif k in ("-v", "--version"):
                    print version
                    return 0
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        return 2

if __name__ == "__main__":
    sys.exit(main())
