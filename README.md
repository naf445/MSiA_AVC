
# Judging a Book by its Cover
## An MSiA AVC Final Project
---
## Team
**Lead Developer** : Nathan Franklin  
**Lead QA** : Tony Colucci  
**Faculty Advisors** : Chloe Mawer & Fausto Inestroza  

## Project Charter

**Vision:** 
A potential reader of a piece of prose - whether an article, a novel, a blog post, or something else - cannot know the contents of that piece without actually reading it. Thus they cannot know if they will enjoy its contents until they have already consumed them. The human heuristic to solve this problem is to make a judgment call based on the observable characteristics of a text. In effect, humans must 'judge a book by its cover', as well as by other features we will collectively label 'meta details' (genre, title, reviews, length, etc...). Thus, it is extremely important for the people who make these decisions about a piece of writing to provide potential readers with meta details which most accurately convey the contents of the piece. This project exists to ease some of this burden by using machine learning to give suggestions to the authors, editors, publishers, or other decision makers involved in this proccess.

**Mission:** 
The goal of this project is to give suggestions for meta data based on a user's input. In this project, the model will generate these suggestions based on a user-provided summary of the larger prose piece in question. These suggestions will hopefully be informative and useful for those making these decisions, allowing them to more accurately represent their text to readers.

**Success Criteria:** 
* Model Performance: Genre classification accuracy of >= 75% 
* Business Performance:  Users consider meta detail suggestions to be helpful and to accurately convey information about the larger piece >= 50% of the time.

## Planning

**Themes:** 
* Initial Model Development (IMD)
* Model Improvement (MI)
* User Experience (UE)
* Value Extraction (VE)
* Infrastructure Building (IB)

**Stories:**   

Backlog | Points | Next 2 Weeks? | Theme
------- |:------:| :-----------: | :-----:
As a developer, I would like a data set containing text titles, their summaries, and their genre labeled so I can train my model.  | 4 | :heavy_check_mark: | IMD
As a future user/developer, I would like an environment set up and a requirements file so I can recreate the environment necessary to run the model/app | 1 | :heavy_check_mark: | IB
As a developer, I want a model, which is trained on sample data, to take in a book summary and return suggested meta data (genre) about that book so that I can use it in my app  | Epic | :heavy_check_mark: | IMD
As a user I want to be able to type or paste text into a textbox so it can be analyzed | 2 | :x: | UE
As a user I would like my entered text to be analyzed so that I can receive a genre suggestion | 2 | :x: | UE
As a user I would like to be able to indicate whether I am satisfied with the suggestions | 2 | :x: | UE
As a developer I want to be able to see what % of recommendations are 'acceptable' as judged by the user so that I can improve my model and measure my app's performance and usefulness | 2 | :x: | MI

Icebox | Points | Next 2 Weeks? | Theme
-------|:------:| :----------: | :---:
As a user I would like my entered text to be analyzed so that I can receive a title suggestion   | Epic | :heavy_minus_sign: | UE
As a user I would like my entered text to be analyzed so that I can receive a cover image suggestion   | Epic | :heavy_minus_sign: | UE
As a developer I want to know how long an author had spent thinking on these topics for the piece of interest so that I could know what type of users are using my app  | :heavy_minus_sign: | :heavy_minus_sign: | VE
As a developer, I would like a flask app to be able to integrate all of these tasks, presenting a user interface which communicates with the model and also my database | Epic | :x: | :heavy_minus_sign:
As a developer, I would like my app to be deployed on an AWS EC2 server so my app can be running continuously | Epic | :x: | IB
As a developer, I would like my app to interface with a relational database to possibly pull fitted model parameters, store user input for future use, or other features | Epic | :x: | IB
As a developer, I would like my app to interface with an Amazon S3 database to pull stored data | Epic | :x: | IB



## Data
* [CMU Book Summary Dataset](http://www.cs.cmu.edu/~dbamman/booksummaries.html)

## Misc.
* Formatted on [stackedit.io](https://stackedit.io/app#)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExMTQyNTQ5NzcsNDg0MzA2NTcyLDYwMz
czNjE3NiwtMTQ3MTUzMjA2MCwtMTYzNDM4Mjg1OCwtNDAxODc4
NTY2LDEwNTM4NzI5NDJdfQ==
-->
