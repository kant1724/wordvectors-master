# coding: utf-8
import argparse
import codecs
import lxml.etree as ET
import os
import regex
from eunjeon import Mecab

lcode = 'ko'
mecab = Mecab()
max_corpus_size = 1000000000
fname = "{}wiki-20190820-pages-articles-multistream.xml".format(lcode)

def clean_text(text):
    # Common
    text = regex.sub("(?s)<ref>.+?</ref>", "", text) # remove reference links
    text = regex.sub("(?s)<[^>]+>", "", text) # remove html tags
    text = regex.sub("&[a-z]+;", "", text) # remove html entities
    text = regex.sub("(?s){{.+?}}", "", text) # remove markup tags
    text = regex.sub("(?s){.+?}", "", text) # remove markup tags
    text = regex.sub("(?s)\[\[([^]]+\|)", "", text) # remove link target strings
    text = regex.sub("(?s)\[\[([^]]+\:.+?]])", "", text) # remove media links
    
    text = regex.sub("[']{5}", "", text) # remove italic+bold symbols
    text = regex.sub("[']{3}", "", text) # remove bold symbols
    text = regex.sub("[']{2}", "", text) # remove italic symbols
    
    text = regex.sub(u"[^ \r\n\p{Hangul}.?!]", " ", text) # Replace unacceptable characters with a space.

    # Common
    text = regex.sub("[ ]{2,}", " ", text) # Squeeze spaces.
    return text

def sentence_segment(text):
    sents = regex.split("([.?!])?[\n]+|[.?!] ", text)
    return sents
        
def word_segment(sent):
    words = [word for word, _ in mecab.pos(sent)]

    return words

def build_corpus():
    global lcode, max_corpus_size, fname
    with codecs.open("data/{}.txt".format(lcode), 'w', 'utf-8') as fout:
        i = 1
        ns = "{http://www.mediawiki.org/xml/export-0.10/}" # namespace
        for _, elem in ET.iterparse("data/{}".format(fname), tag=ns+"text"):
            running_text = elem.text
            try:
                running_text = clean_text(running_text)
                sents = sentence_segment(running_text)
                for sent in sents:
                    if sent is not None:
                        words = word_segment(sent)
                        if len(words) > 10:
                            if lcode in ['ja']:
                                fout.write(" ".join(words).decode('utf8') + "\n")
                            else:
                                fout.write(" ".join(words) + "\n")
                                
            except:
                continue # it's okay as we have a pretty big corpus!
            elem.clear() # We need to save memory!
            if i % 1000 == 0: 
                print(i)
                fsize = os.path.getsize("data/{}.txt".format(lcode))
                if fsize > max_corpus_size:
                    break
            i += 1

if __name__ == "__main__":
    build_corpus()
    
    print('Done')
