# cs50ai
## 0. Search
- Project 0:

  - Degrees

    Implementation of a search algorithm to find the shortest path between 2 actors, based on the "Six Degrees of Kevin Bacon" game

  - Tic-Tac-Toe

    Using Minimax to implement an AI to play Tic-Tac-Toe.

## 1. Knowledge
- Project 1:

  - Knights

    Write a program to solve logic puzzles, using propositional logic.

    Touches on skills such as being able to convert worded knowledge of a problem into code knowledge for the computer to understand

  - Minesweeper
 
    Write an AI to play Minesweeper.

    Teaches different ways to represent knowledge for a computer
    
## 2. Uncertainty
- Project 2:

  - PageRank
 
    Write an AI to rank web pages by importance.

    Calculating PageRank by sampling pages from a Markov Chain random surfer and by iteratively applying the PageRank formula.

  - Heredity
 
    Write an AI to assess the likelihood that a person will have a particular genetic trait.

    Forming a Bayesian network to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, it will infer the probability distribution   
for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

## 3. Optimization
- Project 3:

  - Crossword

    AI to generate crossword puzzles.
    
    Mainly the implementation of functions to enforce Node Consistency, Arc Consistency, order domain values according to the least-constraining values heuristic, selecting unassigned variable according to the minimum remaining value heuristic and then the degree heuristic, and finally the backtrack search algorithm which encompasses the previous few functions mentioned.

## 4. Learning
- Project 4:

  - Shopping
 
    Write an AI to predict whether online shopping customers will complete a purchase.
    Loading, cleaning, formating of data from CSV file into program to be used by the model

  - Nim

    Write an AI that teaches itself to play Nim through reinforcement learning.
    
    Implementation of Q-learning formula (Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)) to allow AI to select the best possible choice of action. The choice of action uses either the epsilon-greedy algorithm or just chooses its action greedily based on the use's choice.

## 5. Neural Networks
- Project 5:

  - Write an AI to identify which traffic sign appears in a photograph.
 
    Processes data set of images into numpy multidimensional array, and creating a CNN by manually adding layers
    Documentation and investigating
    - different options for number of convolutional and pooling layers
    - different numbers and sizes of filters for convolutional layers
    - different pool sizes for pooling layers
    - different numbers and sizes of hidden layers
    - dropout (proportion of nodes ignored to prevent overfitting)
## 6. Language
