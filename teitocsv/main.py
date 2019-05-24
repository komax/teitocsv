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


def tei_to_csv_entry(tei_file):
    tei = TEIFile(tei_file)
    print(f"Handled {tei_file}")
    return tei.basename(), tei.doi(), tei.title(), tei.published_in()


def main():
    parser = set_up_argparser()
    args = parser.parse_args()
    
    result_csv = pd.DataFrame(columns=['ID', 'DOI','Title', 'Journal'])

    teis = all_teis(args.inputdir)

    pool = Pool()
    csv_entries = pool.map(tei_to_csv_entry, teis)
    print(csv_entries)
    
    print("Done with parsing")
    result_csv = pd.DataFrame(csv_entries, columns=['ID', 'DOI','Title', 'Journal'])
    print("Done with appending")

    result_csv.to_csv(args.outfile, index=False)
    print("Done with csv")

if __name__ == '__main__':
    main()
