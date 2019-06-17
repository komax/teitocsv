
from bacteria_regex import BacteriaMatcher

def read_text_file(filename, delimiter=' ', strip='\n'):
    with open(filename, 'rb') as txt:
        res = []
        for line_bytes in txt:
            line = line_bytes.decode('utf-8', 'ignore')
            res.append(line.rstrip(strip))
        return delimiter.join(res)


class PDFToText(object):
    def __init__(self, filename):
        self.filename = filename
        self.text = read_text_file(filename)

    def accession_numbers(self):
        return BacteriaMatcher.accession_numbers(self.text)
