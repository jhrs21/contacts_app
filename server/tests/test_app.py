import pytest

from server.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_ping_pong(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data.decode() == '"pong!"\n'


def test_insert_contact(client):
    new_contact_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john_test@example.com',
        'phone_number': '1234567890'
    }
    new_contact_id = ''
    try:
        post_response = client.post('/contacts', json=new_contact_data)
        assert post_response.status_code == 200
        assert post_response.json['status'] == 'success'
        assert post_response.json['message'] == 'Contact added!'
        new_contact_id = post_response.json['contact_id']

        get_response = client.get('/contacts')
        assert get_response.status_code == 200
        assert new_contact_id in [item.get('id', '') for item in get_response.json['contacts']]

    finally:
        # Remove the contact after the test completes (cleanup)
        delete_response = client.delete(f"/contacts/{new_contact_id}")
        assert delete_response.status_code == 200


def test_update_contact(client):
    new_contact_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john_test@example.com',
        'phone_number': '1234567890'
    }
    new_contact_id = ''
    try:
        post_response = client.post('/contacts', json=new_contact_data)
        assert post_response.status_code == 200
        assert post_response.json['status'] == 'success'
        assert post_response.json['message'] == 'Contact added!'
        new_contact_id = post_response.json['contact_id']

        new_contact_data['last_name'] = 'Test'
        put_response = client.put(f'/contacts/{new_contact_id}', json=new_contact_data)
        assert put_response.status_code == 200

        get_response = client.get('/contacts')
        assert get_response.status_code == 200
        assert (new_contact_id, 'Test') in [(item.get('id', ''), item.get('last_name', '')) for item in get_response.json['contacts']]

    finally:
        # Remove the contact after the test completes (cleanup)
        delete_response = client.delete(f"/contacts/{new_contact_id}")
        assert delete_response.status_code == 200


def test_all_contacts(client):
    get_response = client.get('/contacts')
    assert get_response.status_code == 200
    assert isinstance(get_response.json['contacts'], list)

    for contact in get_response.json['contacts']:
        assert 'id' in contact
        assert 'first_name' in contact
        assert 'last_name' in contact
        assert 'email' in contact
        assert 'phone_number' in contact
