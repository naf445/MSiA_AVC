data/booksummaries/booksummaries.txt: config/src_config.yml
	python src/1-getData.py
raw_data: data/booksummaries/booksummaries.txt

data/booksummaries/booksummaries_genres_cleaned.csv: config/src_config.yml
	python src/2-clean_genres.py
clean_genres: data/booksummaries/booksummaries_genres_cleaned.csv

data/booksummaries/books_Porter_True.csv: config/src_config.yml
	python src/3-clean_summaries_gen_vecs.py True Porter
clean_summaries_gen_vecs: data/booksummaries/books_Porter_True.csv

models/LDA_model.pkl: config/src_config.yml
	python src/4-gen_LDA_model.py
gen_LDA_model: models/LDA_model.pkl

data/booksummaries/booksummaries_ready2train.csv: config/src_config.yml
	python src/5-gen_LDA_vecs.py
gen_LDA_vecs: data/booksummaries/booksummaries_ready2train.csv

models/RFC_deployment_model.pkl: config/src_config.yml
	python src/6-train_model.py
train_model: models/RFC_deployment_model.pkl

all: raw_data clean_genres clean_summaries_gen_vecs gen_LDA_model gen_LDA_vecs train_model