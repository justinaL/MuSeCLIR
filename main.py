import os, argparse
from src import get_nouns, sense_dict, doc_match_unicode, translate_query
from src.utils import *


parser = argparse.ArgumentParser(description='MuSeCLIR')

parser.add_argument("--target_lang", type=str, default='ja', help="Target language")

params = parser.parse_args()

tlang = params.target_lang
####################################################################################################

# create a target language folder
if not os.path.exists(tlang):
    os.mkdir(tlang)

# collect wiki ambiguous nouns
get_nouns.main(tlang=tlang)

# collect word sense dictionaries
sense_dict.main(tlang=tlang)

# collect eng sentence queries
eng_sense_dict = unpickle('{}/clean_eng_sense_dict.pickle'.format(tlang))
sentences = get_sentences(eng_sense_dict)
save_pickle('{}/eng_sentences.pickle'.format(tlang), sentences)

yy_sense_dict = unpickle('{}/clean_{}_sense_dict.pickle'.format(tlang,tlang))
sentences = unpickle('{}/eng_sentences.pickle'.format(tlang))
# ground-truth table, document collection
merged_df, document_df = combine(yy_sense_dict, sentences, tlang)

# merged_df.to_csv('{}/merged_df.csv'.format(tlang), index=None)
# document_df.to_csv('{}/document_df.csv'.format(tlang), index=None)

# match unicode for single language documents
document_df = doc_match_unicode.main(document_df, tlang)
document_df.to_csv('{}/document_df.csv'.format(tlang), index=None)

# translate queries
translated_nouns = translate_query.traslate(merged_df['noun'], tlang)
save_pickle('{}/translated_noun.pickle'.format(tlang), translated_nouns)
for i,r in merged_df.iterrows():
    merged_df.at[i, 'translated_noun'] = trans_clean_up(translated_nouns[i], tlang)

translated_sentences = translate_query.traslate(merged_df['sentence'], tlang)
save_pickle('{}/translated_sentence.pickle'.format(tlang), translated_sentences)
for i,r in merged_df.iterrows():
    merged_df.at[i, 'translated_sentence'] = trans_clean_up(translated_sentences[i], tlang)

merged_df.to_csv('{}/merged_df.csv'.format(tlang), index=None)