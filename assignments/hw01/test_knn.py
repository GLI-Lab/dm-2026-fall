"""
Doctests for hw1_knn.py
No changes needed to this file.

Setup
-----
>>> import numpy as np

Define example dataset with N=20 points in 2D (F=2)
>>> data_NF = np.array([
...     [ 0., 0.],
...     [ 1., 1.],
...     [ 2., 0.],
...     [ 0., 2.],
...     [ 4., 4.],
...     [ 5., 5.],
...     [ 6., 4.],
...     [ 4., 6.],
...     [ 8., 1.],
...     [ 9., 2.],
...     [10., 1.],
...     [ 8., 3.],
...     [12., 8.],
...     [13., 9.],
...     [14., 8.],
...     [12.,10.],
...     [17., 5.],
...     [18., 6.],
...     [19., 5.],
...     [17., 7.]])
>>> query_QF = np.array([
...     [ 0.2, 0.1],
...     [ 4.2, 4.1],
...     [ 8.7, 1.8],
...     [12.7, 8.2],
...     [17.8, 5.8]])


Test euclidean_distances
------------------------
>>> dist_QN = euclidean_distances(data_NF, query_QF)
>>> dist_QN.shape
(5, 20)

# Distance from [0.2, 0.1] to [0, 0] should be sqrt(0.05)
>>> np.allclose(dist_QN[0, 0], np.sqrt(0.05))
True

# Distance from [4.2, 4.1] to [4, 4] should be sqrt(0.05)
>>> np.allclose(dist_QN[1, 4], np.sqrt(0.05))
True

# Distance from [17.8, 5.8] to [18, 6] should be sqrt(0.08)
>>> np.allclose(dist_QN[4, 17], np.sqrt(0.08))
True


Test find_k_nearest_indices
---------------------------
>>> dist_QN = euclidean_distances(data_NF, query_QF)
>>> indices_QK = find_k_nearest_indices(dist_QN, K=3)
>>> indices_QK.shape
(5, 3)

# [0.2, 0.1] is closest to data[0], then data[1], then data[2]
>>> indices_QK[0].tolist()
[0, 1, 2]

# [4.2, 4.1] is closest to data[4], then data[5], then data[6]
>>> indices_QK[1].tolist()
[4, 5, 6]

# [8.7, 1.8] is closest to data[9], then data[8], then data[11]
>>> indices_QK[2].tolist()
[9, 8, 11]

# [12.7, 8.2] is closest to data[12], then data[13], then data[14]
>>> indices_QK[3].tolist()
[12, 13, 14]

# [17.8, 5.8] is closest to data[17], then data[16], then data[18]
>>> indices_QK[4].tolist()
[17, 16, 18]


Test calc_k_nearest_neighbors K=1
----------------------------------
>>> neighb_QKF = calc_k_nearest_neighbors(data_NF, query_QF, K=1)
>>> neighb_QKF.shape
(5, 1, 2)

>>> neighb_QKF[0]
array([[0., 0.]])

>>> neighb_QKF[1]
array([[4., 4.]])

>>> neighb_QKF[2]
array([[9., 2.]])

>>> neighb_QKF[3]
array([[12.,  8.]])

>>> neighb_QKF[4]
array([[18.,  6.]])


Test calc_k_nearest_neighbors K=3
----------------------------------
>>> neighb_QKF = calc_k_nearest_neighbors(data_NF, query_QF, K=3)
>>> neighb_QKF.shape
(5, 3, 2)

>>> np.allclose(neighb_QKF[0], np.array([[0., 0.], [1., 1.], [2., 0.]]))
True

>>> np.allclose(neighb_QKF[1], np.array([[4., 4.], [5., 5.], [6., 4.]]))
True

>>> np.allclose(neighb_QKF[2], np.array([[9., 2.], [8., 1.], [8., 3.]]))
True

>>> np.allclose(neighb_QKF[3], np.array([[12., 8.], [13., 9.], [14., 8.]]))
True

>>> np.allclose(neighb_QKF[4], np.array([[18., 6.], [17., 5.], [19., 5.]]))
True


Test predict_knn_classification
-------------------------------
>>> labels_N = np.array([1, 1, 0, 2, 0, 0, 2, 1, 2, 2, 0, 1, 1, 1, 0, 2, 0, 2, 2, 0])
>>> indices_QK = find_k_nearest_indices(euclidean_distances(data_NF, query_QF), K=3)

# Query 0 neighbors: indices [0,1,2] -> labels [1,1,0] -> majority 1
# Query 1 neighbors: indices [4,5,6] -> labels [0,0,2] -> majority 0
# Query 2 neighbors: indices [9,8,11] -> labels [2,2,1] -> majority 2
# Query 3 neighbors: indices [12,13,14] -> labels [1,1,0] -> majority 1
# Query 4 neighbors: indices [17,16,18] -> labels [2,0,2] -> majority 2
>>> predict_knn_classification(labels_N, indices_QK).tolist()
[1, 0, 2, 1, 2]

>>> labels_N2 = np.array([0, 1, 2, 0, 1, 2, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 1, 2, 0, 0])

# Each query sees three different labels, so ties break toward the smallest label 0
>>> predict_knn_classification(labels_N2, indices_QK).tolist()
[0, 0, 0, 0, 0]

"""

import numpy as np
from hw1_knn import (
    euclidean_distances,
    find_k_nearest_indices,
    calc_k_nearest_neighbors,
    predict_knn_classification,
)
