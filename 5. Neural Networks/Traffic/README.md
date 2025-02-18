optimizer="adam",
loss="categorical_crossentropy",
metrics=["accuracy"]

1st: Best
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
Dense: 256, Dropout 0.5
Dense: 128, Dropout 0.5
Dense: 43
Result: 
1. accuracy: 0.9079 - loss: 0.3351
2. accuracy: 0.8856 - loss: 0.3963


2nd:
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
Dense: 128, Dropout 0.5
Dense: 64, Dropout 0.5
Dense: 43
Result: 
1. accuracy: 0.5972 - loss: 1.1617
2. accuracy: 0.8240 - loss: 0.5436
3. accuracy: 0.7836 - loss: 0.7021
4. accuracy: 0.7356 - loss: 0.9147

3rd:
Activation: all relu, softmax output layer
3x Conv, MaxPool
Flatten
Dense: 512, Dropout 0.5
Dense: 256, Dropout 0.5
Dense: 128, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.7270 - loss: 0.8497

4rd:
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
Dense: 512, Dropout 0.5
Dense: 256, Dropout 0.5
Dense: 128, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.7249 - loss: 0.8152

5th:
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
2x Dense: 128, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.0564 - loss: 3.5047 ???
2. accuracy: 0.6617 - loss: 1.0555
3. accuracy: 0.8968 - loss: 0.3808
4. accuracy: 0.8067 - loss: 0.6488

6th:
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
2x Dense: 256, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.8871 - loss: 0.3679
2. accuracy: 0.9305 - loss: 0.2522

7th:
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
2x Dense: 512, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.9434 - loss: 0.2089
2. accuracy: 0.9438 - loss: 0.1982

8th:
Activation: all relu, softmax output layer
3x Conv, MaxPool
Flatten
2x Dense: 512, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.9034 - loss: 0.3179
2. accuracy: 0.9106 - loss: 0.3006

9th
Activation: all relu, softmax output layer
2x Conv, MaxPool
Flatten
3x Dense: 512, Dropout 0.5
Dense: 43
Result:
1. accuracy: 0.8716 - loss: 0.3909
2. accuracy: 0.7895 - loss: 0.6647

# Based on the few testings:
Increasing size of hidden layers helps increase accuracy
Shape (of size: 1 -> 2 -> 1, 1 -> 2 -> 3, 3 -> 2 -> 1) of hidden layer, not so obvious, not enough tests
Adding more Conv layers may not increase accuracy
