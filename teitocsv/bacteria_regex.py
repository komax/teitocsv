
import re

class UnionPatternMatcher(object):
    def __init__(self, patterns):
        combined_pattern = f'({"|".join(patterns)})'
        self.pattern = combined_pattern
        self.regex = re.compile(combined_pattern, re.I)

    def matches(self, text):
        matches = []
        for match in self.regex.findall(text):
            group = match[0]
            matches.append(group)
        return matches

    def match(self, text, default_val=''):
        match = self.regex.search(text)
        if match:
            group = match.group(0)
            return group.lower()
        else:
            return default_val


class AccessionNumberMatcher(UnionPatternMatcher):
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
        patterns = [projects_pattern, studies_pattern, biosamples_pattern, samples_pattern, runs_pattern, experiments_pattern, analysis_pattern]
        super().__init__(patterns)

    def accession_numbers(self, text):
        return self.matches(text)


class DataSourceMatcher(UnionPatternMatcher):
    def __init__(self):
        sources = ['Figshare', 'QIITA', 'MG-RAST', 'bioproject']
        super().__init__(patterns=sources)

        combined_pattern = f'({"|".join(sources)})'
        self.pattern = combined_pattern
        self.regex = re.compile(combined_pattern, re.I)

    def data_source(self, text, default_val=''):
        return self.match(text, default_val)


class SequencingMethodMatcher(UnionPatternMatcher):
    def __init__(self):
        sequencing_methods = ['Miseq', 'Hiseq', 'Illumina', 'Solexa', '454', 'Iontorrent']

        super().__init__(patterns=sequencing_methods)

    def sequencing_method(self, text, default_val=''):
        self.match(text, default_val)


class Primer515Matcher(UnionPatternMatcher):
    def __init__(self):
        primer_515 = [r'515\s*[fF]?', r'(?:Fwd\s*)?5 -GTGBCAGCMGCCGCGGTAA-3']
        
        super().__init__(patterns=primer_515)
    
    def primer_515(self, text, default_val=''):
        self.match(text, default_val)


class Primer806Matcher(UnionPatternMatcher):
    def __init__(self):
        primer_806 = [r'806\s*[rR]?', r'(?:Rev\s*)?5’-GGACTACHVGGGTWTCTAAT-3′']

        super().__init__(patterns=primer_806)

    def primer_806(self, text, default_val=''):
        self.match(text, default_val)


class GeneRegionsMatcher(UnionPatternMatcher):
    def __init__(self):
        gene_regions_patterns = [
            r'([vV]\d)\s*(?:\s*-?\s*([vV]\d)\s*)?regions?',
            r'regions?\s*([vV]\d)(?:\s*-?\s*([vV]\d))?'
        ]

        super().__init__(patterns=gene_regions_patterns)

    def gene_regions(self, text, default_val=''):
        matches = self.regex.findall(text)
        regions = set()
        for match in matches:
            regions.union(set(match))
        return regions


class BacteriaMatcher(object):
    
    sequencing_matcher = SequencingMethodMatcher()
    primer_515 = Primer515Matcher()
    primer_806 = Primer806Matcher()
    
    gene_region_16ness = re.compile(r'(16[sS]\s*rRNA)')
    gene_regions_matcher = GeneRegionsMatcher()

    accession_no_matcher = AccessionNumberMatcher()
    data_source_matcher = DataSourceMatcher()

    @staticmethod
    def accession_numbers(text):
        return BacteriaMatcher.accession_no_matcher.accession_numbers(text)

    @staticmethod
    def matches_16ness(text):
        return BacteriaMatcher.gene_region_16ness.findall(text)

