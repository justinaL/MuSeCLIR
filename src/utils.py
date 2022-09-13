import pickle, copy, re
import pandas as pd
import spacy
en_spacy = spacy.load('en_core_web_sm')

def unpickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def save_pickle(file, var):
    print('SAVING PICKLE, ', file)
    with open(file, 'wb') as f:
        pickle.dump(var, f)

def get_sentences(eng_sense_dict):

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

    return sentences

# create ground-truth tables and the document collection
def combine(yy_sense_dict, sentences, tlang):
    combine_df = {k:v[1] for dic in yy_sense_dict.values() for k,v in dic.items()}
    # v[1] is the summary; v[0] is the page title
    document_df = pd.DataFrame(zip(combine_df.keys(), combine_df.values()), columns=['key','summary'])
    document_df.reset_index(level=0,inplace=True)

    eng_sent_query_df = pd.DataFrame.from_records(((word,key,sent)
                                                   for word,dic in sentences.items()
                                                   for key,sents in dic.items() for sent in sents), columns=['word','key','sentence'])
    eng_sent_query_df.reset_index(level=0,inplace=True)

    # ground-truth table
    merged_df = pd.merge(document_df,eng_sent_query_df,on='key',how='inner')
    merged_df.columns = ['{}_idx'.format(tlang),'pg_title','summary','eng_q_idx','noun','sentence']

    return merged_df, document_df

def trans_clean_up(sentence, tlang):
    c = re.sub('[<>]','',sentence)
    if tlang in ['ja','zh']:
        return ''.join(t.strip() for t in c)
    else:
        return ' '.join(c.split())