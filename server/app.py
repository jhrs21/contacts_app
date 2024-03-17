import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from init_db import create_database_and_table
import database_services as db

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

create_database_and_table()


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/contacts', methods=['GET', 'POST'])
def all_contacts():
    try:
        response_object = {'status': 'success'}

        if request.method == 'POST':
            post_data = request.get_json()
            contact_id = uuid.uuid4().hex
            db.execute_query("INSERT INTO contacts (id, first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?, ?)",
                      (contact_id, post_data.get('first_name'), post_data.get('last_name'), post_data.get('email'), post_data.get('phone_number')))
            insert_changelog_entry('CREATE', contact_id)

            response_object['message'] = 'Contact added!'
        else:
            contacts = db.fetch_all("SELECT * FROM contacts", set_row_factory=True)
            response_object['contacts'] = [dict(contact) for contact in contacts]
    except Exception as e:
        response_object = {'status': 'error', 'message': str(e)}
    return jsonify(response_object)


@app.route('/contacts/<contact_id>', methods=['PUT', 'DELETE'])
def single_contact(contact_id):
    try:
        response_object = {'status': 'success'}

        if request.method == 'PUT':
            post_data = request.get_json()
            db.execute_query("UPDATE contacts SET first_name=?, last_name=?, email=?, phone_number=? WHERE id=?",
                      (post_data.get('first_name'), post_data.get('last_name'), post_data.get('email'), post_data.get('phone_number'), contact_id))
            insert_changelog_entry('UPDATE', contact_id)
            response_object['message'] = 'Contact updated!'
        if request.method == 'DELETE':
            db.execute_query("DELETE FROM contacts WHERE id=?", (contact_id,))
            insert_changelog_entry('DELETE', contact_id)
            response_object['message'] = 'Contact removed!'
    except Exception as e:
        response_object = {'status': 'error', 'message': str(e)}
    return jsonify(response_object)


@app.route('/changelog/<contact_id>', methods=['GET'])
def single_changelog(contact_id):
    try:
        response_object = {'status': 'success'}

        changelogs = db.fetch_all("SELECT * FROM changelog WHERE contact_id=? ORDER BY created_at DESC LIMIT 10", (contact_id,), set_row_factory=True)

        response_object['changelog'] = [dict(change) for change in changelogs]
    except Exception as e:
        response_object = {'status': 'error', 'message': str(e)}
    return jsonify(response_object)


def insert_changelog_entry(action, contact_id):
    changelog_id = uuid.uuid4().hex
    db.execute_query("INSERT INTO CHANGELOG (id, contact_id, action, description) VALUES (?, ?, ?, ?)",
                     (changelog_id, contact_id, action, f'{action.capitalize()} contact with ID: {contact_id}'))


if __name__ == '__main__':
    app.run()
