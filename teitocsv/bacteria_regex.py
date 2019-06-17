
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
