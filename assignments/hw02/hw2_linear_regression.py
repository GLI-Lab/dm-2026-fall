'''
Linear Regression via Gradient Descent with NumPy

Build a complete linear regression training pipeline step by step, exercising
core NumPy skills: synthetic data generation, vectorized prediction, loss
computation, partial derivatives, and iterative optimization.

Examples
--------
See test_linear_regression.py for example inputs and expected outputs.

To verify correctness of your implementation, you can execute:

$ python -m doctest test_linear_regression.py -v
'''

import numpy as np


def generate_interaction_synthetic_data(n, noise_std=0.5, seed=42):
    ''' Generate synthetic regression data with an interaction term.

    Data is generated from
        y = 1 + 2*x1 + 3*x2 + 4*x1*x2 + eps
    where eps is Gaussian noise with standard deviation noise_std.

    Args
    ----
    n : int
        Number of samples to generate.
    noise_std : float, optional
        Standard deviation of Gaussian noise added to the targets.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    x1_N : 1D np.array, shape (N,)
        First feature values.
    x2_N : 1D np.array, shape (N,)
        Second feature values.
    y_N : 1D np.array, shape (N,)
        Regression targets.
    '''
    n = int(n)
    if n < 1:
        raise ValueError("n must be at least 1")

    # ========== TODO ==========
    # 1. Create a random number generator using the given seed
    # 2. Sample x1_N and x2_N uniformly from [0, 2]
    # 3. Sample Gaussian noise with standard deviation noise_std
    # 4. Compute y_N = 1 + 2*x1_N + 3*x2_N + 4*x1_N*x2_N + noise
    # 5. Return x1_N, x2_N, y_N
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def predict_interaction_linear_regression(x1_N, x2_N, w_D):
    ''' Predict targets for a 2-feature linear model with an interaction term.

    The model is
        yhat_i = b + w1*x1_i + w2*x2_i + w3*x1_i*x2_i
    where w_D = [b, w1, w2, w3].

    Args
    ----
    x1_N : 1D np.array, shape (N,)
        First feature value for each sample.
    x2_N : 1D np.array, shape (N,)
        Second feature value for each sample.
    w_D : 1D np.array, shape (4,)
        Parameter vector [b, w1, w2, w3].

    Returns
    -------
    yhat_N : 1D np.array, shape (N,)
        Predicted target for each sample.
    '''
    N = x1_N.shape[0]
    if x2_N.shape[0] != N:
        raise ValueError("x1_N and x2_N must have the same length")
    if w_D.shape[0] != 4:
        raise ValueError("w_D must have length 4")

    # ========== TODO ==========
    # Compute yhat_N using the formula
    #     yhat_i = b + w1*x1_i + w2*x2_i + w3*x1_i*x2_i
    # for all N samples without Python loops.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def compute_mse_loss(y_N, yhat_N):
    ''' Compute mean squared error loss.

    Args
    ----
    y_N : 1D np.array, shape (N,)
        True target values.
    yhat_N : 1D np.array, shape (N,)
        Predicted target values.

    Returns
    -------
    loss : float
        Mean squared error over all samples.
    '''
    N = y_N.shape[0]
    if yhat_N.shape[0] != N:
        raise ValueError("y_N and yhat_N must have the same length")

    # ========== TODO ==========
    # 1. Compute residuals r_N = yhat_N - y_N
    # 2. Return the mean of r_N ** 2
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def compute_mse_gradient(x1_N, x2_N, y_N, w_D):
    ''' Compute the gradient of MSE loss with respect to [b, w1, w2, w3].

    You should derive the four partial derivatives by hand from the model and
    MSE definition, then implement the result directly in NumPy.

    Args
    ----
    x1_N : 1D np.array, shape (N,)
        First feature value for each sample.
    x2_N : 1D np.array, shape (N,)
        Second feature value for each sample.
    y_N : 1D np.array, shape (N,)
        True target values.
    w_D : 1D np.array, shape (4,)
        Parameter vector [b, w1, w2, w3].

    Returns
    -------
    grad_D : 1D np.array, shape (4,)
        Gradient of the MSE loss with respect to [b, w1, w2, w3].
    '''
    N = x1_N.shape[0]
    if x2_N.shape[0] != N or y_N.shape[0] != N:
        raise ValueError("x1_N, x2_N, and y_N must have the same length")
    if w_D.shape[0] != 4:
        raise ValueError("w_D must have length 4")

    # ========== TODO ==========
    # 1. Compute predictions yhat_N using predict_interaction_linear_regression
    # 2. Compute residuals r_N = yhat_N - y_N
    # 3. Derive and implement the four partial derivatives:
    #       dL/db, dL/dw1, dL/dw2, dL/dw3
    # 4. Return them as a NumPy array of shape (4,)
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def fit_linear_regression_gd(x1_N, x2_N, y_N, lr=0.1, num_epochs=1000):
    ''' Fit the interaction linear regression model using batch gradient descent.

    Args
    ----
    x1_N : 1D np.array, shape (N,)
        First feature value for each sample.
    x2_N : 1D np.array, shape (N,)
        Second feature value for each sample.
    y_N : 1D np.array, shape (N,)
        True target values.
    lr : float, optional
        Learning rate.
    num_epochs : int, optional
        Number of gradient descent updates to perform.

    Returns
    -------
    w_D : 1D np.array, shape (4,)
        Learned parameter vector [b, w1, w2, w3].
    losses_L : 1D np.array, shape (num_epochs,)
        Loss value recorded before each parameter update.
    '''
    N = x1_N.shape[0]
    if x2_N.shape[0] != N or y_N.shape[0] != N:
        raise ValueError("x1_N, x2_N, and y_N must have the same length")
    num_epochs = int(num_epochs)
    if num_epochs < 1:
        raise ValueError("num_epochs must be at least 1")

    # ========== TODO ==========
    # 1. Initialize w_D as zeros of shape (4,)
    # 2. Create an empty Python list to store losses
    # 3. For each epoch:
    #       a. Compute predictions with predict_interaction_linear_regression
    #       b. Compute loss with compute_mse_loss
    #       c. Compute gradient with compute_mse_gradient
    #       d. Append loss to the list
    #       e. Update weights with w_D = w_D - lr * grad_D
    # 4. Convert the list of losses to a NumPy array before returning
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
