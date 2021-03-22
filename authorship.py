import nltk
import string
import pandas as pd
from main import find_lex_variety
from main import find_average_word_len
from main import find_average_sentence_len

list_direction = ['VanillaChip101+.txt', 'imadetheline+.txt', 'another_author.txt']
lex_var_list = []
word_len_list = []
sentence_len_list = []
for element in list_direction:
    file = open(element, encoding='utf-8')
    s = file.read().split()
    s = str(s)

    tokens = nltk.word_tokenize(s)

    remove_punctuation = str.maketrans('', '', string.punctuation)
    tokens_ = [x for x in [t.translate(remove_punctuation).lower() for t in tokens] if len(x) > 0]
    # чтобы убрать еще и апострофы
    for element in tokens_:
        if element.isalpha():
            continue
        else:
            tokens_.remove(element)

    #print(tokens_)

    lex_variety = find_lex_variety(tokens_)
    lex_var_list.append(lex_variety)

    word_len = find_average_word_len(tokens_)
    word_len_list.append(word_len)

    sentence_len = find_average_sentence_len(s)
    sentence_len_list.append(sentence_len)

df = pd.DataFrame({'Author': ['1', '2', '3'], 'lex variety': [lex_var_list[0], lex_var_list[1], lex_var_list[2]],
                   'average word len': [word_len_list[0], word_len_list[1], word_len_list[2]],
                   'average sentence len': [sentence_len_list[0], sentence_len_list[1], sentence_len_list[2]]})
#print(df)
df.to_excel('./result_authorship.xlsx', sheet_name='results', index=False)
