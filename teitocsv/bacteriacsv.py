#!/usr/bin/env python
import argparse
from pathlib import Path
from multiprocessing.pool import Pool

import pandas as pd

from teireader import BacteriaPaper

def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="input directory containing TEI XML files")
    parser.add_argument('pdftotexts',
        help="directory containing pdftotext files")
    parser.add_argument('outfile',
                        help="output file as CSV with descriptive attributes on bacteria")
    return parser


def all_teis(input_dir):
    return sorted(Path(input_dir).glob('*.tei.xml'))


def repr_gene_regions(regions, default_length=9):
    length_regions = len(regions)
    if length_regions > default_length:
        raise RuntimeError(
            "Gene region input is longer than the ouput:{} > {}".format(
                length_regions, default_length))
    elif length_regions == default_length:
        return regions
    else:
        # always non-empty.
        leftover_size = default_length - length_regions
        expanded_regions = list(regions)
        remaining_items = [''] * leftover_size
        expanded_regions.extend(remaining_items)
        return expanded_regions


def tei_to_csv_entries(param):
    tei_file, pdftotexts_directory = param
    tei = BacteriaPaper(tei_file, pdftotexts_directory)

    # Check if 16s RNA is mentioned in the paper.
    is_16_ness = tei.contains_16ness()

    # Sequencing method.
    seq_method = tei.sequencing_method()

    # Check for primers.
    has_515_primer = tei.has_515_primer()
    has_806_primer = tei.has_806_primer()

    # Output all gene regions.
    gene_regions = repr_gene_regions(tei.gene_regions())

    entries = []
    # Expand accession numbers from the paper if present.
    for accession_number in tei.accession_numbers():
        entry = tei.basename(), tei.title, tei.doi(), is_16_ness, accession_number, has_515_primer, has_806_primer, seq_method,  *gene_regions
        entries.append(entry)
    # Otherwise empty string.
    if not entries:
        data_source = tei.data_source()
        entry = tei.basename(), tei.title, tei.doi(), is_16_ness, data_source, has_515_primer, has_806_primer, seq_method, *gene_regions
        entries.append(entry)
    print(f"Handled {tei_file}")
    return entries


def main():
    parser = set_up_argparser()
    args = parser.parse_args()

    teis = all_teis(args.inputdir)
    # Store tei and path to directory for pdftotexts.
    mapped_teis = map(lambda tei: (tei, args.pdftotexts), teis)

    csv_entries = []

    pool = Pool()
    csv_entries = pool.map(tei_to_csv_entries, mapped_teis)

    csv_data = []
    for entry in csv_entries:
        csv_data.extend(entry)
    
    print("Done with parsing")
    result_csv = pd.DataFrame(csv_data, columns=['ID', 'Title', 'DOI', '16ness', 'accession', '515f', '806r', 'seq_method', 'gene_region1', 'gene_region2', 'gene_region3', 'gene_region4', 'gene_region5', 'gene_region6', 'gene_region7', 'gene_region8', 'gene_region_9'])
    print("Done with appending")

    result_csv.to_csv(args.outfile, index=False)
    print("Done with csv")

if __name__ == '__main__':
    main()
