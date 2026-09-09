"""
Doctests for hw2_logistic_regression.py
No changes needed to this file.

Setup
-----
>>> import numpy as np

Test generate_interaction_synthetic_classification_data
-------------------------------------------------------
>>> x1_gen, x2_gen, y_gen = generate_interaction_synthetic_classification_data(
...     n=50, noise_std=0.0, threshold=5.0, seed=0
... )
>>> x1_gen.shape, x2_gen.shape, y_gen.shape
((50,), (50,), (50,))

>>> score_gen = 1 + 2 * x1_gen + 3 * x2_gen + 4 * x1_gen * x2_gen
>>> np.array_equal(y_gen, (score_gen >= 5.0).astype(int))
True

>>> x1_gen_2, x2_gen_2, y_gen_2 = generate_interaction_synthetic_classification_data(
...     n=50, noise_std=0.0, threshold=5.0, seed=0
... )
>>> np.allclose(x1_gen, x1_gen_2) and np.allclose(x2_gen, x2_gen_2) and np.array_equal(y_gen, y_gen_2)
True


Define a tiny noiseless dataset for grading-preview doctests
>>> x1_N = np.array([0., 1., 0., 1.])
>>> x2_N = np.array([0., 0., 1., 1.])
>>> y_N = np.array([0, 0, 0, 1])


Test sigmoid
------------
>>> np.allclose(sigmoid(np.array([0., 2.])), np.array([0.5, 0.88079708]))
True


Test predict_proba_logistic_regression
--------------------------------------
>>> w_true = np.array([-4., 2., 3., 4.])
>>> np.allclose(
...     predict_proba_logistic_regression(x1_N, x2_N, w_true),
...     np.array([0.01798621, 0.11920292, 0.26894142, 0.99330715])
... )
True

>>> np.allclose(predict_proba_logistic_regression(x1_N, x2_N, np.zeros(4)), 0.5)
True


Test compute_bce_loss
---------------------
>>> p_zero = predict_proba_logistic_regression(x1_N, x2_N, np.zeros(4))
>>> np.allclose(compute_bce_loss(y_N, p_zero), 0.6931471805599453)
True


Test compute_bce_gradient
-------------------------
>>> grad_D = compute_bce_gradient(x1_N, x2_N, y_N, np.zeros(4))
>>> np.allclose(grad_D, np.array([0.25, 0.0, 0.0, -0.125]))
True


Test fit_logistic_regression_gd
-------------------------------
>>> w_fit, losses_L = fit_logistic_regression_gd(x1_N, x2_N, y_N, lr=1.0, num_epochs=2000)
>>> w_fit.shape
(4,)

>>> losses_L.shape
(2000,)

>>> bool(losses_L[0] > losses_L[-1])
True

>>> p_fit = predict_proba_logistic_regression(x1_N, x2_N, w_fit)
>>> np.array_equal((p_fit >= 0.5).astype(int), y_N)
True
"""

import numpy as np
from hw2_logistic_regression import (
    generate_interaction_synthetic_classification_data,
    sigmoid,
    predict_proba_logistic_regression,
    compute_bce_loss,
    compute_bce_gradient,
    fit_logistic_regression_gd,
)
