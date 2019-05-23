from dataclasses import dataclass

from bs4 import BeautifulSoup 


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

    def doi(self):
        idno_elem = self.soup.find('idno', type='DOI')
        return idno_elem.getText()

    def title(self):
        return self.soup.title.getText()

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



def main():
    #tei = TEIFile("/Users/mk21womu/data/steph_bacteria_text_mining/grobid-output/Winstel_Kuhner_et_al._2015_-_Wall_Teichoic_Acid_Glycosylation_Governs.tei.xml")
    tei = TEIFile("/Users/mk21womu/data/steph_bacteria_text_mining/grobid-output/Aliyu_Maayer_et_al._2016_-_The_genome_of_the_Antarctic.tei.xml")
    print(tei.doi())
    print(tei.title())
    print(tei.authors())
    print(tei.published_in())


if __name__ == "__main__":
    main()
