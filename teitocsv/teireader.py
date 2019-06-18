import re
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

from pdftotext_reader import PDFToText
from bacteria_regex import AccessionNumberMatcher, BacteriaMatcher



def read_tei(tei_file):
    with open(tei_file, 'r') as tei:
        soup = BeautifulSoup(tei, 'lxml')
        return soup
    raise RuntimeError('Cannot generate a soup from the input')


def elem_to_text(elem, default=''):
    if elem:
        return elem.getText()
    else:
        return default


@dataclass
class Person:
    firstname: str
    middlename: str
    surname: str


class TEIFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.soup = read_tei(filename)
        self._text = None
        self._title = ''
        self._abstract = ''

    def basename(self):
        stem = Path(self.filename).stem
        if stem.endswith('.tei'):
            # Return base name without tei file
            return stem[0:-4]
        else:
            return stem

    def doi(self):
        idno_elem = self.soup.find('idno', type='DOI')
        if not idno_elem:
            return ''
        else:
            return idno_elem.getText()

    @property
    def title(self):
        if not self._title:
            self._title = self.soup.title.getText()
        return self._title

    @property
    def abstract(self):
        if not self._abstract:
            abstract = self.soup.abstract.getText(separator=' ', strip=True)
            self._abstract = abstract
        return self._abstract

    def authors(self):
        authors_in_header = self.soup.analytic.find_all('author')

        result = []
        for author in authors_in_header:
            persname = author.persname
            if not persname:
                continue
            firstname = elem_to_text(persname.find("forename", type="first"))
            middlename = elem_to_text(persname.find("forename", type="middle"))
            surname = elem_to_text(persname.surname)
            person = Person(firstname, middlename, surname)
            result.append(person)
        return result

    def published_in(self):
        title_elem = self.soup.monogr.title
        if not title_elem:
            return ''
        
        if title_elem.get("level") in ['j', 'u', 'm', 's', 'a'] and\
            title_elem.get("type") == "main":
            return title_elem.getText()
        else:
            return ''
    
    @property
    def text(self):
        if not self._text:
            divs_text = []
            for div in self.soup.body.find_all("div"):
                # div is neither an appendix nor references, just plain text.
                if not div.get("type"):
                    div_text = div.get_text(separator=' ', strip=True)
                    divs_text.append(div_text)

            plain_text = " ".join(divs_text)
            self._text = plain_text
        return self._text


class BacteriaPaper(TEIFile):

    def __init__(self, filename, pdftotext_directory):
        super().__init__(filename)
        self.pdftotext_dir = pdftotext_directory

        self._pdftotext = ''

    @property
    def pdftotext(self):
        if not self._pdftotext:
            path_pdftotext = Path(self.pdftotext_dir) / f"{self.basename()}.txt"
            self._pdftotext = PDFToText(path_pdftotext)
        return self._pdftotext

    def accession_numbers(self):
        accession_numbers = BacteriaMatcher.accession_numbers(self.text)
        if accession_numbers:
            # if accession numbers found return them.
            return accession_numbers
        else:
            # Otherwise try to retrieve them from the pdftotext.
            return self.pdftotext.accession_numbers()

    def _has_match_16ness(self, text):
        matches = BacteriaMatcher.matches_16ness(self.text)
        return bool(matches)

    def contains_16ness(self):
        if self._has_match_16ness(self.title):
            return True
        elif self._has_match_16ness(self.abstract):
            return True
        else:
            return self._has_match_16ness(self.text)
        return False

    def _gene_region_matches(self, text):
        return BacteriaMatcher.gene_regions(text)

    def gene_regions(self):
        regions_in_title = self._gene_region_matches(self.title)
        regions_in_text = self._gene_region_matches(self.text)
        regions = regions_in_title.union(regions_in_text)
        # Remove empty str from the gene regions.
        if '' in regions:
            regions.remove('')
        # Sort the results based on the digit: v1 before V6
        return sorted(regions, key=lambda r: r[1])



def main():
    #tei = TEIFile("/Users/mk21womu/data/steph_bacteria_text_mining/grobid-output/Winstel_Kuhner_et_al._2015_-_Wall_Teichoic_Acid_Glycosylation_Governs.tei.xml")
    tei = TEIFile("/Users/mk21womu/data/steph_bacteria_text_mining/grobid-output/Aliyu_Maayer_et_al._2016_-_The_genome_of_the_Antarctic.tei.xml")
    print(tei.basename())
    print(tei.doi())
    print(tei.title)
    print(tei.authors())
    print(tei.published_in())


if __name__ == "__main__":
    main()
