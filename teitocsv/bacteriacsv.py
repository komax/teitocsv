#!/usr/bin/env python
import argparse
from pathlib import Path
from multiprocessing.pool import Pool

import pandas as pd

from teireader import BacteriaPaper

def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="input directory containing TEI XML files")
    parser.add_argument('outfile',
                        help="output file as CSV with descriptive attributes on bacteria")
    return parser


def all_teis(input_dir):
    return sorted(Path(input_dir).glob('*.tei.xml'))


def tei_to_csv_entries(tei_file):
    tei = BacteriaPaper(tei_file)
    is_16_ness = tei.contains_16ness()
    entries = []
    for accession_number in tei.accession_numbers():
        entry = tei.basename(), tei.doi(), is_16_ness, accession_number
        entries.append(entry)
    print(f"Handled {tei_file}")
    return entries


def main():
    parser = set_up_argparser()
    args = parser.parse_args()
    
    result_csv = pd.DataFrame(columns=['ID', 'DOI', '16ness', 'accession'])

    teis = all_teis(args.inputdir)

    csv_entries = []

    pool = Pool()
    csv_entries = pool.map(tei_to_csv_entries, teis)

    csv_data = []
    for entry in csv_entries:
        csv_data.extend(entry)
    
    print("Done with parsing")
    result_csv = pd.DataFrame(csv_data, columns=['ID', 'DOI', '16ness', 'accession'])
    print("Done with appending")

    result_csv.to_csv(args.outfile, index=False)
    print("Done with csv")

if __name__ == '__main__':
    main()
