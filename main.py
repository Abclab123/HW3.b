import bcrypt
import streamlit as st
from UI_module import StorytellingAppBase
from UI_search import UI_search
from ai import OpenAIGenerator, ImageGenerator

salt = bcrypt.gensalt()

# We don't have a server for now, so we don't have a database.
# We maintain the following list instead.
valid_users = [
    {
        "name": "test",
        "password": bcrypt.hashpw(bytes("password123", "utf-8"), salt),
        "group": "user",
    },
    {
        "name": "admin",
        "password": bcrypt.hashpw(bytes("password123", "utf-8"), salt),
        "group": "admin",
    },
]


class StorytellingApp(StorytellingAppBase):
    # Implement the methods to create text and image to display
    # You can also add any other methods that you may need
    def __init__(self, _text_generator=None, _image_generator=None):
        # Call the base class constructor
        super().__init__(_text_generator, _image_generator)

    def create_image_to_display(self, image):
        # Implement the logic to process and return text for display

        # image = self.image_generator.generate_image(prompt, output_file_id)
        # return image

        return "https://via.placeholder.com/300"

    def create_text_to_display(self, text):
        # Implement the logic to create and return an image for display

        # text = self.text_generator.generate(user_input, self.user_history)
        # return text
        return "Open ai genetrated text "


class UI_login:
    def __init__(self):
        pass

    def login(self, usr: str, pwd: str) -> tuple[bool, int, str]:
        for user in valid_users:
            if user["name"] == usr:
                if user["password"] == bcrypt.hashpw(bytes(pwd, "utf-8"), salt):
                    return True, 200, "Login Successfully."
                else:
                    return False, 401, "Wrong Password."
        return False, 404, "User Does Not Exist."

    def signup(self, usr: str, pwd: str):
        for user in valid_users:
            if user["name"] == usr:
                return False, 403, "User Already Exist."

        valid_users.append(
            {
                "name": usr,
                "password": bcrypt.hashpw(bytes(pwd, "utf-8"), salt),
                "group": "user",
            }
        )
        return True, 200, "Signup Successfully."

    def signup_page(self):
        st.title("Please Signup")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        signup_button = st.button("Submit")

        if signup_button:
            if username == "":
                st.error("Username is equired.")
                return
            elif password == "":
                st.error("Password is equired.")
                return
            else:
                res = self.signup(username, password)
                res_code = res[1]
                res_msg = res[2]

                if res_code == 200:
                    st.success(res_msg)
                    st.session_state.page = "Welcome"
                    st.rerun()
                elif res_code == 401 or res_code == 404:
                    st.error(res_msg)
                else:
                    st.error("Please Signup")

    def login_page(self):
        st.title("BDS HW3b")
        st.write("Group 14")
        st.write("Welcome to our page. Please Sign Up or Login.")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        st.write("Don't have an account?")
        signup_button = st.button("Signup")

        if login_button:
            if username == "":
                st.error("Username is equired.")
                return
            elif password == "":
                st.error("Password is equired.")
                return
            else:
                res = self.login(username, password)
                res_code = res[1]
                res_msg = res[2]

                if res_code == 200:
                    st.session_state.page = "Welcome"
                    st.rerun()
                elif res_code == 401 or res_code == 404:
                    st.error(res_msg)
                else:
                    st.error("Please Login")

        elif signup_button:
            st.session_state.page = "Signup"
            st.rerun()

    def welcome_page(self):
        st.title("Welcome!")
        st.write("Welcome to our page.")
        gen_button = st.button("gen")
        search_button = st.button("search")
        if gen_button:
            st.session_state.page = "Gen"
            st.rerun()
        elif search_button:
            st.session_state.page = "Search"
            st.rerun()

    def gen_page(self):
        st.title("Gen")
        app = StorytellingApp(
            _text_generator=OpenAIGenerator("OpenAI API Key"),
            _image_generator=ImageGenerator("CompVis/stable-diffusion-v1-4", True),
        )
        app.run()

    def search_page(self):
        st.title("Search")
        ui = UI_search()
        ui.UI()

    def show(self):
        if "page" not in st.session_state:
            st.session_state.page = "Login"

        if st.session_state.page == "Login":
            self.login_page()
        elif st.session_state.page == "Welcome":
            self.welcome_page()
        elif st.session_state.page == "Gen":
            self.gen_page()
        elif st.session_state.page == "Search":
            self.search_page()
        else:
            self.signup_page()


if __name__ == "__main__":
    UI_login().show()
