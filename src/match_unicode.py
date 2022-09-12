import re

def find_unicode(summary, tlang):
    l = []
    for t in summary.split():
        if tlang == 'fr':
            f = re.findall(r'[\u0041-\u007Açéâêîôûàèìòùëïü\']+', t) # french
        elif tlang == 'de':
            f = re.findall(r'[a-zA-ZÄäÖöÜüẞß]+', t) # german
        elif tlang == 'it':
            f = re.findall(r'[\u0041-\u0049\u004C-\u0056\u0061-\u0069\u006C-\u0076àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]+',t) # italian

        elif tlang == 'zh':
            f = re.findall(r'[\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC]+',t) # chinese
        elif tlang == 'ja':
            f = re.findall(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]+', t) # japanese

        if tlang not in ['ja','zh']:
            if len(f) > 0 and f[0] == t:
                l.append(f[0])
        else:
            # for non space separated languages
            l.append(f)

    if not tlang in ['ja','zh']:
        return ' '.join(l)
    else:
        # for non space separated languages
        l = [elem for sublist in l for elem in sublist]
        return ''.join(l)

def main(df, tlang):
    c = 0

    for i,r in df.iterrows():
        doc_only = find_unicode(r['summary'], tlang)

        if len(doc_only):
            df.at[i, 'tlang_only'] = doc_only
        else:
            # random.seed(i)
            # it_document_df.at[i, 'ja_only'] = random.choices(list(it_spacy.Defaults.stop_words), k=1)[0]
            c+=1
        print(f'\r>finished %d/%d doc' % (i,len(df)), flush=True, end='')

    print(c)

    return df
