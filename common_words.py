#! usr/bin/env python3.

"""
Prep words text file

Open ranked text file
Strip numbers
Return list of lowercase words
"""

import re

# Global variables: numbers list
# NUMBERS = re.compile(r'\d')
LITTER = re.compile(r'(\d|\brank\b|\bword\b)')

def get_words():
    f = open('words.txt', 'r')
    text = f.read().split()
    
    words_space = [LITTER.sub('', w.lower()) for w in text] # remove numbers
    words = [w for w in words_space if w] # remove whitespace
    
    f.close()
    
    
    # out = '|'.join(words)     used to make common words regex
    
    return words
    
get_words()