import unittest

from teireader import AccessionNumberMatcher


class TestAccessionNumberMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = AccessionNumberMatcher()

    def test_studies_pattern_matches_once(self):
        text = """
        This is a text with accession number ERP123456. 
        This will give us this.
        """

        matches = list(self.matcher.accession_numbers(text))
        self.assertEqual(['ERP123456'], matches)

    def test_studies_pattern_matches_twice(self):
        text = """
        This is a text with accession number ERP123456. 
        This will give us this. DRP654321.
        """
        matches = list(self.matcher.accession_numbers(text))
        self.assertEqual(['ERP123456', 'DRP654321'], matches)

    def test_studies_pattern_does_not_match(self):
        text = """
        This is a text with accession number foobar. 
        This will give us this.
        """
        matches = list(self.matcher.accession_numbers(text))
        self.assertFalse(matches)


if __name__ == '__main__':
    unittest.main()