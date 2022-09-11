import copy
import re
import opencc
import spacy
from utils import *
import wikipediaapi
converter = opencc.OpenCC('s2t.json') # simplified to traditional Chinese characters
en_spacy = spacy.load('en_core_web_sm')
wiki_wiki = wikipediaapi.Wikipedia('en')


def check_pos(title, word):
    if title.lower().find(word) == -1:
        return []
    else:
        part_of_speech = []
        for t in en_spacy(title): # turn spacy to case sensitive to catch proper nouns
            if t.text.lower().find(word) != -1:
                part_of_speech.append(t.pos_)

        return part_of_speech


def clean_doc(sense_dict,lang='en'):

    if lang=='zh':
        cleaned = copy.deepcopy(sense_dict)

        for word,dic in sense_dict.items():
            for key,tup in dic.items():
                (title, summary) = tup
                cleaned[word][key] = (converter.convert(title), re.sub('\s+',' ',converter.convert(summary)))

        return cleaned
    else:
        cleaned = copy.deepcopy(sense_dict)

        for word,dic in sense_dict.items():
            for key,tup in dic.items():
                (title, summary) = tup
                cleaned[word][key] = (title,re.sub('\s+',' ',summary))

        return cleaned

def clean_internal(sense_dict, sense_dict_2):
    # list of english "internal" pages to be removed

    dict_copy = copy.deepcopy(sense_dict)
    dict_copy2 = copy.deepcopy(sense_dict_2)

    for word, dic in dict_copy.items():
        for key, (tit, summary) in dic.items():
            # boo = any(p in tit for p in punc)
            # if boo: print('WORD: {}, TITLE: {}'.format(word,tit))
            if re.search('(Wikipedia|Category|Help|WikiProject):', tit):
                print('WORD: {}, TITLE: {}'.format(word,tit))
                try: del sense_dict[word][key]
                except: pass
                try: del sense_dict_2[word][key]
                except: pass

    for word, dic in dict_copy2.items():
        for key, (tit, summary) in dic.items():
            # boo = any(p in tit for p in punc)
            # if boo: print('WORD: {}, TITLE: {}'.format(word,tit))
            if re.search('(Wikipedia|Category|Help|WikiProject):', tit):
                print('WORD: {}, TITLE: {}'.format(word,tit))
                try: del sense_dict[word][key]
                except: pass
                try: del sense_dict_2[word][key]
                except: pass

    return sense_dict, sense_dict_2

def main(tlang):
    dis_nouns = unpickle('{}/dis_nouns.pickle'.format(tlang))
    eng_sense_dict, yy_sense_dict = {}, {}
    # eng_sense_dict = unpickle('{}/eng_sense_dict.pickle'.format(tlang))
    # yy_sense_dict = unpickle('{}/{}_sense_dict.pickle'.format(tlang,tlang))

    for word in dis_nouns:
        english_pages, yy_pages = {}, {}
        pages = list(wiki_wiki.page(str('%s (disambiguation)' % word.lower())).links.items())

        for page in pages:
            # conditions
            find1 = page[0].lower().find(word)  # find target word in page name
            find2 = page[0].find('disambiguation')  # find disambiguation
            find_it = tlang in page[1].langlinks  # find chinese page
            match_tit = page[1].title.lower() == page[0].lower()  # marching title and name
            match_pos = 'NOUN' in check_pos(page[1].title, word)  # check if target is noun in title

            if (find1 != -1) and not (find2 != -1) and match_tit and match_pos and find_it:
                yy_page = page[1].langlinks[tlang]

                if len(yy_page.summary) > 0 and len(page[1].summary) > 0:
                    english_pages[page[0]] = (page[1].title, page[1].summary)
                    yy_pages[page[0]] = (yy_page.title, yy_page.summary)
                else:
                    continue

        if len(english_pages): eng_sense_dict[word] = english_pages
        if len(yy_pages): yy_sense_dict[word] = yy_pages

        print(f'\r>finish getting %d/%d nouns' % (len(eng_sense_dict.keys()),len(dis_nouns)), flush=True, end='')
        if len(eng_sense_dict)%10 == 0:
            save_pickle('{}/eng_sense_dict.pickle'.format(tlang), eng_sense_dict)
            save_pickle('{}/{}_sense_dict.pickle'.format(tlang,tlang), yy_sense_dict)
    print('\n===========finished===========')

    print('last save')
    save_pickle('{}/eng_sense_dict.pickle'.format(tlang), eng_sense_dict)
    save_pickle('{}/{}_sense_dict.pickle'.format(tlang,tlang), yy_sense_dict)

    print('clean single sense')
    eng_sense_dict = {k:v for k,v in eng_sense_dict.items() if len(v)>=2}
    yy_sense_dict = {k:v for k,v in yy_sense_dict.items() if len(v)>=2}

    print('clean docs')
    eng_sense_dict = clean_doc(eng_sense_dict, 'en')
    yy_sense_dict = clean_doc(yy_sense_dict, tlang)

    print('update pickle files')
    save_pickle('{}/eng_sense_dict.pickle'.format(tlang), eng_sense_dict)
    save_pickle('{}/{}_sense_dict.pickle'.format(tlang,tlang), yy_sense_dict)

    print('clean internal pages')
    eng_sense_dict, yy_sense_dict = clean_internal(eng_sense_dict, yy_sense_dict)

    # clean single sense
    eng_sense_dict = {k:v for k,v in eng_sense_dict.items() if len(v)>=2}
    yy_sense_dict = {k:v for k,v in yy_sense_dict.items() if len(v)>=2}

    print('save cleaned pickle')
    save_pickle('{}/clean_eng_sense_dict.pickle'.format(tlang), eng_sense_dict)
    save_pickle('{}/clean_{}_sense_dict.pickle'.format(tlang,tlang), yy_sense_dict)