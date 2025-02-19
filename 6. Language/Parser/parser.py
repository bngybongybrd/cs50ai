import nltk
from nltk.tokenize import word_tokenize
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> G | G Conj G
G -> NP VP | VP NP | VP | NP
VP -> V | V NP | V NP PP | V PP | V Adv
PP -> P NP
NP -> AdjN | Det AdjN
AdjN -> N | Adj N PP | Adj AdjN | N Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.strip(".\n ")
    words = sentence.split()
    res = []

    # convert all to lowercase
    for i in range(len(words)):
        # ok = False
        # for letter in words[i]:
        #     if letter.islapha():
        #         ok = True
        # if ok:
        #     res.append(words[i].lower())
        if all(letter.isalpha() for letter in words[i]):
            res.append(words[i].lower())

    #print(res)
    return res


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    gen = tree.subtrees()
    next(gen)
    res = []
    for s in gen:
        #print(s)
        if s.label() == "NP":
            add = True
            subgen = s.subtrees()
            next(subgen)
            for m in subgen:
                #print(m.label())
                if m.label() == "NP":
                    add = False
            if add:
                res.append(s)
    
    #print(f"res: {res}")
    return res


if __name__ == "__main__":
    main()
