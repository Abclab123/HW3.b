import psycopg2
import streamlit as st
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

    def welcome_page(self):
        st.title('Welcome')

        gen_button = st.button('Gen')
        search_button = st.button('Search')

        if gen_button:
            # maybe use method in login_page and UI?
            # set some variable in st.session_state
            # and rerun to go to ui gen
            pass

        elif search_button:
            pass

    def login_page(self):
        st.title('Login')

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        login_button = st.button('Login')
        signup_button = st.button('Signup')

        if login_button:
            if self.__login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.write('login failed')

        elif signup_button:
            if self.__signup(username, password):
                st.write('signup success')
            else:
                st.write('username exists')

    def UI(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        # decide which page to go
        if st.session_state.logged_in:
            self.welcome_page()
        else:
            self.login_page()


if __name__ == '__main__':
    UI_login().UI()
