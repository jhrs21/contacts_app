# Project for FactorialHR interview 

## Description
We want a Frontend + Backend application that allows you to create, read, update and delete a list of contacts.
Each contact will have: 
- First name
- Last name
- Email
- Phone number 

All the fields are mandatory, and there can’t be two contacts with the same email. You should be able to see the history of edits on those contacts. The contacts will be persisted in the database.

## Solution
A basic API was built using Flask. The main file is `app.py` where all the endpoints are stored.
```sh 
$ flask routes                                                                                                                     ✔  11m 5s  contacs_app Py  11:29:01 

Endpoint          Methods      Rule
----------------  -----------  -----------------------
all_contacts      GET, POST    /contacts
ping_pong         GET          /ping
single_changelog  GET          /changelog/<contact_id>
single_contact    DELETE, PUT  /contacts/<contact_id>
static            GET          /static/<path:filename>
```

_Notes_: endpoints `/ping` and `/static/<path:filename>` are not part of the technical solution

## Technologies
- Vue JS (frontend)
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

## Database

### Schema

The schema includes only two tables.

```sql
    CREATE TABLE CONTACTS (
        id TEXT PRIMARY KEY NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number TEXT NOT NULL);
    CREATE TABLE CHANGELOG (
        id TEXT PRIMARY KEY NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        contact_id TEXT NOT NULL,
        action TEXT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (contact_id) REFERENCES CONTACTS(id));
```


### Setup
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
  
## Tests

Tests were created only for the backend (Flask)

```sh
$ cd server
$ pytest tests
```