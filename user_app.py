import argparse

from password_app import check_password
from user_class import User

from psycopg2.errors import UniqueViolation, OperationalError
from psycopg2 import connect

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min. 8 characters)")
parser.add_argument("-n", "--new-pass", help="new password (min. 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


def list_all_users(cursor_):
    users = User.load_all_users(cursor_)
    for user in users:
        print(user.username)


def create_user(cursor_, username, password):
    if len(password) < 8:
        print('Password is too short. It has to be min. 8 characters')
    else:
        try:
            user = User(username, password)
            user.save_to_db(cursor_)
            print('User created')
        except UniqueViolation as error_:
            print('User already exists ', error_)


def delete_user(cursor_, username, password):
    user = User.load_user_by_username(cursor_, username)
    if not user:
        print('User does not exist')
    elif not check_password(password, user.hashed_password):
        user.delete(cursor_)
        print(f'User {user.username} deleted')
    else:
        print('Incorrect password')


def edit_user(cursor_, username, password, new_pass):
    user = User(username, password)
    if not user:
        print('User does not exist')
    elif not check_password(password, user.hashed_password):
        print('Incorrect password')
    else:
        if len(new_pass) < 8:
            print('New password is too short. It has to be min. 8 characters')
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor_)
            print('Password changed')


if __name__ == '__main__':
    try:
        cnx = connect(user='postgres', password='coderslab', host='localhost', port=5432, database='database_')
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_all_users(cursor)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as error_:
        print('Connection error: ', error_)
