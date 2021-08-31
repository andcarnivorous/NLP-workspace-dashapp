import logging

import numpy as np
from scipy.stats import chi2_contingency

from models.word_frequency_model import WordFrequencyModel

FORMAT = "[%(levelname)s] %(name)s:%(lineno)d : %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ChiSquared:

    def __init__(self, texts, test_word_a, stopwords, stem, filter=None):
        self.texts = texts
        self.test_word_a = test_word_a.lower()
        self.word_models = [
            WordFrequencyModel(text=self.texts[key], stopwords=[], remove_stopwords=stopwords, stem=stem, punct=True)
            for key in self.texts.keys()]
        self.tokens = [model.tokens for model in self.word_models]

        self.filter = None

    def return_table(self):
        self.calculate_chi_square()
        return

    def find_and_count(self, tokens):
        tokens = list(tokens)
        return tokens.count(self.test_word_a), len(tokens)
        # return re.findall("", tokens) if self.filter else tokens.count(self.test_word_a)

    def calculate_chi_square(self):
        test_word_count_generator = map(self.find_and_count, self.tokens)

        # tokens_lists = [len(list(token_list)) for token_list in self.tokens if token_list]
        table = np.array(list(test_word_count_generator)).T
        chi2, p, dof, expected = chi2_contingency(table)
        logger.info("Calculated chi2.")
        return chi2, p, dof, expected, table
