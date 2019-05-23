#!/usr/bin/env python
import argparse

from multiprocessing.pool import Pool


def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="input directory containing TEI XML files")
    parser.add_argument('outfile',
                        help="output file as CSV with information about the TEI articles")
    return parser


def main():
    parser = set_up_argparser()
    args = parser.parse_args()

    #pool = Pool()

    #pool.map(func, teis)
    pass

if __name__ == '__main__':
    main()
