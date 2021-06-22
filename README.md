# Knowledge-Based Robotic Access and Retrieval

## Git Command-Line Reference

### Making a branch:

git branch new-branch\
git checkout new-branch\
git push

### Pulling a branch:

git checkout branch-name\
git pull

### Merging one branch with another:

git checkout target-branch _# Usually target-branch = master_\
git pull\
git merge source-branch _# You may have to deal with merge conflicts_

## Python Virtual Environment Reference

### Making a virtual environment:

Navigate to the project directory\
py -m venv env _# By convention the environment is usually called 'env'_\
.\env\Scripts\activate _# Do this prior to using pip or running any code_

### Assigning a virtual environment in VS Code:

Create the virtual environment\
_# In VS Code:_\
Hit ctrl-shift-p\
Type 'python interpreter'\
Click 'Python: Select Interpreter'\
Select Python 3.9.5 ('env': venv)\
_# If this doesn't appear in the list:_\
Hit 'Enter interpreter path...'\
Hit 'Find...'\
Navigate to .\env\Scripts\
Select python

### Importing libraries:

pip install -r requirements.txt

### Adding new libraries:

pip install python-library\
pip freeze > requirements.txt

### Adding node.js:

go to https://nodejs.org/en/ and download the LTS version and install it.

### Adding node.js libraries:

run:
cd webapp
npm install

### Starting everything:

in \robart run: py app.py
in \robart\webapp run: npm start