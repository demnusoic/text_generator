# --------------------------
# Date Created: 11/27/18
# Date Modified: 11/28/18
# Author: Nick Leyson
# Generate random text based on a given source.
# --------------------------

from random import randint
from copy import copy
import argparse

class TextGen:
    """ Analyze and create text using a markov chain.
    """

    main_text = None
    word_chain = {}
    
    def __init__(self, main_text):
        """ Analyze the main text if available.
            main_text: The text to use
        """
        self.main_text = main_text
        # self.word_chain will be a nested dictionary like the following
        # {current_word: 
        #   {
        #       next_word: occurences,
        #       next_word: occurences,
        #       next_word: occurences,
        #   }
        # }
        self.analyze()

    def analyze(self):
        """ Analyze the main_text and set the word 
            change frequencies to self.word_chain.
        """ 
        words = self.main_text.split()
        i = 0
        # This condition will leave off the last word, since there are no 
        # further probabilities to set for it
        while i < len(words)-1:
            # If the current word is not in the dict, add it
            current_word = words[i]
            if current_word not in self.word_chain:
                self.word_chain[current_word] = {}

            current_word_prob = self.word_chain[current_word]
            next_word = words[i+1]

            # If the next word is not in the current word's
            # probability list, add it and set its occurences to 1 
            # otherwise increment the occurences of that word
            if next_word not in current_word_prob:
                current_word_prob[next_word] = 1
            else:
                current_word_prob[next_word] += 1
            i += 1
            
    def generate(self, limit=60, finish_sentences=False):
        """ Generate new text based on word frequencies.
            limit(int): the number of words to generate
            finish_sentences(bool): when set to True, generate text until 
            the last word ends in a period
        """
        keys = list(self.word_chain.keys())
        # To start at the beginning of a sentence
        # Set a word ending in a period as the start word, but do not add it to output text
        # create list including only words ending in a period, 
        starting_words = [word for word in keys if word[-1] == '.']
        # If filtered list is empty, set starting word from all words, otherwise set word from filtered list
        starting_words = keys if starting_words == [] else starting_words
        # select a random list entry as the starting word
        current_word = starting_words[randint(0, len(starting_words)-1)]
        # Create a list to hold the words that will make up the final text
        chained_words = []
        i = 0
        while i < limit or (finish_sentences == True and current_word[-1] != '.'):
            # Check that the current word has a list of possible next words, otherwise
            # an error occurs when the last word does not occur anywhere else in the input text
            # in which case it would occur in a next word dictionary, but not the word chain dictionary
            if current_word not in keys:
                current_word = keys[randint(0, len(keys)-1)]
            next_words = copy(self.word_chain[current_word])
            # Convert word occurences to a range ex:
            # {current_word: 
            #   {
            #       next_word: 8,
            #       next_word: 1,
            #       next_word: 2,
            #   }
            # }
            # Becomes
            #       next_word: range(0,8),
            #       next_word: range(8,9),
            #       next_word: range(9,11),

            # Get the total number of words that have occurred after this one
            possible_words = 0
            for next_word in next_words:
                # keep the occurrences
                occurrences = next_words[next_word]
                # Assign each word a numeric range based on it's occurrences
                next_words[next_word] = range(possible_words, possible_words+next_words[next_word])
                possible_words += occurrences
            
            # Get an index between 0 and possible words
            rand_index = randint(0, possible_words-1)

            # If the index is within the range corresponding to the word
            # then use that word
            for next_word in next_words:
                if rand_index in next_words[next_word]:
                    current_word = next_word
            # add the word to the list
            chained_words.append(current_word)
            i += 1
        # Join the words together with a space in between each
        return ' '.join(chained_words)

def main():
    # Accept one or more text file names as command line input
    # parse flags from command line input to determine how to modify text
    parser = argparse.ArgumentParser(description='Generate random text.')
    # add accepted arguments to the parser
    parser.add_argument("-f", "--files", 
                        help="The names of one or more text files separated by a space. ex. textgen.py -f file.txt file2.txt", 
                        nargs='+')
    parser.add_argument('-g', "--generate", 
                        type=int, 
                        help="The number of words to generate. ex. textgen.py -f file.txt -g 60")
    args = parser.parse_args()

    if args.files == None:
        exit("No input file. Try textgen.py -h for help.")

    # read in text from file(s)
    text = ""
    for filename in args.files:
        with open(filename, encoding="utf-8") as file:
            text += file.read()
    
    # create a class instance using the text from the files
    textgen = TextGen(text)

    # modify or generate text based on the input flags and print text
    if args.generate is not None:
        print(textgen.generate(args.generate, finish_sentences=True))
    else:
        print(textgen.generate(40, finish_sentences=True))

if __name__ == '__main__': 
    main()
    