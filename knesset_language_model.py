import pandas as pd 
import numpy as np
import heapq




class corpus:
    def __init__(self,type):
        self.type = type
        # read the data
        df = pd.read_csv('example_knesset_corpus.csv')

        frequncy_dictionary = {} #frequncy_dictionary[word] = how many did the token appear
        df = df.loc[df['protocol_type'] == type]
        for row_number,row in enumerate(df.itertuples()):

            all_words = str(row[5]).split(" ")
            for word in all_words:
                if word not in frequncy_dictionary.keys():
                    frequncy_dictionary[word]=1# if I dont have an intry make one
                else:
                    frequncy_dictionary[word]+=1
        
        #getting the corpus size
        corpus_size = 0
        for word in frequncy_dictionary.keys():
            corpus_size+=frequncy_dictionary[word]



        # frequncy_dictionary_2_words[word1][word2] is how many did word 1 appear before word 2
        frequncy_dictionary_2_words = {}
        for row_number,row in enumerate(df.itertuples()):
            all_words = str(row[5]).split(" ")
            first_word = None
            for word in all_words:
                if first_word == None: #if it is the fist word in the sentnce then dont dont do any thing 
                    first_word = word 
                    continue

                if first_word not in frequncy_dictionary_2_words.keys():#if the first word does not have an entry then make one
                    frequncy_dictionary_2_words[first_word] ={}

                if word not in frequncy_dictionary_2_words[first_word].keys():# if we dont have an entry to the seond word then make one
                    frequncy_dictionary_2_words[first_word][word] = 0
                
                frequncy_dictionary_2_words[first_word][word] +=1

                first_word = word#change the first word in the bigram


        frequncy_dictionary_3_words = {}
        for row_number,row in enumerate(df.itertuples()):
            all_words = str(row[5]).split(" ")
            first_word = None
            second_word = None

            for word in all_words:

                if first_word == None:# if we are in the first word of the sentnce then we do not add anything
                    first_word = word
                    continue

                if second_word == None:# if we are at the second then dont save anythig
                    second_word = word
                    continue
                #starting from the third we begin to increce the counter
                #make the entry if we dont have one yet and then incearce the counter
                if first_word not in frequncy_dictionary_3_words.keys(): 
                    frequncy_dictionary_3_words[first_word] ={}
                if second_word not in frequncy_dictionary_3_words[first_word].keys():
                    frequncy_dictionary_3_words[first_word][second_word] ={}
                if word not in frequncy_dictionary_3_words[first_word][second_word].keys():
                    frequncy_dictionary_3_words[first_word][second_word][word] = 0
                frequncy_dictionary_3_words[first_word][second_word][word] +=1
                
                #for the next iteration change the word places in the current 3 words
                first_word = second_word
                second_word = word
        # save our computation
        self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size=frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size
        

        
    def calculate_prob_of_sentence(self,sentence,smoothing = 'Linear'):
        smoothing = 'Laplace'
        frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size = self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size
        #notes
        '''sentence_prop calculation sentece will chane
        still need the progran the second type of smoothing'''
        lambda1 = 0.2
        lambda2 = 0.3
        lambda3 = 0.5
        sentence_token_temp = sentence.split(' ')
        sentence_token = []
        for token in sentence_token_temp:
            if token != '':
                sentence_token.append(token)

        if 'Laplace' == smoothing:
            V = len(frequncy_dictionary.keys())# number of diffrent words
            sentence_prop  = 1
            for token_number, token in enumerate(sentence_token):
                if token_number ==0 : #if we are at the fist word in the sentence
                    
                    #claculate the prop of the word
                    sentence_prop = np.log((frequncy_dictionary.get(token,0)+1)/(corpus_size+V))
                elif token_number == 1:# if we are at the second wrod of the sentnce
                    # then calcualte 
                    sentence_prop += np.log((frequncy_dictionary_2_words.get(sentence_token[0],{}).get(token,0)+1)/(frequncy_dictionary.get(sentence_token[0],0)+V))#may change
                else:
                    #calcualte
                    first = sentence_token[token_number-2]
                    second = sentence_token[token_number-1]
                    third = token
                    sentence_prop += np.log((frequncy_dictionary_3_words.get(first,{}).get(second,{}).get(third,0)+1)/(frequncy_dictionary_2_words.get(first,{}).get(second,0)+V))#may change
            return sentence_prop
        else:
            V = len(frequncy_dictionary.keys())# number of diffrent words
            sentence_prop  = 1
            for token_number, token in enumerate(sentence_token):
                if token_number ==0 :# if we are at the first word
                    #caluclate
                    sentence_prop = np.log(lambda1*(frequncy_dictionary.get(token,0)+1)/(corpus_size+V))
                elif token_number == 1:# if we are at the second word
                    #caluclate
                    sentence_prop += np.log((lambda2*(frequncy_dictionary_2_words.get(sentence_token[0],{}).get(token,0)+1)/(frequncy_dictionary.get(sentence_token[0],0)+V))+lambda1*(frequncy_dictionary.get(token,0)+1)/(corpus_size+V))#may change
                else:
                    first = sentence_token[token_number-2]
                    second = sentence_token[token_number-1]
                    third = token
                    sentence_prop = np.log((lambda3*(frequncy_dictionary_3_words.get(first,{}).get(second,{}).get(third,0)+1)/(frequncy_dictionary_2_words.get(first,{}).get(second,0)+V))+(lambda2*(frequncy_dictionary_2_words.get(second,{}).get(third,0)+1)/(frequncy_dictionary.get(second,0)+V))+lambda1*(frequncy_dictionary.get(third,0)+1)/(corpus_size+V))#may change
            return sentence_prop
        


    def get_next_token(self,sentence):
        frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size = self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size

        max_prop = -np.infty
        max_token = ''
        # for every possiable token make calcualte the prop of he sentce and return the token that have the highes prop
        for word in self.frequncy_dictionary.keys():
            if word == ' ' or word == '':
                continue
            sentece_porp = self.calculate_prob_of_sentence(sentence=sentence + ' '+ word,smoothing='Linear')
            if sentece_porp > max_prop: 
                max_prop = sentece_porp
                max_token = word
        return max_token



    def  get_k_n_collocations(self,k,n):
        frequncy_dictionary,frequncy_dictionary_2_words,frequncy_dictionary_3_words,corpus_size = self.frequncy_dictionary,self.frequncy_dictionary_2_words,self.frequncy_dictionary_3_words,self.corpus_size
        collocations_dictionary = {}
        df = pd.read_csv('example_knesset_corpus.csv')
        df = df.loc[df['protocol_type'] == self.type]
        for row_number in range(len (df)):
            sentence_tokens = df.iloc[row_number]['sentence_text'].strip().split(' ')
            sentece_length = len (sentence_tokens)
            if sentece_length<n:
                continue
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
    
