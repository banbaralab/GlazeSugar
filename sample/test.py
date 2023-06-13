#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""

import sys
import getopt
import re


class Config:
    def __init__(self, verbose=False):
        self.verbose = verbose


config = Config()


def usage(msg=""):
    if msg != "":
        print(f"{msg}\n")
    print(f"Usage: python3 {sys.argv[0]} <options> file")
    print(f"    -h --help               : show this help")
    print(f"    -v --verbose            : show detail")
    exit()


def main():
    global config
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "verbose"])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
            elif opt in ("-v", "--verbose"):
                config.verbose = True

        if len(args) != 1:
            usage("please input file.")

    except getopt.GetoptError as err:
        usage(str(err))


if __name__ == "__main__":
    main()
