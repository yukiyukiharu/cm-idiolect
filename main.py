import nltk
import string
import numpy as np
import os
import pandas as pd


def find_lex_variety(token):
    #лексическое разнообразие
    text = nltk.Text(token)
    lexical_diversity = (len(set(text)) / len(text)) * 100
    return lexical_diversity


def find_average_word_len(token):
    #средняя длина слова
    words = set(token)
    word_chars = [len(word) for word in words]
    mean_word_len = sum(word_chars) / float(len(word_chars))
    return mean_word_len


def find_average_sentence_len(words):
    #средняя длина предложения
    sentences = nltk.sent_tokenize(words)
    sentence_word_length = [len(sent.split()) for sent in sentences]
    mean_sentence_len = np.mean(sentence_word_length)
    return mean_sentence_len


def find_average(catalogue):
    numerator = 0
    for element in catalogue:
        numerator += element
    result = numerator / len(catalogue)
    return result


def calculate_punctuation_percentage(text):
    if text.strip() == "":
        return 0
    count = sum([1 if char in string.punctuation else 0 for char in text])
    spaces = text.count(" ")
    total_chars = len(text) - spaces

    return round(count / total_chars, 3) * 100


if __name__ == '__main__':
    direct = ["./VanillaChip101", "./imadetheline"]
    nltk.download('punkt')
    author_res = []
    for el in direct:
        lex_var_list = []
        word_len_list = []
        sentence_len_list = []
        res_punct = []
        token_list = []
        direction = os.path.abspath(el)
        direction_1 = os.listdir(el)
        counter = 0
        for element in direction_1:
            element = direction + "\\" + element
            f = open(element, encoding='utf-8')
            s = f.read().split()
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
            token_list.extend(tokens_)

            punctuation = calculate_punctuation_percentage(s)
            res_punct.append(punctuation)
            
            lex_variety = find_lex_variety(tokens_)
            lex_var_list.append(lex_variety)

            word_len = find_average_word_len(tokens_)
            word_len_list.append(word_len)

            sentence_len = find_average_sentence_len(s)
            sentence_len_list.append(sentence_len)

        #print(lex_var_list)
        res_lex_var = find_average(lex_var_list)
        #print(res_lex_var)
        author_res.append(res_lex_var)

        #print(word_len_list)
        res_word_len = find_average(word_len_list)
        #print(res_word_len)
        author_res.append(res_word_len)

        #print(sentence_len_list)
        res_sentence_len = find_average(sentence_len_list)
        #print(res_sentence_len)
        author_res.append(res_sentence_len)
        
        res_punctuation = sum(res_punct) / len(res_punct)
        author_res.append(res_punctuation)

    #print(author_res)

    #print(token_list)

    df = pd.DataFrame({'Author': ['Author1', 'Author2'], 'lex variety': [author_res[0], author_res[4]],
                       'average word len': [author_res[1], author_res[5]],
                       'average sentence len': [author_res[2], author_res[6]],
                       'punctuation percentage': [author_res[3], author_res[7]]})
    #print(df)
    df.to_excel('./result.xlsx', sheet_name='results', index=False)
