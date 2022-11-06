import numpy as np

def sigmoid(inputs, derivative=False):
    if derivative:
        return inputs * (1 - inputs)
    return 1 / (1 + (np.e ** -inputs))

def tanh(inputs, derivative=False):
    if derivative:
        return 1 - (np.tanh(inputs)**2)
    return np.tanh(inputs) 

def relu(inputs, derivative=False):
    if derivative:
        matrix = inputs
        matrix = np.maximum(0, matrix) 
        matrix = np.minimum(matrix, 1)      
        return matrix
    return np.maximum(0, inputs)

indexToLetter = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
}

letterToMatrix = {
    'A': [[1],[0],[0],[0]],
    "B": [[0],[1],[0],[0]],
    "C": [[0],[0],[1],[0]], 
    "D": [[0],[0],[0],[1]],
}
