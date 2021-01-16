from sklearn.cluster import KMeans


def cluster(X, X_prime=()):
    km = KMeans(
        n_clusters=3, init='random',
        n_init=10, max_iter=300, 
        tol=1e-04, random_state=0
    )

    km.fit(X)

    new = None

    if X_prime:
        new = km.fit_predict(X_prime)

    return km.labels_, new