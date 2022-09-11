import copy
from utils import *

import spacy
en_spacy = spacy.load('en_core_web_sm')


def main(tlang):

    eng_sense_dict = unpickle('{}/clean_eng_sense_dict.pickle'.format(tlang))

    sentences = copy.deepcopy(eng_sense_dict) # modify the copy
    i=1
    # per summary, get sentences with the appearence of 'word'
    for word,dic in eng_sense_dict.items():

        for key,tup in dic.items():
            sentence = []
            (title,summary) = tup

            for sent in en_spacy(summary).sents:
                if word.lower() in sent.text.lower():
                    sentence.append(sent.text)

            # if len(sentence):
            sentences[word][key] = sentence
            # else: del sentences[word][key]

        print(f'\r>finish getting %d words'%i, flush=True, end='')
        i+=1

    # sentences = {k:v for k,v in sentences.items() if len(v)>=1}

    print('saving sentences')
    save_pickle('{}/eng_sentences.pickle'.format(tlang), sentences)