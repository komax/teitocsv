import unittest

from bacteria_regex import AccessionNumberMatcher


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

    def test_biosamples_pattern_matches_once(self):
        text = """
        This is a text with accession number SAMEF1234567890123456 637783848.
        """
        matches = list(self.matcher.accession_numbers(text))
        self.assertEqual(matches, ['SAMEF1234567890123456'])

    def test_sample_pattern_matches_twice(self):
        text = """
        This is a text with accession numbers ERS123456 and ERS654321.
        """
        matches = list(self.matcher.accession_numbers(text))
        self.assertEqual(matches, ['ERS123456', 'ERS654321'])

    def test_experiments_pattern_matches_four_times(self):
        text = """
        This is a text with accession numbers ERX123456, DRX123456, SRX123456 and
        SRX654321.
        """
        matches = list(self.matcher.accession_numbers(text))
        self.assertEqual(matches, ['ERX123456', 'DRX123456', 'SRX123456', 'SRX654321'])

    def test_analysis_pattern_matches_three_times(self):
        text = """
        This paragraph has accession number ERZ111333.

        Another analysis has accession number DRZ666333.

        Accession number SRZ333222 is contained in  [Foobar, 2000].
        """
        accession_numbers = list(self.matcher.accession_numbers(text))
        self.assertEqual(accession_numbers, ['ERZ111333', 'DRZ666333', 'SRZ333222'])

    def test_chinese_accession_number_matches(self):
        text = """
        This paragraph has accession number PRJCA001121.

        """
        accession_numbers = list(self.matcher.accession_numbers(text))
        self.assertEqual(accession_numbers, ['PRJCA001121'])



if __name__ == '__main__':
    unittest.main()