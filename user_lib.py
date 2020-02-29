import pickle
import hashlib
import os.path
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, username, password, user_id, active=True):
        self.id = user_id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    # def get_auth_token(self):
    #     return self.make_secure_token(self.username, key='secret_key')


class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

        pickle_filename = 'users.pickle'
        if os.path.exists(pickle_filename):
            try:
                with open(pickle_filename, 'rb') as f:
                    self.users, self.users_id_dict = pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                print('Cannot write into object')  # logging this

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

        with open('users.pickle', 'wb') as f:
            try:
                pickle.dump((self.users, self.users_id_dict), f)
            except pickle.PicklingError:
                print('Error while reading from object. Object is not picklable')  # logging this

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, user_id):
        return self.users_id_dict.get(user_id)

    def next_index(self):
        self.identifier += 1
        return self.identifier
