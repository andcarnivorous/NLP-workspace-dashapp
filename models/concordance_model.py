from models.utils import sanitize_regex
import re


class ConcordanceList:

    def __init__(self, text: str, pattern: str, limit: int=2):
        self.text = text.lower()
        self.limit = limit
        self.pattern = re.compile("\\b"+sanitize_regex(pattern)+"\\b")
        self.records = self.text.split()
        self.matches = (idx for idx, item in enumerate(self.records) if re.search(self.pattern, item))
        self.rows = self.__rows()
        self.idx = 0

    def __rows(self):
        for idx in self.matches:
            yield [" ".join(self.records[idx-self.limit:idx]),
                   self.records[idx],
                   " ".join(self.records[idx+1:idx+1+self.limit])]

    def get_row(self):
        try:
            return next(self.rows)
        except StopIteration:
            return
