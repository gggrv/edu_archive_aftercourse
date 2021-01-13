# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script advanced_nlp_with_spacy.

Contains the results of reading https://course.spacy.io/
and trying it out on English and Russian languages.
"""

# embedded in python
# pip install
import spacy
from spacy import displacy
from spacy.lang.en import English
from spacy.lang.ru import Russian
from spacy.matcher import Matcher
import stanza
import spacy_stanza
# same folder

TXT_RU = r'russian_test.txt'
TXT_EN = r'english_text.txt'
    
def readf( path ):
    with open( path, 'r', encoding='utf-8' ) as f:
        return f.read()
    
def savef( path, text ):
    with open( path, 'w', encoding='utf-8' ) as f:
        f.write(text)
    
"""-------------------------------------------------------------------------+++
Everything about test 1 - spacy basics.
"""
def test1_ru():
    nlp = Russian()
    doc = nlp( readf(TXT_RU) )
    return doc
    
def test1_en():
    nlp = English()
    doc = nlp( readf(TXT_EN) )
    return doc

def resume_test1( doc ):
    for token in doc[ :len(doc)-1]:
        if not token.like_num: continue
        next_token = doc[ token.i+1 ]
        if not next_token.text=='%': continue
        print( 'Found %:', token.text )
        break 

"""-------------------------------------------------------------------------+++
Everything about test 2 - spacy and stanza statistical models.
"""
def test2_ru():
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    doc = nlp( readf(TXT_RU) )
    return doc
    
def test2_en():
    nlp = spacy.load('en_core_web_sm')
    
    doc = nlp( readf(TXT_EN) )
    return doc
    
def resume_test2( doc ):
    for token in doc:
        print( token.text, token.pos_ )
        
"""-------------------------------------------------------------------------+++
Everything about test 3 - spacy matcher.
"""
def test3_ru():
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    pattern = [
        {'LOWER':'судя'}, # LOWER is case-insensitive
        {'LOWER':'по'},
        {'LOWER':'всему'},
        {'IS_PUNCT':True}, # any punctuation mark
        ]
    matcher = Matcher( nlp.vocab )
    matcher.add( 'custom_test_russian_pattern', None, pattern )
    
    doc = nlp( readf(TXT_RU) )
    
    found_matches = matcher(doc)
    for row in found_matches:
        print(row)
        L,R = row[1:]
        print( doc[L:R] )
    
def test3_en():
    nlp = spacy.load('en_core_web_sm')
    
    pattern = [
        {'LOWER':'a', 'OP':'?'}, # optional article
        {'LOWER':'parody', 'POS':'NOUN'}, # LOWER is case-insensitive
        {'LOWER':'of', 'OP':'?'},
        ]
    matcher = Matcher( nlp.vocab )
    matcher.add( 'custom_test_english_pattern', None, pattern )
    
    doc = nlp( readf(TXT_EN) )
    
    found_matches = matcher(doc)
    for row in found_matches:
        print(row)
        L,R = row[1:]
        print( doc[L:R] )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    """
    # autorun test 1
    # creates two docs and seeks the value before the '%'
    docs = [ test1_ru(), test1_en() ]
    for doc in docs:
        resume_test1(doc)
    #"""
    
    """
    # autorun test 2
    # creates two docs
    # applies to them corresponding statistical models
    # saves html with named entity recognition and dependency arrows
    docs = [ test2_ru(), test2_en() ]
    #for doc in docs: resume_test2(doc) # it works, i don't actually need that output
    markup = displacy.render( docs, style='ent', page=True, jupyter=False )
    savef( 'ent.html', markup )
    markup = displacy.render( docs, style='dep', page=True, jupyter=False )
    savef( 'dep.html', markup )
    #"""
    
    #"""
    # autorun test 3
    # creates two docs
    # applies to them corresponding statistical models
    # tries to find some custom matches
    test3_ru()
    test3_en()
    #"""

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2021.01.13 → 2021.01.13
