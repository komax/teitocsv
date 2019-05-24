#!/usr/bin/env python
import argparse
from pathlib import Path
from multiprocessing.pool import Pool

import pandas as pd

from teireader import TEIFile

def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="input directory containing TEI XML files")
    parser.add_argument('outfile',
                        help="output file as CSV with information about the TEI articles")
    return parser


def all_teis(input_dir):
    return sorted(Path(input_dir).glob('*.tei.xml'))


def main():
    parser = set_up_argparser()
    args = parser.parse_args()
    
    result_csv = pd.DataFrame(columns=['ID', 'DOI','Title', 'Journal'])

    for tei_file in all_teis(args.inputdir):
        tei = TEIFile(tei_file)
        result_csv = result_csv.append({
            'ID':tei.basename(),
            'DOI':tei.doi(),
            'Title':tei.title(),
            'Journal':tei.published_in()}, ignore_index=True)

    print(result_csv)

    args.outfile

    #pool = Pool()

    #pool.map(func, teis)
    pass

if __name__ == '__main__':
    main()
