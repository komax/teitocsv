import unittest

import bacteria_regex

from pdftotext_reader import digital_object_identifier


class TestAccessionNumberMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = bacteria_regex.AccessionNumberMatcher()

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
        expected = ['ERP123456', 'DRP654321']
        self.assertCountEqual(expected, matches)

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
        expected = ['ERS123456', 'ERS654321']
        self.assertCountEqual(matches, expected)

    def test_experiments_pattern_matches_four_times(self):
        text = """
        This is a text with accession numbers ERX123456, DRX123456, SRX123456 and
        SRX654321.
        """
        matches = self.matcher.accession_numbers(text)
        expected = ['ERX123456', 'DRX123456', 'SRX123456', 'SRX654321']
        self.assertCountEqual(matches, expected)

    def test_analysis_pattern_matches_three_times(self):
        text = """
        This paragraph has accession number ERZ111333.

        Another analysis has accession number DRZ666333.

        Accession number SRZ333222 is contained in  [Foobar, 2000].
        """
        accession_numbers = self.matcher.accession_numbers(text)
        expected = ['ERZ111333', 'DRZ666333', 'SRZ333222']
        self.assertCountEqual(accession_numbers, expected)

    def test_chinese_accession_number_matches(self):
        text = """
        This paragraph has accession number PRJCA001121.

        """
        accession_numbers = self.matcher.accession_numbers(text)
        self.assertEqual(accession_numbers, ['PRJCA001121'])

    def test_accession_no_occurence_twice_in_text(self):
        text = """
        This is a text with accession number ERP123456. 
        This will give us this. ERP123456.
        """
        matches = self.matcher.accession_numbers(text)
        self.assertEqual(['ERP123456'], matches)


class DataSourceMatcherTest(unittest.TestCase):

    def setUp(self):
        self.matcher = bacteria_regex.DataSourceMatcher()

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


class SequencingMethodTestCase(unittest.TestCase):
    
    def setUp(self):
        self.matcher = bacteria_regex.SequencingMethodMatcher()
    
    def test_illumina_with_miseq(self):
        text = """
        The resulting foobar were purified by great amount of drudging using GEO Standard Kit. 
        and sequenced using the 300PE protocol on MiSeq System (Illumina, United States).
        """
        seq_method = self.matcher.sequencing_method(text)
        self.assertEqual(seq_method, 'miseq')

    def test_illumina_with_hiseq(self):
        text = """
        The resulting foobar were purified by great amount of drudging using GEO Standard Kit. 
        and sequenced using the 300PE protocol on HIseq System (Illumina, United States).
        """
        seq_method = self.matcher.sequencing_method(text)
        self.assertEqual(seq_method, 'hiseq')

    def test_give_priority_to_illumina_over_solexa(self):
        text = "SolexaQA: at-a-glance quality assessment of Illumina second-generation sequencing data"
        seq_method = self.matcher.sequencing_method(text)
        self.assertEqual(seq_method, 'illumina')

    def test_iontorrent_in_url(self):
        text = "were aligned against the reference genome using Tmap (http://github.com/iontorrent/TMAP)"
        seq_method = self.matcher.sequencing_method(text)
        self.assertEqual(seq_method, 'iontorrent')

    def test_find_solexa_in_text(self):
        text = "The resulting foobar were sequenced with help of SOLEXA."
        seq_method = self.matcher.sequencing_method(text)
        self.assertEqual(seq_method, 'solexa')


class GeneRegionsTest(unittest.TestCase):

    def setUp(self):
        self.matcher = bacteria_regex.GeneRegionsMatcher()

    def test_singleton_occurence(self):
        text = "The V4 region of 16S rRNA genes was amplified from the DNA samples using the 515f/806r primer set."
        regions = self.matcher.gene_regions(text)
        expected = set(["v4"])
        self.assertCountEqual(regions, expected)

    def test_singleton_occurence_v_before_region(self):
        text = "v2                       region"
        regions = self.matcher.gene_regions(text)
        self.assertCountEqual(regions, set(['v2']))

    def test_two_regions_with_and_between(self):
        text = "regions            V1     and        v2"
        regions = self.matcher.gene_regions(text)
        self.assertCountEqual(regions, set(['v1', 'v2']))

    def test_two_regions_separated_by_minus(self):
        text = "regions v2    -        V4"
        regions = self.matcher.gene_regions(text)
        self.assertCountEqual(regions, set(['v2', 'v4']))

    def test_two_regions_separated_by_minus_then_region(self):
        text = "v2    -        V4 regions"
        regions = self.matcher.gene_regions(text)
        self.assertCountEqual(regions, set(['v2', 'v4']))

    def test_enumerated_regions(self):
        text = "v1, V2,        v3, and v6 regions"
        regions = self.matcher.gene_regions(text)
        self.assertCountEqual(regions, set(['v1', 'v2', 'v3', 'v6']))

    def test_region_first_enumeration_then(self):
        text = "regions v1, V2,        v3 and v6"
        regions = self.matcher.gene_regions(text)
        self.assertCountEqual(regions, set(['v1', 'v2', 'v3', 'v6']))

    def test_no_regions(self):
        text = "This is a text without any gene regions"
        self.assertFalse(self.matcher.gene_regions(text))


