
# Charter

## Project Charter

**Vision:** 
One difficult task when it comes to writing for an audience is coming up with the meta details & labels, i.e. title, cover image, genre, etc...  This project exists to ease some of that burden by using machine learning to give suggestions for these items to authors, editors, publishers, or whoever is making these decisions.

**Mission:** 
Give suggestions for meta data about a piece of writing, based on a user's input (a summary of the larger prose piece in question).  

**Success Criteria:** 
* Model Performance: ee it accuracy of >= 75% 
* Business Performance:  User considers meta detail ugeion tobe helpful >= 50% of the time.

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
As a user I would like my entered text to be analyzed so that I can receive a ee suggestion | 2 | :x: | UE
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
eyJoaXN0b3J5IjpbNjAzNzM2MTc2LC0xNDcxNTMyMDYwLC0xNj
M0MzgyODU4LC00MDE4Nzg1NjYsMTA1Mzg3Mjk0Ml19
-->