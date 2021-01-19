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
Everything about chapter2.
"""
def ch2test1_ru():
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    wordstr = 'программа'
    wordhash = nlp.vocab.strings[wordstr]
    print( 'Hash test RU for word "%s":'%wordstr, wordhash )
    try:
        reverse = nlp.vocab.strings[wordhash]
        print( 'Looking up string via hash↑: %s ...it works.'%reverse )
    except Exception as ex:
        print( "Looking up string via hash↑... it doesn't work.")
        print( ex )

def ch2test1_en():
    nlp = spacy.load('en_core_web_md')
    
    wordstr = 'program'
    wordhash = nlp.vocab.strings[wordstr]
    print( 'Hash test EN for word "%s":'%wordstr, wordhash )
    try:
        reverse = nlp.vocab.strings[wordhash]
        print( 'Looking up string via hash↑: %s ...it works.'%reverse )
    except Exception as ex:
        print( "Looking up string via hash↑... it doesn't work.")
        print( ex )
        
def ch2test2_ru():
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    words = [ 'Плевать', 'какой', 'текст' ]
    spaces = [ True, True, False ]
    doc = spacy.tokens.Doc( nlp.vocab, words, spaces )
    print( doc.text )
    
    span = spacy.tokens.Span( doc, 1,3, label='intentionally_wrong' )
    doc.ents = [span]
    
    markup = displacy.render( doc, style='ent', page=True, jupyter=False )
    savef( 'ent_ru.html', markup )

def ch2test2_en():
    nlp = spacy.load('en_core_web_md')
    
    words = [ 'Whatever', 'this', 'is' ]
    spaces = [ True, True, False ]
    doc = spacy.tokens.Doc( nlp.vocab, words, spaces )
    print( doc.text )
    
    span = spacy.tokens.Span( doc, 0,2, label='intentionally_wrong' )
    doc.ents = [span]
    
    markup = displacy.render( doc, style='ent', page=True, jupyter=False )
    savef( 'ent_en.html', markup )
        
def ch2test3_ru():
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    words = [ 'Плевать', 'какой', 'текст' ]
    spaces = [ True, True, False ]
    doc = spacy.tokens.Doc( nlp.vocab, words, spaces )
    
    print( doc.text )
    print( len(doc.vector) )

def ch2test3_en():
    nlp = spacy.load('en_core_web_md')
    
    words = [ 'Whatever', 'this', 'is' ]
    spaces = [ True, True, False ]
    doc = spacy.tokens.Doc( nlp.vocab, words, spaces )
    
    print( doc.text )
    print( len(doc.vector) )
        
def ch2test4_ru():
    print( "For this RU model it doesn't work yet." )
    return None
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    words = [ 'Плевать', 'какой', 'текст' ]
    spaces = [ True, True, False ]
    doc1 = spacy.tokens.Doc( nlp.vocab, words, spaces )
    words = [ 'Чай', 'и', 'кофе' ]
    spaces = [ True, True, False ]
    doc2 = spacy.tokens.Doc( nlp.vocab, words, spaces )
    
    print( doc1.text )
    print( doc2.text )
    print( doc1.similarity(doc2) )

def ch2test4_en():
    nlp = spacy.load('en_core_web_md')
    
    words = [ 'Whatever', 'this', 'is' ]
    spaces = [ True, True, False ]
    doc1 = spacy.tokens.Doc( nlp.vocab, words, spaces )
    words = [ 'Tea', 'and', 'coffee' ]
    spaces = [ True, True, False ]
    doc2 = spacy.tokens.Doc( nlp.vocab, words, spaces )
    
    print( doc1.text )
    print( doc2.text )
    print( doc1.similarity(doc2) )
        
"""-------------------------------------------------------------------------+++
Everything about chapter3.
"""
def ch3test1_ru():
    #stanza.download('ru') # already done # download rus statistical model
    
    snlp = stanza.Pipeline( lang='ru' )
    nlp = spacy_stanza.StanzaLanguage( snlp )
    
    #doc = spacy.tokens.Doc( readf(TXT_RU) )
    
    print( nlp.pipe_names )
    print( nlp.pipeline )

def ch3test1_en():
    nlp = spacy.load('en_core_web_md')
    
    #doc = spacy.tokens.Doc( readf(TXT_EN) )
    
    print( nlp.pipe_names )
    print( nlp.pipeline )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    """---------------------------------------------------------------------+++
    Chapter 1.
    """
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
    
    """
    # autorun test 3
    # creates two docs
    # applies to them corresponding statistical models
    # tries to find some custom matches
    test3_ru()
    test3_en()
    #"""
    
    """---------------------------------------------------------------------+++
    Chapter 2.
    """
    """
    # autorun test 1
    # test nlp.vocab.strings lookup table
    ch2test1_ru()
    ch2test1_en()
    #"""
    
    """
    # autorun test 2
    # manually construct doc and span object
    ch2test2_ru()
    ch2test2_en()
    #"""
    
    """
    # autorun test 3
    # see if 300D word vectors work
    ch2test3_ru()
    ch2test3_en()
    #"""
    
    """
    # autorun test 4
    # compare two documents
    ch2test4_ru()
    ch2test4_en()
    #"""
    """---------------------------------------------------------------------+++
    Chapter 3.
    """
    #"""
    # autorun test 1
    # compare two documents
    ch3test1_ru()
    ch3test1_en()
    #"""

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2021.01.13 → 2021.01.19
