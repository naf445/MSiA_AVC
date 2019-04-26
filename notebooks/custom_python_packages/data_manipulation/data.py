import pandas as pd
import ast

def loadAndClean(path=True):
    """ 
    Loads and cleans the booksummaries.txt data file for more
    exploratory analysis and machine learning training. 
  
    Parameters: 
    path (str): Relative path to the booksummaries.txt data file
  
    Returns: 
    pandas.DataFrame: Cleaned version of the booksummaries.txt file in DataFrame form 
    """
    # cleaned column names
    column_names = ['wikiArticleID','freebaseID','bookTitle','author','pubDate','bookGenre', 'plotSum']
    
    booksummaries = pd.read_csv(path, sep='\t', header=None, names=column_names)
    
    # drop values which are NA for bookGenre or plotSum which would not be trainable
    booksummaries.dropna(subset = ['bookGenre','plotSum'] , inplace=True)
    
    booksummaries['bookGenre'] = booksummaries.apply(lambda row:\
                                    list(ast.literal_eval(row.bookGenre).values()), axis=1)
    
    
    booksummaries['bookGenre'] = booksummaries['bookGenre'].apply(lambda row:\
                                    [v.strip().lower().replace("'",'').replace(' ','_') for v in row])
    
    return booksummaries