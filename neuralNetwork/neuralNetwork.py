import numpy as np
from neuralNetwork.layer import Layer
import neuralNetwork.helpers as helpers


class NeuralNetwork:
    #networkShape is an int array of layer sizes eg. [2, 3, 2]
    def __init__(self, networkShape, trainingRate=0.1):
        #array of layers
        self.layers = []
        self.networkShape = networkShape
        self.activationFunction = helpers.sigmoid
        self.trainingRate = trainingRate
        self.addHiddenLayers(self.layers, networkShape)
        pass

    #loop through networkShape array and build hiddenlayers
    def addHiddenLayers(self, layerArray, networkShape):
        arr = layerArray
        for i in range(1, len(networkShape)):
            hiddenLayer = Layer(networkShape[i], networkShape[i - 1], self.activationFunction)
            arr.append(hiddenLayer)
        return arr


    def propagateForward(self, inputs):

        #store each layers output in an array
        outputs = []
        for i, layer in enumerate(self.layers):

            #if first layer in the array, calculate outputs based on the input layer
            if i == 0:
                outputs.append(layer.calculateActivation(layer.calculateOutput(inputs)))

            #outputs are calculated on previous layers outputs
            else:
                outputs.append(layer.calculateActivation(layer.calculateOutput(outputs[i - 1])))
        return outputs


    def propagateBackward(self, propagationOutputs, networkInput, error):
        
        #initialise empty deltas array sized for number of layers so that delta index corresponds to layer index
        deltas = [0] * len(self.layers)

        #loop backwards through the layers
        for i in reversed(range(len(self.layers))):

            #if we are at the output layer
            if i == len(self.layers) - 1:

                #calculate deltas based on output error and derivative of activiation function
                deltas[i] = error * self.layers[i].activationFunction(propagationOutputs[-1], True)

                #update weights
                self.layers[i].updateWeights(deltas[i], propagationOutputs[i - 1], self.trainingRate)
                #update biases with deltas
                self.layers[i].updateBiases(deltas[i])

            #first layer of the network
            elif i == 0:
                layerError = np.dot(self.layers[i + 1].weights.T, deltas[i + 1])
                deltas[i] = layerError * self.layers[i].activationFunction(propagationOutputs[i], True)

                #update weights based on total newtork inputs
                self.layers[i].updateWeights(deltas[i], networkInput, self.trainingRate)  
                self.layers[i].updateBiases(deltas[i])
            else:
                layerError = np.dot(self.layers[i + 1].weights.T, deltas[i + 1])
                deltas[i] = layerError * self.layers[i].activationFunction(propagationOutputs[i], True)
                self.layers[i].updateWeights(deltas[i], propagationOutputs[i - 1], self.trainingRate)  
                self.layers[i].updateBiases(deltas[i])
            
        # print(deltas)
        return deltas


    #train the neural network with data and adjust weights
    def train(self, inputs, expectedOutputs):
        mse = []
        for i, input in enumerate(inputs):

            #propagate forwards through network to get output
            output = self.propagateForward(input)

            #calculate error based on output from forward propagation
            error = self.calculateRawError(output[-1], helpers.letterToMatrix[expectedOutputs[i]])
            mse.append(self.calculateMSE(error))

            #propagate the error backwards to train
            self.propagateBackward(output, input, error)
        return mse

    #cost function determines distance from desired value to be used in training
    def calculateRawError(self, output, expectedOutput):
        error = expectedOutput - output
        return error

    def calculateMSE(self, error):
        return np.mean(np.square(error))

        
    def accuracy(self, testData, expectedOutputs):
        correct = 0
        for i, data in enumerate(testData):
            prediction =  np.argmax(self.propagateForward(data)[-1])
            result = helpers.indexToLetter[prediction] == expectedOutputs[i]
            if result:
                correct += 1
        return float(correct) / len(testData)

    def mutate(self, mutationRate):
        for layer in self.layers:
            layer.mutateWeights(mutationRate)
            layer.mutateBiases(mutationRate)
        pass

    def copy(self):
        new = NeuralNetwork(self.networkShape)
        new.layers = self.layers
        return new