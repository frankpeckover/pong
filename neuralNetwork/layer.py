import random
import numpy as np
import neuralNetwork.helpers as helpers

class Layer:
    def __init__(self, nNeurons, nInputs, activationFunction):
        #fill weights with neuron rows and inputs elements in each row
        self.weights = np.random.uniform(-1, 1, (nNeurons, nInputs))
        #create bias array of ones with size of neurons
        self.biases = np.zeros((nNeurons, 1))
        self.activationFunction = activationFunction
        pass

    # def __repr__(self) -> str:
    #     return "\nneurons: {}\nweights: {}\nbiases: {}\n".format(len(self.biases), self.weights, self.biases)

    #determine dot product of weight matrix and previous layers inputs as 1D array
    def calculateOutput(self, inputs):
        output = np.dot(self.weights, inputs)
        output += self.biases
        return output

    #put outputs through activation function
    def calculateActivation(self, inputs):
        return self.activationFunction(inputs)

    #use deltas input from previous layer and training rate to update layer weight matrix
    def updateWeights(self, delta, input, rate):
        changes = np.dot(delta, input.T) * rate 
        self.weights += changes
        return True

    def updateBiases(self, gradient):
        self.biases += gradient
        pass

    def mutateWeights(self, mutationRate):
        for row in range(len(self.weights)):
            for weight in range(len(self.weights[0])):
                if random.random() <= mutationRate:
                    self.weights[row][weight] = random.uniform(-1, 1)
        pass

    def mutateBiases(self, mutationRate):
        for row in range(len(self.biases)):
            for bias in range(len(self.biases[0])):
                if random.random() <= mutationRate:
                    self.weights[row][bias] = random.uniform(-1, 1)
        pass