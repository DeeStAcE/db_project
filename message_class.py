from psycopg2 import sql


class Message:
    def __init__(self, from_id, to_id, text='empty text'):
        self._id = -1
        self.text = text
        self.to_id = to_id
        self.from_id = from_id
        self.creation_data = None

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            query = sql.SQL('''
                  INSERT INTO {table_name} (from_id, to_id, text, creation_date)
                  VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
              ''').format(table_name=sql.Identifier('Message'))
            cursor.execute(query, (self.from_id, self.to_id, self.text))
            # self._id = cursor.fetchone()['id']
            return True
        else:
            query = sql.SQL('''
                  UPDATE {table_name} SET from_id=%s, to_id=%s, text=%s
                  WHERE id = %s;
              ''').format(table_name=sql.Identifier('Message'))
            cursor.execute(query, (self.from_id, self.to_id, self.text, self._id))
            return True

    @staticmethod
    def load_all_messages(cursor):
        query = sql.SQL('''
                SELECT id, text, from_id, to_id, creation_date
                FROM {table_name};
            ''').format(table_name=sql.Identifier('Message'))
        messages = []
        cursor.execute(query)
        for row in cursor.fetchall():
            id_, text, from_id, to_id, creation_data = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message.creation_data = creation_data
            messages.append(loaded_message)
        return messages
