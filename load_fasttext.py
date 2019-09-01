# coding: utf-8
#!/usr/bin/python2
import nltk
import os
import codecs
import argparse
import numpy as np

def make_wordvectors():
    import gensim

    model = gensim.models.FastText.load('data/ko.bin')
    with open('data/ko.vec', 'w', encoding='utf8') as f:
        for v in model.wv.vocab:
            s = v + ' '
            arr = model.wv[v]
            a = " ".join([str(round(a, 4)) for a in arr])
            s += a + '\n'
            f.write(s)

if __name__ == "__main__":
    make_wordvectors()
    
    print("Done")
