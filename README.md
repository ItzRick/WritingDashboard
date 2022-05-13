# SEP2021


## Installation Guide
> This section discusses the initial installation of the tool
Make sure you have at least py3.8.1 (with paths enabled) and [nodeJS LTS](https://nodejs.org/en/download/) (*important, must be LTS*).
Additionally you need 


First clone the repository from github. Next navigate to the main folder in your file explorer. (SEP2021\WriterDesk1)

Now do `pip install virtualenv`
click the file `startEnv.bat` 
`pip install virtualenv`
`cd backend` 
`py -m venv env`

Then go back to the WriterDesk1 folder in you file explorer and run `startEnv.bat`. Then run the following command to install all packages 'pip install -r requirements.txt'

Now open 2 instances of `startEnv.bat` (by clicking them):

In one instance, run `npm run start-backend`
In the other instance run `npm start`

Now, if it did not happen already, go to your browser and open [this link](http://localhost:3000)

(note that the `npm start` might not work when you have a vpn activated)

Install PostgreSQL ([This link](https://www.postgresql.org/download/)), set a system environment variable called "DATABASE_URL" to <postgresql://postgres:{password}@localhost:5432/database1>, where this password is the password you have chosen in the postgresql installation. 

### Adding Requirements
If you add a package, you have to update the requirements document. Make sure you are located in WriterDesk1 and run `pip freeze > requirements.txt`

### Test cases
A nice tutorial for flask test cases can be found in [This link](https://testdriven.io/blog/flask-pytest/). In short we use pytest for the test cases. In the tests folder one can define setup stuff before the test cases needed to be run and cleanup stuff after the test cases are done in the conftest.py folder. We do this by having the line `@pytest.fixture(scope='module')` above the function. Or with scope='function' if this needs to be run before every function is run. Then one can define instructions to be run before the test case, followed by yield at which the test cases will be run, followed by stuff that cleans up this stuff. The atual test cases are defined in the unit or functional folder respectively. These test cases consist of functions with assert's, which should be satisfied. Stuff from the 'conftest.py' file should be passed as function arguments if this is required in the test cases. 

## Coding Guide
> This section provides some usefull coding tools and tutoriols for flask and ReactJS

Frontend: ReactJS, Backend: Flask, Database: psycopg2 adapter for PostgreSQL

List of good tutorials:
- [Easy Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask and SQL, databases](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
- [React Tutorial](https://reactjs.org/tutorial/tutorial.html)
- [Better React Tutorial](https://www.youtube.com/watch?v=b9eMGE7QtTk)

- [Long, but good react tutorial](https://www.youtube.com/watch?v=w7ejDZ8SWv8), can be watched at 1.25 speed

## Code Style Guide
> [Required by the course](https://canvas.tue.nl/courses/18931/files/folder/SEP%20Materials/Assessment_and_Guidelines?preview=3982997), usefull for use

Code should not be too complex, for this there is a measure _Software Lines of Code (SLOC)_, these are effective lines (excluding comments and whitespace).
- Modules, SLOC <= 400

More than 15% of lines, should be comments

No cyclic dependencies between classes

