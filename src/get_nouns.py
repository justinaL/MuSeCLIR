import wikipediaapi
from utils import *

import spacy
en_spacy = spacy.load('en_core_web_sm')

def main(tlang):
    # read MUSE ground-truth bilingual dictionary
    f = open('../../data/crosslingual/dictionaries/en-{}.txt'.format(tlang))
    en, yy = [],[]

    for line in f.readlines():
        en.append(line.split()[0])
        yy.append(line.split()[1])

    # get tokens with multiple possible translations
    en_set = set(en)
    index = {value : [i for i,v in enumerate(en) if v == value] for value in en_set}
    multi_trans_index = {k:v for k,v in index.items() if len(v) > 1}

    # get nouns with multiple possible translations
    nouns = {}

    for word, indices in multi_trans_index.items():
        if word.startswith('#'):
            word = word[1:]
        d = en_spacy(word)
        if not len(d) == 1:
            print(word)
        if  d[0].pos_ == 'NOUN':
            nouns[word] = indices

    # save multi-translation nouns to pickle
    fname = '{}/multi_trans_nouns.pickle'.format(tlang)
    print('save to ', fname)
    save_pickle(fname, nouns)


    wiki_wiki = wikipediaapi.Wikipedia('en')
    # list of nouns with disambiguation page (chosen based on the order of the translation list)
    dis_nouns = []

    for k in list(nouns.keys())[:10]:
        if wiki_wiki.page(str('%s (disambiguation)'%k.lower())).exists():
            dis_nouns.append(k)

        print(f'\r>finished %d nouns'%len(dis_nouns), flush=True, end='')

    print('\n===========finished===========')

    # save wiki ambiguous nouns to pickle
    fname = '{}/dis_nouns.pickle'.format(tlang)
    save_pickle(fname, dis_nouns)