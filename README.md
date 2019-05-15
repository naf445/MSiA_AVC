
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

## Setup

### 1.) Acquiring and Storing Data
In the root folder is a bash script `getData.sh` which takes one argument `<s3://bucket-name>`. This script will retrieve the data folder from this [website](http://www.cs.cmu.edu/~dbamman/booksummaries.html) and place it in `data/booksummaries`. The script will then take this new directory and copy its contents to an S3 bucket provided by the user.  
**Note:** You must have AWS CLI [installed](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) & [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html), and an existing S3 bucket connected to your account.

```bash
$ getData.sh <s3://bucket-name>
```

### 2.) Setting Up a MySQL DB Instance (RDS or Local SQLite)
#### To Instantiate in RDS
In order to set up the MySQL instance in RDS, there are 2 files to run. The first is `mysqlconfig.sh` which takes 3 arguments <MYSQL_USER>, <MYSQL_PASSWORD>, & <MYSQL_HOST>. <MYSQL_HOST> is specified in your AWS RDS console, under the heading "Endpoint" in the "Connectivity & security" tab. 
```bash
$ source mysqlconfig.sh <MYSQL_USER> <MYSQL_PASSWORD> <MYSQL_HOST>
```
This file will simply set these values as temporary environmental variables.
After this, you will run the `sqlalchemy_mysql_setup.py` file in order to create your MySQL database table schema and send this to RDS. (At this point, remember to configure your RDS security group to have a rule allowing inbound traffic from whatever IP address you will be using to communicate with the RDS.) This command requires you to specify `RDS` as a command line argument and will use the values set by `mysqlconfig.sh`. You can check that these values were recorded successfully by running `echo $MYSQL_USER` and making sure your information appears in your terminal.

```bash
$ python sqlalchemy_mysql_setup.py RDS
```

#### To Instantiate Locally Using SQLite

In order to set up the MySQL instance locally there is only 1 file to run.
You will run the `sqlalchemy_mysql_setup.py` file. This command requires you to specify `sqlite` as a command line argument. The default behavior is to create a databse called `msia423.db` in the data folder of this repository. It is currently not possible to change the location of the `msia423.db` creation.

```bash
$ python sqlalchemy_mysql_setup.py sqlite
```

In order to check that the database was created correctly, go to a machine with MySQL command line tools installed. Connect to your RDS instance using 
``` bash
$ mysql -u <RDS-username> -p -h <RDS-endpoint>
```
Next you can use `mysql> show databases;` and the table `msia423` should be present. Then you can type `mysql> use msia423;` (if it appears) and then `mysql> show tables;`.


## Other
* **Data Source:** [CMU Book Summary Dataset](http://www.cs.cmu.edu/~dbamman/booksummaries.html)








