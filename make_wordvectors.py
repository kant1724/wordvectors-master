# coding: utf-8
#!/usr/bin/python2
import nltk
import os
import codecs
import argparse
import numpy as np

# arguments setting 
def get_min_count(sents):
    '''
    Args:
      sents: A list of lists. E.g., [["I", "am", "a", "boy", "."], ["You", "are", "a", "girl", "."]]
     
    Returns:
      min_count: A uint. Should be set as the parameter value of word2vec `min_count`.   
    '''
    vocab_size = 10000
    from itertools import chain
     
    fdist = nltk.FreqDist(chain.from_iterable(sents))
    min_count = fdist.most_common(vocab_size)[-1][1] # the count of the the top-kth word
    
    return min_count

def make_wordvectors():
    global lcode
    import gensim
     
    print("Making sentences as list...")
    sents = []
    with codecs.open('data/{}.txt'.format('ko'), 'r', 'utf-8') as fin:
        while 1:
            line = fin.readline()
            if not line: break
             
            words = line.split()
            sents.append(words)

    print("fast text...")
    model = gensim.models.FastText(sents, size=300, min_count=54, window=3)
    model.save('data/ko.bin')

    with codecs.open('data/ko.tsv', 'w', 'utf-8') as fout:
        for i, word in enumerate(model.index2word):
            fout.write(u"{}\t{}\t{}\n".format(str(i), word.encode('utf8').decode('utf8'),
                                              np.array_str(model[word])
                                              ))


if __name__ == "__main__":
    make_wordvectors()
    
    print("Done")
