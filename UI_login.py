import psycopg2
import streamlit
import string
import random
import hashlib


class UI_login:
    def __init__(self):
        self.db = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='bdshw3',
            host='ws3.csie.ntu.edu.tw',
            port='5433')


    def __login(self, username, password) -> bool:
        sql = f'''SELECT * FROM users
                  WHERE username = %s;'''

        # check db connection
        try:
            with self.db.cursor() as cur:
                cur.execute('SELECT 1;')
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.db = psycopg2.connect(
                database='postgres',
                user='postgres',
                password='bdshw3',
                host='ws3.csie.ntu.edu.tw',
                port='5433')

        # get data
        with self.db.cursor() as cur:
            cur.execute(sql, (username,))
            f2i = {desc[0]: i for i, desc in enumerate(cur.description)}
            row = cur.fetchone()

            if row is None:
                # user doesn't exist
                return False

        salt = row[f2i['password_salt']]
        db_hash = row[f2i['password_hash']]

        # check validity
        password += salt
        my_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if my_hash != db_hash:
            return False

        return True


    def __signup(self, username, password) -> bool:
        sql = f'''INSERT INTO users (
                      username, password_salt, password_hash)
                  VALUES (%s, %s, %s);'''

        # check db connection
        try:
            with self.db.cursor() as cur:
                cur.execute('SELECT 1;')
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.db = psycopg2.connect(
                database='postgres',
                user='postgres',
                password='bdshw3',
                host='ws3.csie.ntu.edu.tw',
                port='5433')

        # insert data
        salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        password += salt
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        with self.db.cursor() as cur:
            try:
                cur.execute(sql, (username, salt, password_hash))
                self.db.commit()
            except psycopg2.errors.UniqueViolation:
                return False

        return True


    def UI(self):
        pass
