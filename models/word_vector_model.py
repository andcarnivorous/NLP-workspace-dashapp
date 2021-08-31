import pandas as pd
from gensim.models import Word2Vec
from gensim.models import word2vec
import gensim.utils
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import google.cloud.logging
import logging
import os

from models.plotting import Plotter
from utils import GeneratorWrapper
from word_frequency.stopwords import stop_words
from models.word_frequency_model import WordModel, Stemmer

r_state = 12345

stopwords = stop_words

on_cloud = os.getenv("K_SERVICE", None)

handler = None
if on_cloud:
    client = google.cloud.logging.Client()
    handler = client.get_default_handler()
    client.setup_logging()

FORMAT = "[%(levelname)s] %(name)s:%(lineno)d : %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

word2vec.logger.setLevel(logging.CRITICAL)
gensim.utils.logger.setLevel(logging.CRITICAL)

if on_cloud:
    logger.addHandler(handler)


class WordVectorModel(WordModel):

    def __init__(self, text):
        super().__init__()
        self.stemmer = Stemmer()
        self.text = text.lower()
        self.sentences = (self.rm_punct_text(sentence) for sentence in sent_tokenize(self.text))
        self.sentences = (word_tokenize(sentence) for sentence in self.sentences)
        self.sentences = (self._rm_stem_stopwords(sent, stop_words) for sent in self.sentences)
        self.model = self.create_model()
        self.wv = self.model.wv
        self.df = pd.DataFrame(self.wv.index_to_key, index=range(len(self.wv.index_to_key)), columns=["labels"])
        self.pca_vectors = self.pca()
        # self.tsne_vectors = self.tsne()
        self.df["PCA_1"] = self.pca_vectors[:, 0]
        self.df["PCA_2"] = self.pca_vectors[:, 1]
        self.PCA_plotter = Plotter(self.df, col_1="PCA_1", col_2="PCA_2", kind="scatter_with_labels", title="PCA")
        # self.TSNE_plotter = Plotter(self.df, col_1="TSNE_1", col_2="TSNE_2", kind="scatter_with_labels", title="TSNE")

        # self.df["TSNE_1"] = self.tsne_vectors[:, 0]
        # self.df["TSNE_2"] = self.tsne_vectors[:, 1]

        # self.vocab = self.wv.vocab
        # self.wv_vocab = zip(self.vocab, self.wv)

    def sentence_generator(self):
        for sentence in self.sentences:
            yield sentence

    def create_model(self):
        generator = GeneratorWrapper(self.sentence_generator)
        model = Word2Vec(generator, min_count=5, vector_size=350, workers=-1, window=5, sg=0, epochs=15)
        return model

    def pca(self):
        logger.info("Performing PCA")
        pca = PCA(n_components=2, random_state=r_state)
        pcaoutput = pca.fit_transform(self.wv.vectors)
        logger.warning("Returning PCA results")
        return pcaoutput

    def tsne(self):
        logger.warning("Training TSNE...")
        pca = PCA(n_components=10, random_state=r_state)
        pcaoutput = pca.fit_transform(self.wv.vectors)
        logger.warning("Reducing with TSNE...")
        tsneoutput = TSNE(n_components=2, n_jobs=-1, random_state=r_state, perplexity=150).fit_transform(pcaoutput)
        return tsneoutput

    def _rm_stem_stopwords(self, tokens: list, stopwords: set) -> list:
        if not self.stemmer:
            tokens = [token for token in tokens if token not in stopwords]
            return tokens
        tokens = [self.stemmer.stem_word(token) for token in tokens if token not in stopwords]
        return tokens
