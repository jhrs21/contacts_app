import sys
import sqlite3
import uuid
import random
import string

DB_FILE = 'app.db'


# Function to generate random phone numbers
def generate_phone_number():
    return ''.join(random.choices(string.digits, k=10))


# Function to create database and table, and optionally insert data
def create_database_and_table(insert_data=False):
    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create CONTACTS table
    c.execute("""
        CREATE TABLE IF NOT EXISTS CONTACTS (
            id TEXT PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT NOT NULL)
            """)

    # Create CHANGELOG table
    c.execute("""
        CREATE TABLE IF NOT EXISTS CHANGELOG (
            id TEXT PRIMARY KEY NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            contact_id TEXT NOT NULL,
            action TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES CONTACTS(id))
            """)

    # Commit changes (creating table)
    conn.commit()

    # Insert data if requested
    if insert_data:
        # Generate sample data for insertion
        sample_data_contacts = [
            ('John', 'Doe', 'john@example.com', generate_phone_number()),
            ('Jane', 'Smith', 'jane@example.com', generate_phone_number()),
            ('Michael', 'Johnson', 'michael@example.com', generate_phone_number()),
            ('Emily', 'Brown', 'emily@example.com', generate_phone_number())
        ]

        # Insert sample data into CONTACTS table
        for data in sample_data_contacts:
            contact_id = uuid.uuid4().hex
            changelog_id = uuid.uuid4().hex
            first_name, last_name, email, phone_number = data
            c.execute("INSERT INTO CONTACTS (id, first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?, ?)",
                      (contact_id, first_name, last_name, email, phone_number))
            c.execute("INSERT INTO CHANGELOG (id, contact_id, action, description) VALUES (?, ?, ?, ?)",
                      (changelog_id, contact_id, 'CREATE', 'Init DB'))

        # Commit changes (inserting data)
        conn.commit()

    # Close connection
    conn.close()

    print(f"Database '{DB_FILE}' created successfully with the CONTACTS and CHANGELOG tables.")


def clean_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM CONTACTS")
    c.execute("DELETE FROM CHANGELOG")
    conn.commit()
    conn.close()
    print("Tables CONTACTS and CHANGELOG cleaned.")


if __name__ == "__main__":
    # Check if "data" argument is passed to execute inserts
    if len(sys.argv) > 1 and sys.argv[1] == "data":
        create_database_and_table(insert_data=True)
    elif len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_data()
    else:
        create_database_and_table()