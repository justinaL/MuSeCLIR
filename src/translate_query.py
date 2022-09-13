import re

def traslate(sentences, tlang):
    f = open('../../data/crosslingual/dictionaries/en-{}.txt'.format(tlang))
    en, yy = [],[]

    for line in f.readlines():
        en.append(line.split()[0])
        yy.append(line.split()[1])

    translated_sentences = []
    for sentence in sentences:
        trans_sent = []
        sent = re.sub(r'[^\w\s]', ' ',sentence)
        if len(sent.strip()): # check if it originally contains punctuations only
            for token in sent.split():
                if token.lower() in en:
                    idx = en.index(token.lower())
                    trans_sent.append(yy[idx])
                else:
                    trans_sent.append('<'+token+'>')

            # for non space separated languages (zh, ja)
            if tlang in ['ja','zh']:
                translated_sentences.append(''.join([t.strip() for t in trans_sent]))
            else:
                translated_sentences.append(' '.join(trans_sent))

        else:
            translated_sentences.append('<'+sentence+'>')
        print(f'\r>finished %d/%d sentences' % (len(translated_sentences),len(sentences)), flush=True, end='')

    return translated_sentences
