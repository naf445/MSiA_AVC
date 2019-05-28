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

## Repo Structure

```
├── README.md                         <- Welcome. You are here.
│
├── app/
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config/                           <- Directory for configuration files for logging, model parameters, etc...
│   ├── logging/                      <- Configuration files for python loggers
│   ├── config.yml                    <- Configuration file for app: model training, scoring, database info, etc...
|   ├── config.py                     <- Configuration file for Flask app
|
├── data/                             <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── booksummaries/                <- Storage repository for project's main data, not synced with git
│   ├── names/                        <- Storage repository for some name data, not synced with git
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs/                             <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures/                          <- Generated graphics and figures to be used in repo.
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive/                      <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks/
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── demonstration/                <- Template notebooks for analysis with useful imports and helper functions. 
│
├── src/                              <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── get_data.py                   <- Script for getting data from source and storing locally or in AWS S3 bucket
│   ├── get_data.sh                   <- Script for getting data from source and storing locally or in AWS S3 bucket
│   ├── clean_data.py                 <- 
│   ├── generate_features.py          <-  
│   ├── train_model.py                <-  
│   ├── score_model.py                <- 
│   ├── sqlalchemy_mysql_setup.py     <- Instantiating MySQL database 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
|
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── makefile.sh                            <- Simplifies the execution of one or more of the src scripts
├── app.py                            <- Flask wrapper for running the model 
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Setup

### 1.) Setting Up the Environment
To increase the probability of this project working on your machine, please start by creating and activating a conda environment using the `environment.yml` file, or doing the same with a virtual environment using the `requirements.txt` file found in the root directory.  

### 2.) Acquiring and Storing Data
In the root folder is a bash script `getData.sh` which takes one argument `<s3://bucket-name>`. This script will retrieve the data folder from this [website](http://www.cs.cmu.edu/~dbamman/booksummaries.html) and place it in `data/booksummaries`. The script will then take this new directory and copy its contents to an S3 bucket provided by the user.  
**Note:** You must have AWS CLI [installed](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) & [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html), and an existing S3 bucket connected to your account.

```bash
$ bash getData.sh <s3://bucket-name>
```

### 3.) Setting Up a MySQL DB Instance (RDS or Local SQLite)
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

In order to check that the database was created correctly, go to a machine with MySQL command line tools installed. Connect to your RDS instance using the following:
``` bash
$ mysql -u <RDS-username> -p -h <RDS-endpoint>
```
After providing the password used to create your RDS instance, you can use the following commands to ensure your MySQL instantiation worked. 
```
mysql> show databases;
mysql> use avc423;
mysql> show tables;
```
These commands should show the database `msia423` and the subsequent tables which were created and that you can now query.

#### To Instantiate Locally Using SQLite

In order to set up the MySQL instance locally there is only 1 file to run.
You will run the `sqlalchemy_mysql_setup.py` file. This command requires you to specify `sqlite` as a command line argument. The default behavior is to create a databse called `msia423.db` in the data folder of this repository. It is currently not possible to change the location of the `msia423.db` creation.

```bash
$ python sqlalchemy_mysql_setup.py sqlite
```


## Other
* **Data Source:** [CMU Book Summary Dataset](http://www.cs.cmu.edu/~dbamman/booksummaries.html)








