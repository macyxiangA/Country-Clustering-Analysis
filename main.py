import csv
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def load_data(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        return [dict(row) for row in rdr]
    
def calc_features(row):
    keys = [
        "child_mort", "exports", "health", "imports", "income",
        "inflation", "life_expec", "total_fer", "gdpp"
    ]
    return np.array([float(row[k]) for k in keys], dtype=np.float64)

def hac(features, linkage_type):
    n = len(features)
    Z = np.zeros((n - 1, 4))
    clusters = {i: [i] for i in range(n)}  

    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = np.linalg.norm(features[i] - features[j])
            D[j, i] = D[i, j]

    next = n 

    for step in range(n - 1):
        min_dist = np.inf
        pair = (None, None)
        keys = sorted(clusters.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                dists = [
                    D[p][q] for p in clusters[a] for q in clusters[b]
                ]
                dist = min(dists) if linkage_type == "single" else max(dists)
                if (dist < min_dist or
                    (dist == min_dist and (a < pair[0] or
                     (a == pair[0] and b < pair[1])))):
                    min_dist = dist
                    pair = (a, b)

        a, b = pair
        size_a = len(clusters[a])
        size_b = len(clusters[b])
        Z[step] = [a, b, min_dist, size_a + size_b]

        clusters[next] = clusters[a] + clusters[b]
        del clusters[a], clusters[b]
        next += 1

    return Z

def fig_hac(Z, names):

    Z = np.asarray(Z, dtype=float)
    fig = plt.figure()
    dendrogram(Z, labels=names, leaf_rotation=90)
    fig.tight_layout()
    return fig

def normalize_features(features):

    X = np.vstack(features)
    mean = np.mean(X, axis=0)             # μ ∈ R^9
    std  = np.std(X,  axis=0, ddof=0)     # σ ∈ R^9
    Xn = (X - mean) / std
    return [Xn[i] for i in range(Xn.shape[0])]
