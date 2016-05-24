#! usr/bin/env python3.


"""
Analyzes text for word frequency

Counts word repetitions but
separates most common words.
Can identify words by root (eg focus = focuses, focused)
"""


# Modules to open, read docx files, count words, remove trash
from docx import Document
from collections import defaultdict
import re
import common_words as cw



# Characters to remove from text
LITTER = re.compile(r"(\:|\.|\s|\,|\;|\||)")      
COMMON = cw.get_words()



# Open docx file to read, return lowercase text
def get_text(filename):
    doc = Document(filename)
    doc.save('demo_n.docx')
    
    full_text = []
    for p in doc.paragraphs:
        full_text.append(p.text)

    text = ' '.join(full_text).split(' ')
    output = [w.lower() for w in text]
    return output
           
# print(get_text('demo.docx'), len(get_text('demo.docx')))  # len = 273



# Remove punctuation and numbers, return clean text
def clean_text(filename):
    text = get_text(filename)
    
    clean_text_space = [LITTER.sub('', w) for w in text]
    clean_text = [w for w in clean_text_space if w]
    return clean_text
    
# print(clean_text('demo.docx'), len(clean_text('demo.docx')))    # len = 259


"""
# Count words, return frequencies dictionary
def count_words(filename):
    text_to_count = clean_text(filename)
    
    word_frequencies = defaultdict(int)
    for w in text_to_count:
        word_frequencies[w] += 1
    
    categories = {
        1: [w for w in word_frequencies if word_frequencies[w] == 1],
        2: [w for w in word_frequencies if word_frequencies[w] == 2],
        3: [w for w in word_frequencies if word_frequencies[w] == 3],
        4: [w for w in word_frequencies if word_frequencies[w] == 4],
        5: [w for w in word_frequencies if word_frequencies[w] == 5],
        6: [w for w in word_frequencies if 5 < word_frequencies[w] <= 10],
        10: [w for w in word_frequencies if word_frequencies[w] > 10]
    }
    
    return categories
   
# print(count_words('demo.docx'))
"""


# Identify contractions and return 2 words
def undo_contract(word_list):
    word_list = [w for w in word_list if len(w) > 1]
    unhyphened_words = []
    for w in word_list:
        if '-' in w:
            h_index = w.index('-')
            unhyphened_words.append(w[:h_index])
            unhyphened_words.append(w[h_index + 1:])
    print(unhyphened_words)

# Split of common words, categorize rest by frequency
def categorize(filename):
    parse_text = clean_text(filename)
    
    common_words = defaultdict(int)
    remaining_words = defaultdict(int)
    misc_words = []
    for w in parse_text:
        if w in COMMON:
            common_words[w] += 1
        elif w.isalpha():
            remaining_words[w] += 1
        else:
            misc_words.append(w)
    
    misc_words = undo_contract(misc_words)
    
    return misc_words     
    
    
print(categorize('demo.docx'))


# Main engine, drill down, retrieve synonyms
def drill_down(filename):
    categories = count_words(filename)
    
    print("""
    Your text breaks down into the following categories by word frequency:
    """)
    
    for c in categories:
        print("Category {0}: {1} words".format(c, len(categories[c])))
        
    print("""
    Select a category to examine by typing in its number (eg, 2)
    """)
    
    while True:
        try:
            drill_choice = int(input("> "))
            for w in categories[drill_choice]:
                print(w)
            break
        except ValueError:
            print("Enter the digit, such as 1 or 2")   
    
    print("""
    Type a word if you would like to see its synonyms,
    otherwise press ESC
    """)
    
    while True:
        try:
            word_lookup = str(input("> "))
            if word_lookup in categories[drill_choice]:
                print("Looking up {}...".format(word_lookup))
                return word_lookup
                break
            else:
                print("That word is not in the list, but ok...")
                return word_lookup
                break
        except ValueError:
            print("That's not a word, try again")
                        
# drill_down('demo.docx')


"""
Synonym lookup

# Look up, return synonyms
def get_synonyms(filename):
    word_lookup = str(drill_down(filename) + '.n.01')
    
    synonyms = wn.synset('fraud.n.01')
    print(synonyms.lemma_names)
    
# get_synonyms('demo.docx')
"""  

"""
TODO

- Improve filtering and categorization
    1. Filter out common words into Common category
    2. Identify roots of remaining words
    3. Count frequencies of all variations of existing roots

- Improve display scheme
    1. Display as table
    2. Show root and total frequencies
    3. Show variations as subs and specific frequencies

"""
