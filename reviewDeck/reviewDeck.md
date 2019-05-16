## Outline

* **Highlights** 
* **Progress Review**
* **Demo/Analysis**
* **Lessons Learned**
* **Recommendations For Next Sprint**    
 
# Highlights  

## Highlight 1
* Created a notes.md Document with Notes on Various Topics for Reference
<span style="font-size:20pt;">
    * Latent Dirichlet Allocation with sklearn
    * Word2Vec
    * Doc2Vec
    * Other Github Repos on Similar Topics
    * Text Classification in Python
    * Topic Modeling in Python with LDA
    * Sklearn Pipelines and Custom Transformers
    * Basic Sklearn Syntax for Pipelines & CV
</span>

## Highlight 2
* Basic EDA
<span style="font-size:20pt;">
    * 12841 books and their summaries after dropping the NA's
    * 227 unique genre tags to roll up to a smaller amount of categories
    *   | Genre|Count|
        |---|---|
        |fiction|4747|
        |speculative_fiction|4314|
        |science_fiction|2870|
        |novel|2463|
        |fantasy|2413|  
</span>

## Highlight 3
* Made Progress on Model Development
<span style="font-size:20pt;">
    * Analysis done on rolling up genre combinations into fewer categories
        -   | Genre Combination |Appearances|
        |---|---|
        |science_fiction, fiction, speculative_fiction|1000|
        |fiction, speculative_fiction, fantasy|947|
        |(mystery, suspense, fiction| 617|
        |fiction, childrens_literature, speculative_fiction|558|
        |(science_fiction, speculative_fiction, fantasy|557|
</span>

## Highlight 4
* Created Python Package to Aid in Data Exploration and Modeling
<span style="font-size:20pt;">
    * Created load_and_clean() function to enable quick loading
    * Created custom sklearn transformers to allow multiple methods of data cleaning
        - Optional name filterer
        - Word stemmer
            + Porter & Lancaster Methods Optional
        - Word lemmatizer
</span>

# Progress Review   
  
## Stories Completed
- Stories Completed
<span style="font-size:20pt;">
    1. Got data set containing text titles, their summaries, and their genre labeled so I can train my model ✅
    2. Set up an environment and a requirements file so I can recreate the environment necessary to run the model/app ✅
    3. Set up an AWS EC2 server instance ✅
    4. Set up an AWS RDS instance and local SQLite instance ✅
    5. Moved data to S3 database ✅  
</span>

# Demo/Analysis  

## Initial LDA Run Without Name Filtering
<img src="Resources/initialLDA.png" height=400/>

# Lessons Learned  

## Modeling Side
* Mostly just been learning a lot about nlp with python, topic modeling, and how to use sklearn to make this proccess smooth.

## Infrastructure / AWS
* Learned a lot about S3, RDS, EC2, AWS in general, and writing bash scripts!


# Next Sprint Story Recommendations

## Stories to be Done Next
* Finish rolling up genres into a few categories
* Finish model development and prediction proccess
* Finalize RDS/SQLite schema
* Work on UI front including Flask app and think about how all the various pieces will interface together
