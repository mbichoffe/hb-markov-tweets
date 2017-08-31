"""Generate Markov text from text files."""

from random import choice
import sys
import twitter
import os

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

def open_and_read_file(*file_paths):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    text = ''

    for file_path in file_paths[0]:
        f = open(file_path)
        text += f.read()
        f.close()

    return text


def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = text_string.split()

    if n > len(words):
        print 'Length of n cannot be greater than text string length.'
        sys.exit()

    for i in range(len(words) - n):

        key = tuple(words[i: n + i])

        value = words[i + n]

        chains.setdefault(key, []).append(value)

    return chains


def make_first_link(chains):

    first_link = []

    caps_key = filter(lambda x: x[0][0].isupper(), chains.keys())

    start_link = choice(caps_key)

    [first_link.append(word) for word in start_link]

    next_word = choice(chains[start_link])

    first_link.append(next_word)

    return first_link


def make_text(chains, n):
    """Return text from chains."""
    # get random key to start the link
        # append into words list
        # look up key in dictionary
            # get random word within the list
            # append into words list
        # evaluate last two words in words[] to find key in dictionary

    markov_sentence = make_first_link(chains)

    while (len(' '.join(markov_sentence))) <= 130:

        last_n_words = tuple(markov_sentence[-n:])

        if last_n_words not in chains:
            break

        last_word = choice(chains[last_n_words])

        markov_sentence.append(last_word)

        if last_word[-1] in '.!?"-':
            break

    return " ".join(markov_sentence)


def tweet(chains, n):

    random_text = make_text(chains, n)
    print 'first', random_text

    status = api.PostUpdate(random_text)

    tweet_again = True
    while tweet_again:
        exit = raw_input("Enter to tweet again [q to quit]> ")
        if exit.lower() != "q":
            random_text = make_text(chains, n)
            print 'loop', random_text
            status = api.PostUpdate(random_text)
            print status.text
        else:
            tweet_again = False


input_path = sys.argv[1:]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

n = 3

# Get a Markov chain
chains = make_chains(input_text, n)
# print chains
print make_text(chains, n)
tweet(chains, n)
