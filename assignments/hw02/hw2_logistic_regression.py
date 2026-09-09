'''
Logistic Regression via Gradient Descent with NumPy

Build a complete logistic regression training pipeline step by step, exercising
core NumPy skills: synthetic data generation, sigmoid probabilities, binary
cross-entropy loss, partial derivatives, and iterative optimization.

Examples
--------
See test_logistic_regression.py for example inputs and expected outputs.

To verify correctness of your implementation, you can execute:

$ python -m doctest test_logistic_regression.py -v
'''

import numpy as np


def generate_interaction_synthetic_classification_data(
    n, noise_std=0.5, threshold=5.0, seed=42
):
    ''' Generate binary classification data with an interaction term.

    Data is generated from the continuous interaction score
        s = 1 + 2*x1 + 3*x2 + 4*x1*x2 + eps
    where eps is Gaussian noise with standard deviation noise_std.
    Binary labels are then assigned by thresholding the score:
        y = 1 if s >= threshold else 0

    Args
    ----
    n : int
        Number of samples to generate.
    noise_std : float, optional
        Standard deviation of Gaussian noise added to the score.
    threshold : float, optional
        Threshold used to convert the continuous score into binary labels.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    x1_N : 1D np.array, shape (N,)
        First feature values.
    x2_N : 1D np.array, shape (N,)
        Second feature values.
    y_N : 1D np.array of ints, shape (N,)
        Binary labels in {0, 1}.
    '''
    n = int(n)
    if n < 1:
        raise ValueError("n must be at least 1")

    # ========== TODO ==========
    # 1. Create a random number generator using the given seed
    # 2. Sample x1_N and x2_N uniformly from [0, 2]
    # 3. Sample Gaussian noise with standard deviation noise_std
    # 4. Compute the interaction score
    #       s_N = 1 + 2*x1_N + 3*x2_N + 4*x1_N*x2_N + noise
    # 5. Convert scores to binary labels using the given threshold
    # 6. Return x1_N, x2_N, y_N
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def sigmoid(z_N):
    ''' Compute the sigmoid function elementwise.

    Args
    ----
    z_N : np.array or scalar
        Input values.

    Returns
    -------
    sigma_N : np.array or scalar
        Sigmoid-transformed values.
    '''
    # ========== TODO ==========
    # Compute sigma(z) = 1 / (1 + exp(-z)) elementwise.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def predict_proba_logistic_regression(x1_N, x2_N, w_D):
    ''' Predict class-1 probabilities for logistic regression.

    The model is
        p_i = sigmoid(b + w1*x1_i + w2*x2_i + w3*x1_i*x2_i)
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
    p_N : 1D np.array, shape (N,)
        Predicted probability of class 1 for each sample.
    '''
    N = x1_N.shape[0]
    if x2_N.shape[0] != N:
        raise ValueError("x1_N and x2_N must have the same length")
    if w_D.shape[0] != 4:
        raise ValueError("w_D must have length 4")

    # ========== TODO ==========
    # 1. Compute z_N = b + w1*x1_N + w2*x2_N + w3*x1_N*x2_N
    # 2. Apply sigmoid to z_N
    # 3. Return the predicted probabilities
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def compute_bce_loss(y_N, p_N):
    ''' Compute binary cross-entropy loss.

    Args
    ----
    y_N : 1D np.array, shape (N,)
        True binary labels.
    p_N : 1D np.array, shape (N,)
        Predicted probabilities.

    Returns
    -------
    loss : float
        Mean binary cross-entropy over all samples.
    '''
    N = y_N.shape[0]
    if p_N.shape[0] != N:
        raise ValueError("y_N and p_N must have the same length")

    # ========== TODO ==========
    # 1. Add a small epsilon to guard against log(0)
    # 2. Compute the BCE loss
    #      -(1/N) * sum[y*log(p) + (1-y)*log(1-p)]
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def compute_bce_gradient(x1_N, x2_N, y_N, w_D):
    ''' Compute the gradient of BCE loss with respect to [b, w1, w2, w3].

    You should derive the four partial derivatives by hand from the model and
    BCE definition, then implement the result directly in NumPy.

    Args
    ----
    x1_N : 1D np.array, shape (N,)
        First feature value for each sample.
    x2_N : 1D np.array, shape (N,)
        Second feature value for each sample.
    y_N : 1D np.array, shape (N,)
        True binary labels.
    w_D : 1D np.array, shape (4,)
        Parameter vector [b, w1, w2, w3].

    Returns
    -------
    grad_D : 1D np.array, shape (4,)
        Gradient of the BCE loss with respect to [b, w1, w2, w3].
    '''
    N = x1_N.shape[0]
    if x2_N.shape[0] != N or y_N.shape[0] != N:
        raise ValueError("x1_N, x2_N, and y_N must have the same length")
    if w_D.shape[0] != 4:
        raise ValueError("w_D must have length 4")

    # ========== TODO ==========
    # 1. Compute predicted probabilities p_N using predict_proba_logistic_regression
    # 2. Compute prediction errors e_N = p_N - y_N
    # 3. Derive and implement the four partial derivatives:
    #       dL/db, dL/dw1, dL/dw2, dL/dw3
    # 4. Return them as a NumPy array of shape (4,)
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def fit_logistic_regression_gd(x1_N, x2_N, y_N, lr=0.5, num_epochs=1000):
    ''' Fit the interaction logistic regression model using batch gradient descent.

    Args
    ----
    x1_N : 1D np.array, shape (N,)
        First feature value for each sample.
    x2_N : 1D np.array, shape (N,)
        Second feature value for each sample.
    y_N : 1D np.array, shape (N,)
        True binary labels.
    lr : float, optional
        Learning rate.
    num_epochs : int, optional
        Number of gradient descent updates to perform.

    Returns
    -------
    w_D : 1D np.array, shape (4,)
        Learned parameter vector [b, w1, w2, w3].
    losses_L : 1D np.array, shape (num_epochs,)
        BCE loss recorded before each parameter update.
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
    #       a. Compute probabilities with predict_proba_logistic_regression
    #       b. Compute loss with compute_bce_loss
    #       c. Compute gradient with compute_bce_gradient
    #       d. Append loss to the list
    #       e. Update weights with w_D = w_D - lr * grad_D
    # 4. Convert the list of losses to a NumPy array before returning
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
