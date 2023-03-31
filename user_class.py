from password_app import hash_password
from psycopg2 import sql


class User:
    def __init__(self, username='', password='', salt=''):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, new_password):
        self.set_password(new_password)

    def save_to_db(self, cursor):
        if self._id == -1:
            query = sql.SQL('''
                INSERT INTO {table_name} (username, hashed_password)
                VALUES (%s, %s);
            ''').format(table_name=sql.Identifier('User'))
            cursor.execute(query, (self.username, self.hashed_password))
            # self._id = cursor.fetchone()['id']
            return True
        else:
            query = sql.SQL('''
                UPDATE {table_name} SET username=%s, hashed_password=%s
                WHERE id = %s;
            ''').format(table_name=sql.Identifier('User'))
            cursor.execute(query, (self.username, self.hashed_password, self._id))
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        query = sql.SQL('''
            SELECT id, username, hashed_password
            FROM {table_name}
            WHERE id = %s;
        ''').format(table_name=sql.Identifier('User'))
        cursor.execute(query, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
        return loaded_user

    @staticmethod
    def load_user_by_username(cursor, username_):
        query = sql.SQL('''
               SELECT id, username, hashed_password
               FROM {table_name}
               WHERE username = %s;
           ''').format(table_name=sql.Identifier('User'))
        cursor.execute(query, (username_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
        return loaded_user

    @staticmethod
    def load_all_users(cursor):
        query = sql.SQL('''
            SELECT id, username, hashed_password
            FROM {table_name};
        ''').format(table_name=sql.Identifier('User'))
        users = []
        cursor.execute(query)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        query = sql.SQL('''
            DELETE
            FROM {table_name}
            WHERE id = %s;
        ''').format(table_name=sql.Identifier('User'))
        cursor.execute(query, (self._id,))
        self._id = -1
        return True
