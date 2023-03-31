from user_class import User
from message_class import Message
from psycopg2 import connect, OperationalError

try:
    cnx = connect(user='postgres', password='coderslab', host='localhost', port=5432, database='database_')
    cnx.autocommit = True
    cursor = cnx.cursor()
    print('CONNECTED')
except OperationalError as error:
    print('CONNECTION ERROR')
    raise ValueError(f'Connection error: {error}')

# user1 = User('Dawid', 'haslo654321')
# user1.save_to_db(cursor)
# user2 = User('Dawid', 'haslo123456')
# user2.save_to_db(cursor)

# print(User.load_all_users(cursor))

# user3 = User.load_user_by_id(cursor, 4)
# user3.delete(cursor)

# user4 = User.load_user_by_id(cursor, 7)
# user4.username = 'Ala'
# user4.save_to_db(cursor)


# text1 = Message(12, 13, 'witam kolege')
# text1.save_to_db(cursor)

# print(Message.load_all_messages(cursor))
