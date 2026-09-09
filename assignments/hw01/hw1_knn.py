'''
Numerical Programming with NumPy: K-Nearest Neighbors

Build a complete KNN pipeline step by step, exercising core NumPy skills:
broadcasting, argsort, fancy indexing, and reductions.

Examples
--------
See test_knn.py for example inputs and expected outputs.

To verify correctness of your implementation, you can execute:

$ python -m doctest test_knn.py -v
'''

import numpy as np


def euclidean_distances(data_NF, query_QF):
    ''' Compute pairwise Euclidean distances between data and query points.

    Uses NumPy broadcasting to compute all Q*N distances without explicit
    Python loops.

    Args
    ----
    data_NF : 2D np.array, shape (N, F)
        Each row is a feature vector of one data point.
    query_QF : 2D np.array, shape (Q, F)
        Each row is a feature vector of one query point.

    Returns
    -------
    dist_QN : 2D np.array, shape (Q, N)
        dist_QN[q, n] is the Euclidean distance from query q to data point n.
    '''
    N, F = data_NF.shape
    Q, F2 = query_QF.shape
    assert F == F2

    # ========== TODO ==========
    # Compute pairwise Euclidean distances using broadcasting.
    #
    # Hint: Expand dimensions with np.newaxis so that subtraction
    #       broadcasts over Q and N simultaneously.
    #       query_QF[:, np.newaxis, :] has shape (Q, 1, F)
    #       data_NF[np.newaxis, :, :]  has shape (1, N, F)
    #       Their difference has shape (Q, N, F).
    #       Then square, sum over axis=2, and take the square root.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def find_k_nearest_indices(dist_QN, K):
    ''' Find indices of the K nearest neighbors from a distance matrix.

    Args
    ----
    dist_QN : 2D np.array, shape (Q, N)
        Pairwise distance matrix.
    K : int, must satisfy 1 <= K <= N
        Number of nearest neighbors to retrieve.

    Returns
    -------
    indices_QK : 2D np.array of ints, shape (Q, K)
        indices_QK[q, k] is the index into the original data array
        of the k-th nearest neighbor of query q.
        Neighbors are ordered from closest to farthest.
        Ties are broken by smaller index first (guaranteed by argsort stability).
    '''
    Q, N = dist_QN.shape
    K = int(K)
    if K < 1 or K > N:
        raise ValueError("K must satisfy 1 <= K <= N")

    # ========== TODO ==========
    # Use np.argsort along axis=1 to get sorted indices per query,
    # then slice the first K columns.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def calc_k_nearest_neighbors(data_NF, query_QF, K=1):
    ''' Compute and return k-nearest neighbors under Euclidean distance.

    This function combines euclidean_distances and find_k_nearest_indices,
    then gathers the actual feature vectors of the neighbors.

    Args
    ----
    data_NF : 2D np.array, shape (N, F)
        Each row is a feature vector of one data point.
    query_QF : 2D np.array, shape (Q, F)
        Each row is a feature vector of one query point.
    K : int, must satisfy 1 <= K <= N
        Number of neighbors to find per query.

    Returns
    -------
    neighb_QKF : 3D np.array, shape (Q, K, F)
        Entry [q, k] is the feature vector of the k-th nearest neighbor
        of the q-th query.
        Ties are broken by the original row order in data_NF.
    '''
    N, F = data_NF.shape
    Q, F2 = query_QF.shape
    assert F == F2
    K = int(K)
    if K < 1 or K > N:
        raise ValueError("K must satisfy 1 <= K <= N")

    # ========== TODO ==========
    # 1. Call euclidean_distances to get dist_QN of shape (Q, N)
    # 2. Call find_k_nearest_indices to get indices_QK of shape (Q, K)
    # 3. Use fancy indexing: data_NF[indices_QK] produces shape (Q, K, F)
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def predict_knn_classification(labels_N, nearest_indices_QK):
    ''' Predict class labels via majority vote among K nearest neighbors.

    Args
    ----
    labels_N : 1D np.array of ints, shape (N,)
        Integer class label for each data point (e.g., 0, 1, 2, ...).
    nearest_indices_QK : 2D np.array of ints, shape (Q, K)
        Indices of K nearest neighbors for each query.

    Returns
    -------
    predictions_Q : 1D np.array of ints, shape (Q,)
        Predicted class for each query by majority vote.
        Ties are broken in favor of the smallest class label.
    '''
    Q, K = nearest_indices_QK.shape

    # ========== TODO ==========
    # 1. Gather neighbor labels: labels_N[nearest_indices_QK] -> shape (Q, K)
    # 2. For each query, find the most common label.
    #    Hint: loop over Q queries. For each row of neighbor labels,
    #          np.bincount counts how many times each label appears,
    #          and np.argmax returns the label with the highest count.
    #          np.bincount naturally breaks ties toward the smallest index.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
