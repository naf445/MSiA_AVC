## Planning

**Themes:** 

* Model Development (MD)
* Front End Experience (FEE)
* Value Extraction (VE)
* Infrastructure Building (IB)
* Code Improvement (CI)

**Stories:**   

Backlog | Points | Status| Theme
------- |:------:| :-----------: | :-----:
Finish analysis of genres to narrow them down to 6-10 single word categories| medium | :large_orange_diamond: | MD
Get a working model which takes in a book summary and returns suggested meta data (genre) about that book  | Epic | :large_orange_diamond: | MD
Get relational database (local sqlite or AWS RDS) set up, schemas decided, and scripts to setup/interact with them | Epic | :large_orange_diamond: | IB
Get basics of a flask app up and running | Epic | :x: | FEE
Convert notebooks into scripts | 4 | :large_orange_diamond: | CI
Make sure entire app can run on other machines (mac/linux/windows) | Epic | :x: | IB
Add logging to all python files | 4 | :large_orange_diamond: | CI
Add config.yml file which houses all function parameters/settings/filepaths/etc... | Epic | :large_orange_diamond: | CI
Add documentation and docstrings to all classes, functions, etc... | 4 | :x: | CI
Add Unit testing | 4 | :x: | CI
Create makefile which can automate entire model building process | 4 | :x: | CI
Finalize what I will use RDS and S3 for | 4 | :large_orange_diamond: | IB

Icebox | Points | Status | Theme
-------|:------:| :----------: | :---:
Deploy my app on an AWS EC2 server so my app can be running continuously | Epic | :x: | IB
Have app interface with a relational database (local sqlite or AWS RDS) to possibly pull fitted model parameters, store user input for future use, or other features | Epic | :x: | IB
As a user I would like my entered text to be analyzed so that I can receive meta data suggestions | 2 | :x: | FEE
As a user I would like to be able to indicate whether I am satisfied with the suggestions | 2 | :x: | FEE
As a developer I want to be able to see what % of recommendations are 'acceptable' as judged by the user so that I can improve my model and measure my app's performance and usefulness | 2 | :x: | MI
As a developer I want to know how long an author had spent thinking on these topics for the piece of interest so that I could know what type of users are using my app  | :heavy_minus_sign: | :x: | VE

Completed Stories| Status | Theme
-------| -------| -------|
Get data set containing text titles, their summaries, etc... | :heavy_check_mark: | MD
Get conda & virtual environment files set up (requirements.txt and environment.yml) | :heavy_check_mark: | IB
Get AWS EC2 server up and running | :heavy_check_mark: | IB
Get S3 bucket running and configured | :heavy_check_mark: | IB

