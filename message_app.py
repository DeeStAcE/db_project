import argparse

from message_class import Message
from user_class import User
from password_app import check_password

from psycopg2.errors import UniqueViolation, OperationalError
from psycopg2 import connect

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min. 8 characters)")
parser.add_argument("-t", "--to", help="who send a message to")
parser.add_argument("-s", "--send", help="message to send")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")

args = parser.parse_args()


def list_messages(cursor_, username, password):
    user = User(username, password)
    if not user:
        print('User does not exist')
    else:
        if not check_password(password, user.hashed_password):
            print('Incorrect password')
        else:
            messages_ = Message.load_all_messages(cursor_, user.id)
            for message_ in messages_:
                print(f'Addressee: {message_.to_id}, date: {message_.creation_data}, text:\n{message_.text}')


def send_message(cursor_, username, password, to_user, text):
    user = User(username, password)
    if not user:
        print('User does not exist')
    else:
        if not check_password(password, user.hashed_password):
            print('Incorrect password')
        else:
            user_to_send = User.load_user_by_id(cursor_, to_user)
            if user_to_send:
                if len(text) > 255:
                    print('Message is too long. It has to be below 255 characters')
                else:
                    message = Message(user.id, to_user, text)
                    message.save_to_db(cursor_)
            else:
                print('User can not receive a massage, because there is no such user')


if __name__ == '__main__':
    try:
        cnx = connect(user='postgres', password='coderslab', host='localhost', port=5432, database='database_')
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.to and args.send:
            send_message(cursor, args.username, args.password, args.to, args.send)
        elif args.username and args.password and args.list:
            list_messages(cursor, args.username, args.password)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as error_:
        print('Connection error: ', error_)
