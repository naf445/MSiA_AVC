data/booksummaries/booksummaries.txt: config/src_config.yml
	bash src/getData.sh
raw_data: data/booksummaries/booksummaries.txt

data/booksummaries/clean_book_summaries.csv: config/src_config.yml data/booksummaries/booksummaries.txt
	python src/clean_book_summaries.py
cleaned_data: data/booksummaries/clean_book_summaries.csv

all: raw_data cleaned_data