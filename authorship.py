import nltk
import string
import pandas as pd
import math
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


#stylometric tests
papers = {'Author1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'Author2': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
          'unknown1': [21], 'unknown2': [22], 'unknown3': [23]}


def read_files_into_string(filenames):
    strings = []
    for filename in filenames:
        with open(f'all_texts/text_{filename}.txt', encoding='utf-8') as f:
            strings.append(f.read())
    return '\n'.join(strings)


text_author = {}
for author, files in papers.items():
    text_author[author] = read_files_into_string(files)

#first stylometric test (Mendenhall’s Characteristic Curves of Composition)
authors = ('Author1', 'Author2', 'unknown1', 'unknown2', 'unknown3')

text_author_tokens = {}
text_author_length_distributions = {}
for author in authors:
    tokens = nltk.word_tokenize(text_author[author])
    # Filter out punctuation
    text_author_tokens[author] = ([token for token in tokens
                                   if any(c.isalpha() for c in token)])
    # Get a distribution of token lengths
    token_lengths = [len(token) for token in text_author_tokens[author]]
    text_author_length_distributions[author] = nltk.FreqDist(token_lengths)
    text_author_length_distributions[author].plot(15, title=author)


#second stylometric test (Kilgariff’s Chi-Squared Method)
# authors we are analyzing
authors = ('Author1', 'Author2')
for author in authors:
    text_author_tokens[author] = ([token.lower() for token in text_author_tokens[author]])
#text of unknown author wich we will check (after will also check for 'unknown1' and 'unknown3')
text_author_tokens['unknown2'] = ([token.lower() for token in text_author_tokens['unknown2']])

# Calculate chisquared for each of the two candidate authors
for author in authors:
    # First, build a joint corpus and identify the 500 most frequent words in it
    joint_corpus = (text_author_tokens[author] +
                    text_author_tokens['unknown2'])
    joint_freq_dist = nltk.FreqDist(joint_corpus)
    most_common = list(joint_freq_dist.most_common(500))

    author_share = (len(text_author_tokens[author])
                    / len(joint_corpus))

    chisquared = 0
    for word, joint_count in most_common:

        # How often do we really see this common word?
        author_count = text_author_tokens[author].count(word)
        disputed_count = text_author_tokens['unknown2'].count(word)

        # How often should we see it?
        expected_author_count = joint_count * author_share
        expected_disputed_count = joint_count * (1-author_share)

        # Add the word's contribution to the chi-squared statistic
        chisquared += ((author_count-expected_author_count) *
                       (author_count-expected_author_count) /
                       expected_author_count)

        chisquared += ((disputed_count-expected_disputed_count) *
                       (disputed_count-expected_disputed_count)
                       / expected_disputed_count)
    #for author 'unknown2'
    print("The Chi-squared statistic for candidate", author, "is", chisquared)


#third stylometric test (John Burrows’ Delta Method (Advanced))
# check 'unknown2'
authors = ('Author1', 'Author2', 'unknown1', 'unknown3')

# Convert papers to lowercase to count all tokens of the same word together
# regardless of case
for author in authors:
    text_author_tokens[author] = ([tok.lower() for tok in text_author_tokens[author]])
# Combine into a single corpus
whole_corpus = []
for author in authors:
    whole_corpus += text_author_tokens[author]
# frequency distribution
whole_corpus_freq_dist = list(nltk.FreqDist(whole_corpus).most_common(30))
#print(whole_corpus_freq_dist[:10])

# The main data structure
features = [word for word, freq in whole_corpus_freq_dist]
feature_freqs = {}

for author in authors:
    # A dictionary for each candidate's features
    feature_freqs[author] = {}
    # A helper value containing the number of tokens in the author's subcorpus
    overall = len(text_author_tokens[author])
    # Calculate each feature's presence in the subcorpus
    for feature in features:
        presence = text_author_tokens[author].count(feature)
        feature_freqs[author][feature] = presence / overall


# The data structure into which we will be storing the "corpus standard" statistics
corpus_features = {}

for feature in features:
    # Create a sub-dictionary that will contain the feature's mean
    # and standard deviation
    corpus_features[feature] = {}
    # Calculate the mean of the frequencies expressed in the subcorpora
    feature_average = 0
    for author in authors:
        feature_average += feature_freqs[author][feature]
    feature_average /= len(authors)
    corpus_features[feature]["Mean"] = feature_average
    # Calculate the standard deviation using the basic formula for a sample
    feature_stdev = 0
    for author in authors:
        diff = feature_freqs[author][feature] - corpus_features[feature]["Mean"]
        feature_stdev += diff*diff
    feature_stdev /= (len(authors) - 1)
    feature_stdev = math.sqrt(feature_stdev)
    corpus_features[feature]["StdDev"] = feature_stdev


feature_zscores = {}
for author in authors:
    feature_zscores[author] = {}
    for feature in features:
        # Z-score = (value - mean) / stddev
        feature_val = feature_freqs[author][feature]
        feature_mean = corpus_features[feature]["Mean"]
        feature_stdev = corpus_features[feature]["StdDev"]
        feature_zscores[author][feature] = ((feature_val-feature_mean) /
                                            feature_stdev)

# Tokenize the test case
testcase_tokens = nltk.word_tokenize(text_author['unknown2'])

# Filter out punctuation and lowercase the tokens
testcase_tokens = [token.lower() for token in testcase_tokens
                   if any(c.isalpha() for c in token)]
# Calculate the test case's features
overall = len(testcase_tokens)
testcase_freqs = {}
for feature in features:
    presence = testcase_tokens.count(feature)
    testcase_freqs[feature] = presence / overall
# Calculate the test case's feature z-scores
testcase_zscores = {}
for feature in features:
    feature_val = testcase_freqs[feature]
    feature_mean = corpus_features[feature]["Mean"]
    feature_stdev = corpus_features[feature]["StdDev"]
    testcase_zscores[feature] = (feature_val - feature_mean) / feature_stdev
    #print("Test case z-score for feature", feature, "is", testcase_zscores[feature])

for author in authors:
    delta = 0
    for feature in features:
        delta += math.fabs((testcase_zscores[feature] -
                            feature_zscores[author][feature]))
    delta /= len(features)
    print("Delta score for candidate", author, "is", delta)
