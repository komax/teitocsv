import unittest

from bacteria_regex import AccessionNumberMatcher, DataSourceMatcher


class TestAccessionNumberMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = AccessionNumberMatcher()

    def test_studies_pattern_matches_once(self):
        text = """
        This is a text with accession number ERP123456. 
        This will give us this.
        """

        matches = self.matcher.accession_numbers(text)
        self.assertEqual(['ERP123456'], matches)

    def test_studies_pattern_matches_twice(self):
        text = """
        This is a text with accession number ERP123456. 
        This will give us this. DRP654321.
        """
        matches = self.matcher.accession_numbers(text)
        self.assertEqual(['ERP123456', 'DRP654321'], matches)

    def test_studies_pattern_does_not_match(self):
        text = """
        This is a text with accession number foobar. 
        This will give us this.
        """
        matches = self.matcher.accession_numbers(text)
        self.assertFalse(matches)

    def test_biosamples_pattern_matches_once(self):
        text = """
        This is a text with accession number SAMEF1234567890123456 637783848.
        """
        matches = self.matcher.accession_numbers(text)
        self.assertEqual(matches, ['SAMEF1234567890123456'])

    def test_sample_pattern_matches_twice(self):
        text = """
        This is a text with accession numbers ERS123456 and ERS654321.
        """
        matches = self.matcher.accession_numbers(text)
        self.assertEqual(matches, ['ERS123456', 'ERS654321'])

    def test_experiments_pattern_matches_four_times(self):
        text = """
        This is a text with accession numbers ERX123456, DRX123456, SRX123456 and
        SRX654321.
        """
        matches = self.matcher.accession_numbers(text)
        self.assertEqual(matches, ['ERX123456', 'DRX123456', 'SRX123456', 'SRX654321'])

    def test_analysis_pattern_matches_three_times(self):
        text = """
        This paragraph has accession number ERZ111333.

        Another analysis has accession number DRZ666333.

        Accession number SRZ333222 is contained in  [Foobar, 2000].
        """
        accession_numbers = self.matcher.accession_numbers(text)
        self.assertEqual(accession_numbers, ['ERZ111333', 'DRZ666333', 'SRZ333222'])

    def test_chinese_accession_number_matches(self):
        text = """
        This paragraph has accession number PRJCA001121.

        """
        accession_numbers = self.matcher.accession_numbers(text)
        self.assertEqual(accession_numbers, ['PRJCA001121'])


class DataSourceMatcherTest(unittest.TestCase):

    def setUp(self):
        self.matcher = DataSourceMatcher()

    def test_find_figshare(self):
        text = """
        All sequence data will be made available through FigShare, http://dx.doi.org/10.22222/m9.figshare.1234567890.
        """
        data_source = self.matcher.data_source(text)
        self.assertEqual(data_source, "figshare")

    def test_figshare_with_weird_spelling(self):
        text = """
        All sequence data will be made available through FIGShare, http://dx.doi.org/10.22222/m9.figshare.1234567890.
        """
        data_source = self.matcher.data_source(text)
        self.assertEqual(data_source, "figshare")

    def test_figshare_only_in_url(self):
        text = """
        All sequence data will be made available via http://dx.doi.org/10.22222/m9.figshare.1234567890.
        """
        data_source = self.matcher.data_source(text)
        self.assertEqual(data_source, "figshare")

    def test_qiita_in_text(self):
        text = "All data available through QIITA."
        data_source = self.matcher.data_source(text)
        self.assertEqual(data_source, "qiita")

    def test_mg_rast_in_text(self):
        text = "All data available through 'MG-RAST'"
        data_source = self.matcher.data_source(text)
        self.assertEqual(data_source, "mg-rast")

    def test_bioproject_as_url(self):
        text = "All data available via https://www.ncbi.nlm.nih.gov/bioproject."
        self.assertEqual(self.matcher.data_source(text), 'bioproject')

    def test_no_data_source(self):
        text = """
        Foo bar is great, but this is bogus.
        """
        data_source = self.matcher.data_source(text)
        self.assertEqual(data_source, '')


if __name__ == '__main__':
    unittest.main()