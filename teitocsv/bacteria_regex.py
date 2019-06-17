
import re


class AccessionNumberMatcher(object):
    def __init__(self):

        """
        ·         PRJ
        """
        projects_pattern = r'PRJ(E|D|N|C)[A-Z][0-9]+'

        """
    ·         ERP
    ·         DRP
    ·         SRP
        """
        studies_pattern = r'(E|D|S)RP\d{6,}'
        """
            ·         SAME
    ·         SAMD
    ·         SAMN
        """
        biosamples_pattern = r'SAM(E|D|N)[A-Z]?\d+'
        """
    ·         ERS

        """
        samples_pattern = r'(E|D|S)RS\d{6,}'
        """
    ·         ERX
    ·         DRX
    ·         SRX
        """
        experiments_pattern = r'(E|D|S)RX\d{6,}'

        """
        ·         DRR
·         SRR
        """
        runs_pattern = r'(E|D|S)RR[0-9]{6,}'
    
        """
        ·         ERZ
    ·         DRZ
    ·         SRZ
        """
        analysis_pattern = r'(E|D|S)RZ\d{6,}'

        combined_pattern = f'({"|".join([projects_pattern, studies_pattern, biosamples_pattern, samples_pattern, runs_pattern, experiments_pattern, analysis_pattern])})'

        self.pattern = combined_pattern
        self.regex = re.compile(combined_pattern)

    def accession_numbers(self, text):
        matches = self.regex.findall(text)
        for match in matches:
            accession_number = match[0]
            yield accession_number


class DataSourceMatcher(object):
    def __init__(self):
        sources = ['Figshare', 'QIITA', 'MG-RAST', 'bioproject']

        combined_pattern = f'({"|".join(sources)})'
        self.pattern = combined_pattern
        self.regex = re.compile(combined_pattern, re.I)

    def data_source(self, text, default_val=''):
        match = self.regex.search(text)
        if match:
            data_source = match.group(0)
            return data_source.lower()
        else:
            return default_val


class BacteriaMatcher(object):
    sequencing_method = re.compile(r'([Ii]llumina|[Ss]olexa|454|[Ii]ontorrent)')
    miseq_pattern = re.compile(r'([Mm]i[Ss]eq).+?([Ii]llumina)')
    hiseq_pattern = re.compile(r'([Hh]i[Ss]eq).+?([Ii]llumina)')
    primer_515 = re.compile(r'(515\s*[fF]?|(Fwd\s*)?5 -GTGBCAGCMGCCGCGGTAA-3)')
    primer_806 = re.compile(r'(806\s*[rR]?|(Rev\s*)?5’-GGACTACHVGGGTWTCTAAT-3′)')
    gene_region_16ness = re.compile(r'(16[sS]\s*rRNA)')
    gene_regions_regex = re.compile(r'([vV]\d)\s*(?:\s*-?\s*([vV]\d)\s*)?regions?|regions?\s*([vV]\d)(?:\s*-?\s*([vV]\d))?')

    accession_no_matcher = AccessionNumberMatcher()

    @staticmethod
    def accession_numbers(text):
        return BacteriaMatcher.accession_no_matcher.accession_numbers(text)

    @staticmethod
    def matches_16ness(text):
        return BacteriaMatcher.gene_region_16ness.findall(text)
