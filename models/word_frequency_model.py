import logging
import re
import string
from concurrent.futures import ProcessPoolExecutor
from types import GeneratorType
import pandas as pd
from nltk import FreqDist
from nltk import ngrams
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from models.token_stats_model import TokensStats
from word_frequency.stopwords import stop_words

FORMAT = "[%(levelname)s] %(name)s:%(lineno)d : %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Stemmer:

    def __init__(self, language="english"):
        self.language = language
        self.stemmer = SnowballStemmer(language, ignore_stopwords=True)

    def stem(self, word_list):
        if len(word_list) < 100000000000:
            return (self.stemmer.stem(word) for word in word_list)
        with ProcessPoolExecutor(max_workers=4) as executor:
            result = executor.map(self.stemmer.stem, word_list)
        return list(result)

    def stem_word(self, word):
        return self.stemmer.stem(word)


class WordModel:

    def __init__(self, stem: bool = False, punct: bool = False, ngrams: int = 0):
        self.ngrams = ngrams
        self.punct = punct
        self.stem = stem

    @property
    def ngrams(self):
        return self._ngrams

    @ngrams.setter
    def ngrams(self, value):
        if isinstance(value, int):
            self._ngrams = int(value) if value and value < 4 else 0
        else:
            self._ngrams = 0

    @staticmethod
    def rm_punct_text(text):
        text = re.sub("[^\w\d]+", " ", text)
        return text

    @staticmethod
    def rm_stopwords(tokens: list, stopwords: set):
        tokens = (token for token in tokens if token not in stopwords)
        return tokens

    @staticmethod
    def rm_punct(tokens):
        tokens = (token for token in tokens if token not in string.punctuation)
        return tokens

    @staticmethod
    def df_to_json(df: pd.DataFrame):
        return df.to_json(orient="records")


class WordFrequencyModel(WordModel):

    def __init__(self, text: str, stopwords: list, remove_stopwords: bool, stem: bool = False, punct: bool = False,
                 ngrams=0):
        super().__init__(ngrams=ngrams, punct=punct, stem=stem)
        self.remove_stopwords = remove_stopwords
        self.stopwords = stopwords + stop_words if stopwords else stop_words
        self.stemmer = stem if not stem else Stemmer()
        self.text = text.lower()
        if punct:  # Make this @property?
            self.text = self.rm_punct_text(self.text)
        self.ngrams = ngrams
        self.tokens = self._tokenizer()
        self._apply_filters()
        self.stats = TokensStats(self.tokens)

    def _apply_filters(self):
        """Apply filters from front-end to the tokens"""
        if self.remove_stopwords and self.stem:
            self.tokens = self._rm_stem_stopwords(self.tokens, self.stopwords)
        elif not self.remove_stopwords and self.stem:
            self.tokens = self.stemmer.stem(self.tokens)
        elif self.remove_stopwords and not self.stem:
            self.tokens = self.rm_stopwords(self.tokens, self.stopwords)
        if self.ngrams and self.ngrams > 1:
            self.tokens = list(self._generate_ngrams(self.ngrams))
        if isinstance(self.tokens, GeneratorType):
            self.tokens = list(self.tokens)

    def frequencies(self, length) -> pd.DataFrame:
        dict_freq = FreqDist(self.tokens).most_common(length)
        if dict_freq and isinstance(dict_freq[0][0], tuple) and len(dict_freq[0][0]) > 1:
            keys = [" ".join(i[0]) for i in dict_freq]
            vals = [i[1] for i in dict_freq]
            dict_freq = zip(keys, vals)
        df_frequencies = pd.DataFrame(dict_freq, columns=["Token", "Frequency"])
        logger.info(f"Calculated top {length} Frequencies")
        #  df_frequencies.sort_values("Frequency", inplace=True)
        return df_frequencies.head(length)

    def _tokenizer(self) -> list:
        tokens = [token for token in word_tokenize(self.text)]
        return tokens

    def _rm_stem_stopwords(self, tokens: list, stopwords: set):
        if not self.stemmer:
            tokens = [token for token in tokens if token not in stopwords]
            return tokens
        tokens = (self.stemmer.stem_word(token) for token in tokens if token not in stopwords)
        return tokens

    def _generate_ngrams(self, n: int):
        if 4 > n > 1:
            result = ngrams(self.tokens, n)
            return result

    def tokens_stats(self):
        if isinstance(self.stats, GeneratorType):
            self.tokens = TokensStats(list(self.tokens))
        return self.stats.set_tokens, self.stats.avg_len(), self.stats.max()
