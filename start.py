from main import tokenize_by_sentence
from main import calculate_average_word_length
from main import calculate_average_sentence_length
from main import check_abbreviations
from main import find_rare_vocabulary
from main import find_words_caps
from main import find_complex_punctuation

if __name__ == '__main__':
    f = ('Hi my name is Dih. I am from russia. dog.')
    #'''f = open('Arthur_Conan_Doyle.txt', encoding='utf-8')
    #text = tokenize_by_sentence(f.read())
    #print(text)'''
    text = tokenize_by_sentence(f)
    print(text)
    text1 = 'Hi my name is Dih. I am from russia. acc. name dog from from from jiji jiji jiji.'



    word_average = calculate_average_word_length(text)
    print(word_average)

    sentence_average = calculate_average_sentence_length(text)
    print(sentence_average)
    
        with open('Arthur_Conan_Doyle.txt') as f:
        f = f.read().splitlines()
    word = find_words_caps(f)
    print(word)

    with open('Arthur_Conan_Doyle.txt') as file:
        file = file.read().split()
    file1 = list(file)
    punct = find_complex_punctuation(file1)
    print(punct)

    abrev = check_abbreviations(text)
    print(abrev)

    rare = find_rare_vocabulary(text1)
    print(rare)

    document_text = open('Arthur_Conan_Doyle.txt', 'r')
    text_strings = document_text.read().lower()
    rare_txt = find_rare_vocabulary(text_strings)
    print(rare_txt)