class Primer515Test(unittest.TestCase):

    def setUp(self):
        self.matcher = bacteria_regex.Primer515Matcher()

    def check_primer_in(self, text):
        primer = self.matcher.primer_515(text)
        self.assertEqual(primer, "515f")

    def test_515f_cooccur_with806(self):
        text = "The V4 region of 16S rRNA genes was amplified from the DNA samples using the 515f/806r primer set."
        self.check_primer_in(text)

    def test_f515_matches(self):
        text = "primers                 F           515 and          R 806"
        self.check_primer_in(text)

    def test_fwd_515_matches(self):
        text = "primers                 Fwd           515 and          Rev 806"
        self.check_primer_in(text)

    def test_primer_as_string(self):
        text = "we are using super-Ursome primers 5'-GTGCCAGCMGCCGCGGTAA"
        self.check_primer_in(text)

    def test_barcode_matches(self):
        text = """
        we used primer 
        AATGATACGGCGACCACCGAGATCTACACGCT        
         XXXXXXXXXXXX   TATGGTAATT  
           GT  GTGYCAGCMGCCGCGGTAA 
        because we have too much space in this paper.
        """
        self.check_primer_in(text)

    def test_515f_original_pattern(self):
        text = """
        This is some text. We used primer 
        GTGCCAGCMGCCGCGGTAA
        because this primer rulez the world.
        """
        self.check_primer_in(text)

    def test_modified_primer_sequence(self):
        text = """
        We used a primer priming this phrase which leads us to the sequence
        FWD:GTGYCAGCMGCCGCGGTAA
        """
        self.check_primer_in(text)

    def test_515_primer_with_b_in_seq(self):
        text = "foo is a primer FWD5-GTGBCAGCMGCCGCGGTAA-3'"
        self.check_primer_in(text)

    def test_no_primer(self):
        text = "Bogus, spam, ham and nothing but text."
        self.assertFalse(self.matcher.primer_515(text))
    


class Primer806Test(unittest.TestCase):

    def setUp(self):
        self.matcher = bacteria_regex.Primer806Matcher()

    def check_primer_in(self, text):
        primer = self.matcher.primer_806(text)
        self.assertEqual(primer, "806r")

    def test_806_cooccur_with515(self):
        text = "The V4 region of 16S rRNA genes was amplified from the DNA samples using the 515f/806r primer set."
        self.check_primer_in(text)

    def test_r806_matches(self):
        text = "primers                 F           515 and          R 806"
        self.check_primer_in(text)

    def test_806_rev_matches(self):
        text = "primers                 Fwd           515 and          806 REV"
        self.check_primer_in(text)

    def test_barcode_pattern_matches(self):
        text = """
        primer 
        
        CAAGCAGAAGACGGCATACGAGAT 
        
        
        
        AGTCAGCCAG 
        
        
        CC 
        
        
        GGACTACNVGGGTWTCTAAT
        
        weird text though.
        """
        self.check_primer_in(text)

    def test_apprill_pattern_matches(self):
        text = """
        Apprill primer REV:GGACTACNVGGGTWTCTAAT with nice results as follows.
        """
        self.check_primer_in(text)

    def test_for_caporaso_pattern(self):
        text = """
        Caporaso primer looks like this: REV:GGACTACHVGGGTWTCTAAT.
        """
        self.check_primer_in(text)

    def test_16s_rna_v4_primer_matches(self):
        text = "We sequenced 16S rRNA in region V4 with primer 5'-GGACTACHVHHHTWTCTAAT"
        self.check_primer_in(text)

    def test_no_primer(self):
        text = "Bogus, spam, ham and nothing but text."
        self.assertFalse(self.matcher.primer_806(text))
    

class DOIfromTextTest(unittest.TestCase):

    def test_doi_with_space(self):
        text = "Appl Environ Microbiol 83:e01672-17. https://doi.org/10.1128/AEM .12344-12"
        doi = digital_object_identifier(text)
        self.assertEqual("10.1128/AEM .12344-12", doi)

    # Tests from https://www.regexpal.com/96937.
    def test_regexpal_appelquist(self):
        text = "Appelquist, T; Babich, R; Brower, RC; Buchoff, MI; Cheng, M; Clark, MA; Cohen, SD; Fleming, GT; Kiskis, J; Lin, MF; Neil, ET; Osborn, JC; Rebbi, C; Schaich, D; Syritsyn, S; Voronov, G; Vranas, P; Wasem, J~WW scattering parameters via pseudoscalar phase shifts~PHYSICAL REVIEW D~85~2012~ ~http://wok-ws.isiknowledge.com/WoS?recid=206452825#000302994100005~10.1103/PhysRevD.85.07450~0~ ~0~ ~21/11/2015 06:57:32.546000000,"
        doi_expected = "10.1103/PhysRevD.85.07450~0"
        doi_computed = digital_object_identifier(text)
        self.assertEqual(doi_expected, doi_computed)

    def test_regexpal_scattering(self):
        text = "R.C. Brower (Boston U.), G.T. Fleming (Yale U.), H. Neuberger (Rutgers U., Piscataway)~Lattice Radial Quantization: 3D Ising~Phys. Lett. B~721~2013~299~~10.1016/j.physletb.2013.03.009~0~ ~0~ ~21/11/2015 06:57:32.546000000"
        doi_expected = "10.1016/j.physletb.2013.03.009~0"
        doi_computed = digital_object_identifier(text)
        self.assertEqual(doi_expected, doi_computed)


if __name__ == '__main__':
    unittest.main()