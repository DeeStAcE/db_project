from psycopg2 import connect, OperationalError, sql
from psycopg2.errors import DuplicateDatabase, DuplicateTable

create_db_query = sql.SQL('''
    CREATE DATABASE {database_name};
''').format(database_name=sql.Identifier('database_'))

query_create_table_user = sql.SQL('''
    CREATE TABLE {table_name} (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    hashed_password VARCHAR(80)
    );
''').format(table_name=sql.Identifier('User'))

query_create_table_message = sql.SQL('''
    CREATE TABLE {table_name} (
    id SERIAL PRIMARY KEY,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text VARCHAR(255),
    from_id INT,
    to_id INT,
    FOREIGN KEY (from_id) REFERENCES {table_ref}(id),
    FOREIGN KEY (to_id) REFERENCES {table_ref}(id)
    );
''').format(table_name=sql.Identifier('Message'), table_ref=sql.Identifier('User'))

try:
    cnx = connect(user='postgres', password='coderslab', host='localhost', port=5432, database='database_')
    cnx.autocommit = True
    cursor = cnx.cursor()
    print('CONNECTED')
except OperationalError as error:
    print('CONNECTION ERROR')
    raise ValueError(f'Connection error: {error}')

try:
    cursor.execute(create_db_query)
except DuplicateDatabase as error:
    print('DATABASE EXISTS')

try:
    cursor.execute(query_create_table_user)
except DuplicateTable as error:
    print('TABLE USER ALREADY EXISTS')

try:
    cursor.execute(query_create_table_message)
except DuplicateTable as error:
    print('TABLE MESSAGE ALREADY EXISTS')

cnx.close()
