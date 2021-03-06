#from builtins import range
import numpy as np
from random import shuffle
import builtins
#from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg_l2, reg_l1 = 0):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg_l2: (float) regularization strength for L2 regularization
    - reg_l1: (float) default: 0. regularization strength for L1 regularization 
                to be used in Elastic Net Reg. if supplied, this function uses Elastic
                Net Regularization.

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    if reg_l1 == 0.:
        regtype = 'L2'
    else:
        regtype = 'ElasticNet'
    
    ##############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.      #
    # Store the loss in loss and the gradient in dW. If you are not careful      #
    # here, it is easy to run into numeric instability. Don't forget the         #
    # regularization! If regtype is set as 'L2' just implement L2 Regularization #
    # else implement both L2 and L1.                                             #
    ##############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****


    scores = X.dot(W)
    num_test = X.shape[0]
    num_classes = scores.shape[0]
    
    # softmax instance
    softmax = np.zeros_like(scores)
    
    exps = np.exp(scores)
    for i in range(num_classes):
        softmax[i] = exps[i] / np.sum(exps[i])
    logs = -np.log(softmax[range(num_test),y])
    
    # Loss
    loss = np.sum(logs) / num_test
    
    if(regtype =='L2'):
        loss += reg_l1 * np.sum(W*W)
    else:
        loss += reg_l2 * np.sum(np.absolute(W))
    
    
    softmax[np.arange(X.shape[0]), y] -= 1
    
    # dW
    for i in range(num_test):
        for j in range( X.shape[1]):
            for k in range(W.shape[1]):
                dW[j, k] += X[i, j] * softmax[i, k] 

    dW /=  num_test
    
    if(regtype == 'L2'):
        dW += reg_l1 * W
    else:
        dW += reg_l2 * W
        
    
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg_l2, reg_l1 = 0):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    if reg_l1 == 0:
        regtype = 'L2'
    else:
        regtype = 'ElasticNet'
    
    ##############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.   #
    # Store the loss in loss and the gradient in dW. If you are not careful      #
    # here, it is easy to run into numeric instability. Don't forget the         #
    # regularization! If regtype is set as 'L2' just implement L2 Regularization #
    # else implement both L2 and L1.                                             #
    ##############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    #print("----------------------")
    #print(reg_l1)    

    scores = X.dot(W)
    num_test = X.shape[0]
    
    # Softmax instance
    exps = np.exp(scores)
    sums = np.sum(exps, axis=1)
    softmax = exps[:] / sums[:, None]
    
    # Loss
    loss -= np.sum(np.log(softmax[np.arange(num_test), y]))
    loss /= num_test
    if(regtype =='L2'):
        loss += reg_l1 * np.sum(W*W)
    else:
        loss += reg_l2 * np.sum(np.absolute(W))

    softmax[np.arange(num_test), y] -= 1
    
    # dW
    dW = X.T.dot(softmax)
    dW /= num_test
    
    if(regtype == 'L2'):
        dW += reg_l1 * W
    else:
        dW += reg_l2 * W
    
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
