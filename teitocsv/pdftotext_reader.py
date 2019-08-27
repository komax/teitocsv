import re
import itertools

from bacteria_regex import BacteriaMatcher

def read_text_file(filename, delimiter=' ', strip='\n'):
    with open(filename, 'rb') as txt:
        res = []
        for line_bytes in txt:
            line = line_bytes.decode('utf-8', 'ignore')
            res.append(line.rstrip(strip))
        return delimiter.join(res)


def digital_object_identifier(text):
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    regex = re.compile(pattern)

    for match in regex.finditer(text):
        # Return first found doi in the text.
        doi = match[1]
        return doi
    # Otherwise return an empty string.
    return ''


class PDFToText(object):
    def __init__(self, filename):
        self.filename = filename
        self.text = read_text_file(filename)

    def accession_numbers(self):
        return BacteriaMatcher.accession_numbers(self.text)

    def text_until(self, word_count=1000, delimiter=' '):
        if not word_count:
            raise RuntimeError("Word count needs to be a positive number")
        words = self.text.split(delimiter)
        sliced_words = itertools.islice(words, word_count)
        return delimiter.join(sliced_words)

    def doi(self):
        text = self.text_until(1000)
        return digital_object_identifier(text)


