# SEP2021


## Installation Guide
> This section discusses the initial installation of the tool
Make sure you have at least py3.8.1 (with paths enabled) and [nodeJS LTS](https://nodejs.org/en/download/) (*important, must be LTS*).
Additionally you need 


First clone the repository from github. Next navigate to the frontend folder in your file explorer. (SEP2021\WriterDesk\frontend)

click the file `startEnv.bat` 
`pip install virtualenv`
`cd backend` 
`py -m venv env`

Then go back to the frontend folder in you file explorer and run `startEnv.bat` 

`pip install flask`
`npm install`
`pip install psycopg2`

Now open 2 instances of `startEnv.bat` (by clicking them):

In one instance, run `npm run start-backend`
In the other instance run `npm start`

Now, if it did not happen already, go to your browser and open [this link](http://localhost:3000)


## Coding Guide
> This section discusses coding support




