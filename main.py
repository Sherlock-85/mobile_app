from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random
from _datetime import datetime
from pathlib import Path

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, usname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if usname in users and users[usname]["password"] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.incorrect_login.text = "Incorrect username or password."

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, usname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[usname] = {"username": usname, "password": pword,
                        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", "w") as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def return_home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, emotion):
        emotion = emotion.lower()
        available_emotions = glob.glob("quotes/*txt")

        available_emotions = [Path(filename).stem for filename in
                              available_emotions]
        if emotion in available_emotions:
            with open(f"quotes/{emotion}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)

class ImageButton(ButtonBehavior,HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()


