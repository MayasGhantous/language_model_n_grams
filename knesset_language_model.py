import pandas as pd 

df = pd.read_csv('knesset_corpus.csv')

token_data_frame = pd.DataFrame() 
frequncy_dictionary = {}

#count 
for row_number,row in enumerate(df.itertuples()):
    all_words = str(row[5]).split(" ")
    for word in all_words:
        if word not in frequncy_dictionary.keys():
            frequncy_dictionary[word]=1
        else:
            frequncy_dictionary[word]+=1
corpus_size = 0
for word in frequncy_dictionary.keys():
    corpus_size+=frequncy_dictionary[word]

frequncy_dictionary_2_words = {}
for row_number,row in enumerate(df.itertuples()):
    all_words = str(row[5]).split(" ")
    first_word = None
    for word in all_words:
        if first_word == None: 
            first_word = word 
            continue
        if first_word not in frequncy_dictionary_2_words.keys():
            frequncy_dictionary_2_words[first_word] ={}
        if word not in frequncy_dictionary_2_words[first_word].keys():
            frequncy_dictionary_2_words[first_word][word] = 0
        frequncy_dictionary_2_words[first_word][word] +=1
        first_word = word


frequncy_dictionary_3_words = {}
for row_number,row in enumerate(df.itertuples()):
    all_words = str(row[5]).split(" ")
    first_word = None
    second_word = None
    for word in all_words:
        if first_word == None:
            first_word = word
            continue
        if second_word == None:
            second_word = word
            continue
        if first_word not in frequncy_dictionary_3_words.keys():
            frequncy_dictionary_3_words[first_word] ={}
        if second_word not in frequncy_dictionary_3_words[first_word].keys():
             frequncy_dictionary_3_words[first_word][second_word] ={}
        if word not in frequncy_dictionary_3_words[first_word][second_word].keys():
            frequncy_dictionary_3_words[first_word][second_word][word] = 0
        frequncy_dictionary_3_words[first_word][second_word][word] +=1
        first_word = second_word
        second_word = word
        


print('finish')




def calculate_prob_of_sentence(sentence,smoothing):
    if 'Laplace' == smoothing:
        V = len(frequncy_dictionary.keys())# number of diffrent words
        sentence_token = sentence.split(' ')
        sentence_prop  = 0 
        for token_number, token in enumerate(sentence_token):
            if token in frequncy_dictionary.keys():
                sentence_prop*=(frequncy_dictionary[token]+1)/(corpus_size+V)



