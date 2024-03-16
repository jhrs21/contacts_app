# Project for FactorialHR interview 

## Description
We want a Frontend + Backend application that allows you to create, read, update and delete a list of contacts.
Each contact will have: 
- First name
- Last name
- Email
- Phone number 

All the fields are mandatory, and there can’t be two contacts with the same email. You should be able to see the history of edits on those contacts. The contacts will be persisted in the database.

## Technologies
- VueJS (frontend)
- Flask (backend)
- SQLite (database)

## Installation

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ flask run --port=5001 --debug
    ```

    Navigate to [http://localhost:5001](http://localhost:5001)

2. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run dev
    ```

    Navigate to [http://localhost:5173](http://localhost:5173)

## Setup DB
The database should be initialized when the Flask server is started.
There are some commands to manage the database

- Initialize a clean database
   ```sh
    $ cd server
    $ python init_db.py
    ```

- Initialize a database with sample data
   ```sh
    $ cd server
    $ python init_db.py data
    ```
  
- Wipe data from the database
   ```sh
    $ cd server
    $ python init_db.py clean
    ```