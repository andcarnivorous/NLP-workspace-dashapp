from typing import List


class TokensStats:
    """
    tokens
    """

    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.set_tokens = set(tokens)
        self.tokens_set_len = len(self.set_tokens)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.tokens[idx]
        elif isinstance(idx, int):
            return self.tokens[idx]

    def avg_len(self):
        if isinstance(self.tokens[0], tuple):
            ngram_tokens = [" ".join(ngram) for ngram in self.tokens]
            return sum(map(len, ngram_tokens)) / len(ngram_tokens)
        return sum(map(len, self.tokens)) / len(self.tokens)

    def max(self):
        if isinstance(self.tokens[0], tuple):
            ngram_tokens = [" ".join(ngram) for ngram in self.tokens]
            return max(ngram_tokens, key=len)
        return max(self.tokens, key=len)
