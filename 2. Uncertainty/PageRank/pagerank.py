import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    res = {}

    # Page has no outgoing links
    if len(corpus[page]) == 0:
        prob_dist = 1 / len(corpus)
        for _ in corpus:
            res[_] = prob_dist
    else:
        # add the `1 - damping_factor` to each page
        for _ in corpus:
            prob_dist = (1 - damping_factor) / len(corpus)
            res[_] = prob_dist
        # randomly choose one of the links from page with equal probability.
        page_link = corpus[page]
        num_links = len(page_link)
        final_prob = damping_factor / num_links
        for _ in page_link:
            res[_] += final_prob
    
    return res

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res = {}

    # set all pages to 0 times visited
    for page in corpus:
        res[page] = 0

    # Randomly generate first sample
    random_page = random.choice(list(corpus.keys()))
    res[random_page] += 1

    transition_prob = transition_model(corpus, random_page, damping_factor)

    for i in range(n-1):
        transition_prob = transition_model(corpus, random_page, damping_factor)
        keys = list(transition_prob.keys())
        weights = list(transition_prob.values())
        random_page = random.choices(keys, weights=weights, k=1)[0]
        res[random_page] += 1
    
    # change to probability
    for _ in res:
        res[_] = res[_] / n

    return res

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res = {}

    # assigning each page a rank of 1 / N
    for page in corpus:
        res[page] = 1 / len(corpus)

    # cont.
    while True:
        converged = True
        for page in res:
            curr_prob = res[page]

            # first part of formula
            new_prob = (1 - damping_factor) / len(corpus)

            # second part of formula.
            # get all page's 'i's and its NumLinks
            parents = {}

            for _ in corpus:
                if page in corpus[_]:
                    parents[_] = len(corpus[_])
            
            for i in parents:
                new_prob += damping_factor * (res[i] / parents[i])
            
            # check curr and new rank values
            diff = max(curr_prob, new_prob) - min(curr_prob, new_prob)
            if diff > 0.001:
                converged = False

            # assign the new prob
            res[page] = new_prob

        if converged:
            break

    return res


if __name__ == "__main__":
    main()

