import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering, DBSCAN
from time import time


class Modeller:

    models = {"KMeans": KMeans, "AgglomerativeClustering": AgglomerativeClustering, "DBSCAN": DBSCAN}
    params_map = {"KMeans": {"n_clusters": None, "n_init": None, "max_iter": None}, "AgglomerativeClustering": {"n_clusters": None},
              "DBSCAN": {"eps": None, "min_samples": None}}

    def __init__(self, dataframe, model_type, **params):
        self.dataframe = dataframe
        self.model_type = model_type
        self.params = {k: v for k, v in params.items() if k in self.params_map[model_type]}

    def subset_dataframe(self, columns):
        if all(col in self.dataframe.columns for col in columns):
            try:
                X = self.dataframe.loc[:, columns]
            except KeyError:
                raise KeyError(f"Columns {columns} not present")
            return X

        if all(col.lower() in self.dataframe.columns for col in columns):
            try:
                columns = [col.lower() for col in columns]
                X = self.dataframe.loc[:, columns]
            except KeyError:
                raise KeyError(f"Columns {columns} not present")
            return X
        else:
            raise KeyError(f"Columns {columns} are not present in dataframe")

    @staticmethod
    def standardize(X):
        X_standardized = StandardScaler().fit_transform(X)
        return X_standardized

    def set_up_model(self, columns):
        if any(param is None for k, param in self.params.items()):
            return None
        X = self.subset_dataframe(columns)
        X_standardized = self.standardize(X)
        model = self.models[self.model_type]
        t0 = time()
        model = model(**self.params).fit(X_standardized)
        timing = time() - t0
        model.execution_time = timing
        self.dataframe[self.model_type] = model.labels_
        self.dataframe[self.model_type] = self.dataframe[self.model_type].astype("category")
        fig = px.scatter(self.dataframe, x=columns[0], y=columns[1], color=self.model_type)
        return fig