def Q2_text (plenary_corpus,committee_corpus):
    text = 'Two-gram collocations:\n'
    text+= 'Committee corpus:\n'
    results = committee_corpus.get_k_n_collocations(10,2)
    for col in results:
        text+=col +'\n'
    text+='\n'
    text += 'Plenary corpus:\n'
    results = plenary_corpus.get_k_n_collocations(10,2)
    for col in results:
        text+=col +'\n'
    text+='\n'

    text += 'Three-gramcollocations:\n'
    text+= 'Committee corpus:\n'
    results = committee_corpus.get_k_n_collocations(10,3)
    for col in results:
        text+=col +'\n'
    text+='\n'
    text += 'Plenary corpus:\n'
    results = plenary_corpus.get_k_n_collocations(10,3)
    for col in results:
        text+=col +'\n'
    text+='\n'

    text += 'four-gram collocations:\n'
    text+= 'Committee corpus:\n'
    results = committee_corpus.get_k_n_collocations(10,4)
    for col in results:
        text+=col +'\n'
    text+='\n'
    text += 'Plenary corpus:\n'
    results = plenary_corpus.get_k_n_collocations(10,4)
    for col in results:
        text+=col +'\n'
    text+='\n'
    with open('knesset_collocations.txt','w',encoding='utf-8') as file:
        file.write(text)

    

def Q3_text (plenary_corpus,committee_corpus):
    with open('masked_sentences.txt', 'r',encoding='utf-8') as file:
    # Read the contents of the file
        file_contents = file.read()
        sentences = file_contents.split('\n')
        text = ''
        for sentence in sentences:
            text+='Original sentence: '+sentence+ '\n'

            committee_sentence =''
            committee_tokens=[]
            committee_prop = 0

            plenary_sentence =""
            plenary_tokens=[]
            plenary_prop = 0 

            all_words = sentence.split(' ')
            for word in all_words:
                if word != '[*]':
                    committee_sentence+= word+" "
                    plenary_sentence +=word + ' '
                else:
                    token_plenary = plenary_corpus.get_next_token(plenary_sentence)
                    token_committee = committee_corpus.get_next_token(committee_sentence)

                    committee_sentence += token_committee+' '
                    committee_tokens.append(token_committee)

                    plenary_sentence += token_plenary+' '
                    plenary_tokens.append(token_plenary)
            committee_sentence = committee_sentence.strip()
            plenary_sentence = plenary_sentence.strip()
            text+='Committee sentence:'+committee_sentence+'\n'
            text += 'Committee tokens: ' +str(committee_tokens) +'\n'
            committee_prop = committee_corpus.calculate_prob_of_sentence(committee_sentence)
            text+= 'Probability of committee sentence in committee corpus: '+str(committee_prop)+'\n'
            text += 'Probability of committee sentence in plenary corpus: '+str(plenary_corpus.calculate_prob_of_sentence(committee_sentence))+'\n'

            text+= 'Plenary sentence: '+plenary_sentence +'\n'
            text+= 'Plenary tokens: '+str(plenary_tokens) +'\n'
            plenary_prop = plenary_corpus.calculate_prob_of_sentence(plenary_sentence)
            text+= 'Probability of plenary sentence in plenary corpus: '+str(plenary_prop) +'\n'
            text+='Probability of plenary sentence in committee corpus: '+str(committee_corpus.calculate_prob_of_sentence(plenary_sentence))+'\n'
            text+= 'This sentence is more likely to appear in corpus: '

            if plenary_prop>committee_prop:
                text+='plenary' +'\n\n'
            else:
                text+='committee' +'\n\n'
    with open('sentences_results.txt','w',encoding='utf-8') as file:
        file.write(text)


            


if __name__ == '__main__':
    #we work on plenary
    plenary_corpus = corpus('plenary')
    committee_corpus = corpus('committee')
    #Q2_text(plenary_corpus=plenary_corpus,committee_corpus=committee_corpus)
    Q3_text(plenary_corpus=plenary_corpus,committee_corpus=committee_corpus)