models = [{"label": "KMeans", "value": "KMeans"},
          {"label": "AgglomerativeClustering", "value": "AgglomerativeClustering"},
          {"label": "DBSCAN", "value": "DBSCAN"}]

params = {"KMeans": {"n_clusters": 5, "n_init": 1, "max_iter": 550},
          "AgglomerativeClustering": {"n_clusters": 5},
          "DBSCAN": {"eps": 0.18, "min_samples": 3}}

all_params = {"n_init": 1, "max_iter": 550,
              "n_clusters": 5, "eps": 0.18, "min_samples": 3}

limits = {"n_init": 50, "max_iter": 550,
          "n_clusters": 50, "eps": 0.9, "min_samples": 55}

columns = [{"label": "F1", "value": "F1"},
           {"label": "F2", "value": "F2"},
           {"label": "F3", "value": "F3"},
           {"label": "F4", "value": "F4"}]
