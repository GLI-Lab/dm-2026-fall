"""
Doctests for hw2_linear_regression.py
No changes needed to this file.

Setup
-----
>>> import numpy as np

Test generate_interaction_synthetic_data
----------------------------------------
>>> x1_gen, x2_gen, y_gen = generate_interaction_synthetic_data(n=50, noise_std=0.0, seed=0)
>>> x1_gen.shape, x2_gen.shape, y_gen.shape
((50,), (50,), (50,))

>>> np.allclose(y_gen, 1 + 2 * x1_gen + 3 * x2_gen + 4 * x1_gen * x2_gen)
True

>>> x1_gen_2, x2_gen_2, y_gen_2 = generate_interaction_synthetic_data(n=50, noise_std=0.0, seed=0)
>>> np.allclose(x1_gen, x1_gen_2) and np.allclose(x2_gen, x2_gen_2) and np.allclose(y_gen, y_gen_2)
True


Define a tiny noiseless dataset for grading-preview doctests
>>> x1_N = np.array([0., 1., 0., 1.])
>>> x2_N = np.array([0., 0., 1., 1.])
>>> y_N = np.array([1., 3., 4., 10.])


Test predict_interaction_linear_regression
------------------------------------------
>>> w_D = np.array([1., 2., 3., 4.])
>>> predict_interaction_linear_regression(x1_N, x2_N, w_D)
array([ 1.,  3.,  4., 10.])

>>> predict_interaction_linear_regression(x1_N, x2_N, np.zeros(4))
array([0., 0., 0., 0.])


Test compute_mse_loss
---------------------
>>> yhat_zero = predict_interaction_linear_regression(x1_N, x2_N, np.zeros(4))
>>> np.allclose(compute_mse_loss(y_N, yhat_zero), 31.5)
True

>>> np.allclose(compute_mse_loss(y_N, y_N), 0.0)
True


Test compute_mse_gradient
-------------------------
>>> grad_D = compute_mse_gradient(x1_N, x2_N, y_N, np.zeros(4))
>>> np.allclose(grad_D, np.array([-9. , -6.5, -7. , -5. ]))
True

>>> grad_opt = compute_mse_gradient(x1_N, x2_N, y_N, np.array([1., 2., 3., 4.]))
>>> np.allclose(grad_opt, np.zeros(4))
True


Test fit_linear_regression_gd
-----------------------------
>>> w_fit, losses_L = fit_linear_regression_gd(x1_N, x2_N, y_N, lr=0.1, num_epochs=2000)
>>> w_fit.shape
(4,)

>>> losses_L.shape
(2000,)

>>> bool(losses_L[0] > losses_L[-1])
True

>>> np.allclose(w_fit, np.array([1., 2., 3., 4.]), atol=1e-2)
True

>>> np.allclose(predict_interaction_linear_regression(x1_N, x2_N, w_fit), y_N, atol=1e-2)
True
"""

import numpy as np
from hw2_linear_regression import (
    generate_interaction_synthetic_data,
    predict_interaction_linear_regression,
    compute_mse_loss,
    compute_mse_gradient,
    fit_linear_regression_gd,
)
