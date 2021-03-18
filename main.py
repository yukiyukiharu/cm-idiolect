import enchant
import re
import spacy
#dictionary = enchant.Dict('en_US')
#print(dictionary.check('Hello'))


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split('[.!?]', text)
    list_words = []
    for sentence in sentences:
        tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not tokens:
            continue
        list_words += tokens + ['<END>']
    return tuple(list_words)


def calculate_average_word_length(list_words: tuple) -> float:
    if not isinstance(list_words, tuple):
        raise ValueError

    list_words = list(list_words)
    letter_counter = 0
    word_counter = 0
    for token in list_words:
        if token != '<END>':
            word_counter += 1
            for letter in token:
                letter_counter += 1
    average = letter_counter / word_counter
    return average


def calculate_average_sentence_length(list_words: tuple) -> float:
    stop = '<END>'
    word_counter = 0
    sentence_counter = 0
    for token in list_words:
        if token != stop:
            word_counter += 1
        else:
            sentence_counter += 1
    average_word = word_counter / sentence_counter
    return average_word


def find_complex_punctuation(text: list) -> list:
    complex_punctuation = []
    pattern_same_punctuation = re.compile('([.!?]{2,})')
    for element in text:
        match = pattern_same_punctuation.search(element)
        if match:
            complex_punctuation.append(match.group(1))
    return complex_punctuation


def find_words_caps(file):
    word_list = []
    for line in file:
        for word in line.split(' '):
            if word.isupper() and len(word) > 1:
                if not word.isalpha():
                    word = re.sub(r'[^A-Za-z]', '', word)
                word_list.append(word)
    return word_list


def check_abbreviations (list_word: tuple): #нужна точка чтобы он смог найти, но при токенизации точка -> в <end> + проблемы с регистром
    d = {}
    with open("abrv.txt", encoding='utf-8') as file:
        for line in file:
            key, *value = line.split()
            d[key] = value
    #print(d)
    counter = 0
    abr = []
    for element in list_word:
        for k in d:
            if element.lower() == k:
                counter += 1
                abr.append(element)
    return counter, abr

def find_rare_vocabulary(text_string):

    frequency = {}
    match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)

    for word in match_pattern:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    list_freq = list(frequency.items())
    list_freq.sort(key=lambda i: i[1])
    return list_freq
