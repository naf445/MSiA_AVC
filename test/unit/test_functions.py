import sys
sys.path.append('../../src/helpers')
sys.path.append('../../src')
clean_genres = __import__('2-clean_genres')
from data_manipulation import custom_transformers as ct
import pandas as pd

def test_rule_swapper():
    # inputs
    genreList = ['fiction', 'history_fiction', 'mystery_fiction', 'love', 'romance']
    rules_dict= {'fiction':['history_fiction','mystery_fiction'],\
    														'romance':'love'}
    
    # expected output
    swapped_genreList = ['fiction', 'fiction', 'fiction',\
    'romance', 'romance']
    
    # check expected output against function output
    assert swapped_genreList == clean_genres.ruleSwapper(genreList, rules_dict)

def test_remove_duplicates():
    # inputs
    genreList = ['fiction', 'fiction', 'fiction',\
    'romance', 'romance']
    
    # expected output
    slim_genreList = ['fiction', 'romance']

    # check expected output against function output
    assert slim_genreList == clean_genres.removeDuplicates(genreList)

def test_tokenize():
	# inputs
	books = pd.DataFrame({'plotSum':['the cat went', 'over the bridge']})
	tokenizer = ct.Tokenizer()
	tokenized_books = tokenizer.transform(books)

	# expected output
	new_tokenized_books = pd.DataFrame({'plotSum':[['the', 'cat', 'went'], ['over', 'the', 'bridge']]})

	# check expected output against function output
	print(tokenized_books)
	print(new_tokenized_books)

	assert tokenized_books.equals(new_tokenized_books) 

def test_filter_sentence():
	# inputs
	tokenized_books = pd.DataFrame({'plotSum':[['John', 'cat', '!'], [',', 'Kevin', 'bridge']]})
	filterer_of_sentences = ct.Filter_sentence()
	filtered_books = filterer_of_sentences.transform(tokenized_books)
	
	# expected output
	clean_books = pd.DataFrame({'plotSum':[['cat'], ['bridge']]})

	# check expected output against function output
	assert clean_books.equals(filtered_books) 



