import sqlite3
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from init_db import create_database_and_table

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

DB_FILE = 'app.db'
create_database_and_table()


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/contacts', methods=['GET', 'POST'])
def all_contacts():
    response_object = {'status': 'success'}
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Set row factory to sqlite3.Row
    c = conn.cursor()

    if request.method == 'POST':
        post_data = request.get_json()
        contact_id = uuid.uuid4().hex
        c.execute("INSERT INTO contacts (id, first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?, ?)",
                  (contact_id, post_data.get('first_name'), post_data.get('last_name'), post_data.get('email'), post_data.get('phone_number')))
        conn.commit()
        insert_changelog_entry('CREATE', contact_id)

        response_object['message'] = 'Contact added!'
    else:
        c.execute("SELECT * FROM contacts")
        contacts = c.fetchall()
        response_object['contacts'] = []
        for contact in contacts:
            contact_dict = dict(contact)
            response_object['contacts'].append(contact_dict)

    conn.close()
    return jsonify(response_object)


@app.route('/contacts/<contact_id>', methods=['PUT', 'DELETE'])
def single_contact(contact_id):
    response_object = {'status': 'success'}
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if request.method == 'PUT':
        post_data = request.get_json()
        c.execute("UPDATE contacts SET first_name=?, last_name=?, email=?, phone_number=? WHERE id=?",
                  (post_data.get('first_name'), post_data.get('last_name'), post_data.get('email'), post_data.get('phone_number'), contact_id))
        conn.commit()
        insert_changelog_entry('UPDATE', contact_id)
        response_object['message'] = 'Contact updated!'
    if request.method == 'DELETE':
        c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        insert_changelog_entry('DELETE', contact_id)
        response_object['message'] = 'Contact removed!'

    conn.close()
    return jsonify(response_object)


@app.route('/changelog/<contact_id>', methods=['GET'])
def single_changelog(contact_id):
    response_object = {'status': 'success'}
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Set row factory to sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM changelog WHERE contact_id=? ORDER BY created_at DESC LIMIT 10", (contact_id,))
    changelogs = c.fetchall()

    response_object['changelog'] = []
    for change in changelogs:
        change_dict = dict(change)
        response_object['changelog'].append(change_dict)

    conn.close()
    return jsonify(response_object)


def insert_changelog_entry(action, contact_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    changelog_id = uuid.uuid4().hex
    c.execute("INSERT INTO CHANGELOG (id, contact_id, action, description) VALUES (?, ?, ?, ?)",
              (changelog_id, contact_id, action, f'{action.capitalize()} contact with ID: {contact_id}'))

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == '__main__':
    app.run()
