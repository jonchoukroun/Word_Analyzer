#! usr/bin/env python3.
# -*- coding: utf-8 -*-


"""
Analyzes text for word frequency

Counts word repetitions but
separates most common words.
Can identify words by root (eg focus = focuses, focused)
"""


# Modules to open, read docx files, count words, remove trash
from docx import Document
from collections import defaultdict, OrderedDict
import re
import common_words as cw



# Characters to remove from text
LITTER = re.compile(r"(\:|\.|\s|\,|\;|\||)")      
COMMON = cw.get_words()



# Open docx file to read, return lowercase text
def get_text(filename):
    doc = Document(filename)
    doc.save('temp.docx')
    
    full_text = []
    for p in doc.paragraphs:
        full_text.append(p.text)

    text = ' '.join(full_text).split(' ')
    text = [w.lower() for w in text]
    return text
           
# print(get_text('demo.docx'), len(get_text('demo.docx')))  # len = 273



# Remove punctuation and numbers, return clean text
def clean_text(text):
    text_to_clean = get_text(text)
    
    clean_text_space = [LITTER.sub('', w) for w in text_to_clean]
    clean_text = [w for w in clean_text_space if w]
    return clean_text
    
# print(clean_text('demo.docx'), len(clean_text('demo.docx')))    # len = 259



# Identify contractions and return 2+ letter words
def undo_hyphen(word_list):
    word_list = [w for w in word_list if len(w) > 1] # remove single characters
    unhyphenated_words = []
    for w in word_list:
        if '-' in w:
            h_index = w.index('-')
            unhyphenated_words.append(w[:h_index])
            unhyphenated_words.append(w[h_index + 1:])
        else:
            unhyphenated_words.append(w)
            
    return unhyphenated_words
    
    

# Split of common words, categorize rest by frequency
def parse_words(text):
    parse_text = clean_text(text)
    
    parse_ready_text = undo_hyphen(parse_text)
    
    common_words = defaultdict(int)
    unique_words = defaultdict(int)
    misc_words = []
    for w in parse_text:
        if w in COMMON:
            common_words[w] += 1
        elif re.search(r'[a-z]', w):
            unique_words[w] += 1
        else:
            misc_words.append(w)
            
    return common_words, unique_words, misc_words
    
# print(parse_words('demo.docx'))



# Create categories of word group
# TODO: Prettify output 
def format_words(words):
    print("""
    Word: # of occurances
    ---------------------
            """)
    
    sorted_words = [(w, words[w]) for w in sorted(words, key=words.get, reverse=True)]
    for word, rep in sorted_words:
        print("\t{}: {}".format(word, rep))

# Main engine, drill down, retrieve synonyms
def main_menu(filename):
    common_words = parse_words(filename)[0]
    unique_words = parse_words(filename)[1]

    
    print("""
    Select an analysis by entering its number:
    
        1. Common words - from most commonly used English words
        2. Unique words - your use of non-common words
        3. ...
    """)
    
    while True:
        try:
            group_select = int(input('> '))
            if group_select == 1:
                format_words(common_words)     # use format function
                break
            elif group_select == 2:
                format_words(unique_words)
                break
            else:
                print("Additional functionalities coming soon. Try again.")
        except ValueError:
            print("That is not an integer, try again.")
                        
main_menu('demo.docx')
