import pandas as pd 
import numpy as np
import heapq




class corpus:
    def __init__(self,type):
        self.type = type
        #input the type of the protocol
        # out put frequncy_dictionary_for 1 word,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size
        df = pd.read_csv('knesset_corpus.csv')

        frequncy_dictionary = {}
        df = df.loc[df['protocol_type'] == type]
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
        self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size=frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size
        

        
    def calculate_prob_of_sentence(self,sentence,smoothing):
        frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size = self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size
        #notes
        '''sentence_prop calculation sentece will chane
        still need the progran the second type of smoothing'''
        lambda1 = 0.2
        lambda2 = 0.3
        lambda3 = 0.5

        if 'Laplace' == smoothing:
            V = len(frequncy_dictionary.keys())# number of diffrent words
            sentence_token = sentence.split(' ')
            sentence_prop  = 1
            for token_number, token in enumerate(sentence_token):
                if token_number ==0 :
                    if token not in frequncy_dictionary.keys():
                        frequncy_dictionary[token] = 0
                        frequncy_dictionary_2_words[token]={}
                        frequncy_dictionary_3_words[token]={}
                    sentence_prop = (frequncy_dictionary[token]+1)/(corpus_size+V)
                elif token_number == 1:
                    if token not in frequncy_dictionary_2_words[sentence_token[0]].keys():
                        frequncy_dictionary_2_words[sentence_token[0]][token] =0
                        frequncy_dictionary_3_words[sentence_token[0]][token] ={}
                    sentence_prop += np.log((frequncy_dictionary_2_words[sentence_token[0]][token]+1)/(frequncy_dictionary_2_words[sentence_token[0]]+V))#may change
                else:
                    first = sentence_token[token_number-2]
                    second = sentence_token[token_number-1]
                    third = token
                    if  first not in frequncy_dictionary.keys():
                        frequncy_dictionary[first] = 0
                        frequncy_dictionary_2_words[first]={}
                        frequncy_dictionary_3_words[first]={}
                    if second not in frequncy_dictionary_2_words[first].keys():
                        frequncy_dictionary_2_words[first][second] = 0
                        frequncy_dictionary_3_words[first][second] = {}
                    if third not in frequncy_dictionary_3_words[first][second].keys():
                        frequncy_dictionary_3_words[first][second][third] = 0
                    sentence_prop += np.log((frequncy_dictionary_3_words[first][second][third]+1)/(frequncy_dictionary_2_words[first][second]+V))#may change
            return sentence_prop
        else:
            V = len(frequncy_dictionary.keys())# number of diffrent words
            sentence_token = sentence.split(' ')
            sentence_prop  = 1
            for token_number, token in enumerate(sentence_token):
                if token_number ==0 :
                    if token not in frequncy_dictionary.keys():
                        frequncy_dictionary[token] = 0
                        frequncy_dictionary_2_words[token]={}
                        frequncy_dictionary_3_words[token]={}
                    sentence_prop = np.log(lambda1*(frequncy_dictionary[token]+1)/(corpus_size+V))
                elif token_number == 1:
                    if token not in frequncy_dictionary.keys():
                        frequncy_dictionary[token] = 0
                        frequncy_dictionary_2_words[token]={}
                        frequncy_dictionary_3_words[token]={}
                    if token not in frequncy_dictionary_2_words[sentence_token[0]].keys():
                        frequncy_dictionary_2_words[sentence_token[0]][token] =0
                        frequncy_dictionary_3_words[sentence_token[0]][token] ={}
                    sentence_prop += np.log((lambda2*(frequncy_dictionary_2_words[sentence_token[0]][token]+1)/(frequncy_dictionary_2_words[sentence_token[0]]+V))+lambda1*(frequncy_dictionary[token]+1)/(corpus_size+V))#may change
                else:
                    first = sentence_token[token_number-2]
                    second = sentence_token[token_number-1]
                    third = token
                    if third not in frequncy_dictionary.keys():
                        frequncy_dictionary[third] = 0
                        frequncy_dictionary_2_words[third]={}
                        frequncy_dictionary_3_words[third]={}
                    if second not in frequncy_dictionary.keys():
                        frequncy_dictionary[second] = 0
                        frequncy_dictionary_2_words[second]={}
                        frequncy_dictionary_3_words[second]={}
                    if third not in frequncy_dictionary_2_words[second].keys():
                        frequncy_dictionary_2_words[second][third] =0
                        frequncy_dictionary_3_words[second][third] ={}
                    if  first not in frequncy_dictionary.keys():
                        frequncy_dictionary[first] = 0
                        frequncy_dictionary_2_words[first]={}
                        frequncy_dictionary_3_words[first]={}
                    if second not in frequncy_dictionary_2_words[first].keys():
                        frequncy_dictionary_2_words[first][second] = 0
                        frequncy_dictionary_3_words[first][second] = {}
                    if third not in frequncy_dictionary_3_words[first][second].keys():
                        frequncy_dictionary_3_words[first][second][third] = 0
                    sentence_prop = np.log((lambda3*(frequncy_dictionary_3_words[first][second][third])/(frequncy_dictionary_2_words[first][second]))+(lambda2*(frequncy_dictionary_2_words[second][third])/(frequncy_dictionary_2_words[second]))+lambda1*(frequncy_dictionary[third]+1)/(corpus_size+V))#may change
            return sentence_prop
        


    def get_next_token(self,sentence):
        frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size = self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size

        max_prop = -np.infty
        max_token = ''
        for word in self.frequncy_dictionary.keys():
            sentece_porp = self.calculate_prob_of_sentence(sentence=sentence + ' '+ word,smoothing='Linear')
            if sentece_porp > max_prop: 
                max_prop = sentece_porp
                max_token = word
        return max_token



    def  get_k_n_collocations(self,k,n):
        frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size = self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size
        collocations_dictionary = {}
        df = pd.read_csv('knesset_corpus.csv')
        df = df.loc[df['protocol_type'] == self.type]
        for row_number in range(len (df)):
            sentence_tokens = df.iloc[row_number]['sentence_text'].split(' ')
            sentece_length = len (sentence_tokens)
            first_collocation = sentence_tokens[0:n]
            current_collocation_text = ''
            for word in first_collocation:
                current_collocation_text+=word +' '
            current_collocation_text = current_collocation_text.strip()
            for i in range(sentece_length-n+1):
                if current_collocation_text not in collocations_dictionary.keys():
                    collocations_dictionary[current_collocation_text] = 0
                collocations_dictionary [current_collocation_text]+=1
                current_collocation_text = current_collocation_text[current_collocation_text.find(' ')+1:]
                if i+n == sentece_length:
                    continue
                current_collocation_text += " " +sentence_tokens[i+n]

        return heapq.nlargest(k, collocations_dictionary, key=collocations_dictionary.get)



if __name__ == '__main__':
    print('start')