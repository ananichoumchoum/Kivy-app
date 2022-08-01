from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
import glob, random, json
from pathlib import Path

Builder.load_file('design.kv')

class RootWidget(ScreenManager):
    pass
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"
    def login(self, username, password):
        with open("users.json") as file:
            users = json.load(file)
        if username in users and users[username]["password"] == password:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong Username and Password combination"
    def go_to_forget_password(self):
        self.manager.transition.direction = "left"
        self.manager.current = "forget_password"
class ForgetPassword(Screen):
    def find_user(self, username):
        with open("users.json") as file:
            users = json.load(file)
        if username in users:
            self.ids.get_password.text = users[username]["password"]
        else:
            self.ids.get_password.text = "No such username in the database"
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current ="login_screen"
class SignUpScreen(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current ="login_screen"
    def add_user(self, username, password):
        with open("users.json") as file:
            users = json.load(file)
        if username in users:
            self.ids.username_exist.text = "Username already exist"
        else:
            users[username]={"username":username, "password":password,
                "created":datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}
            with open("users.json", "w") as file:
                json.dump(users,file)
                self.manager.current= "sign_up_screen_success"
class SignUpScreenSucess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current ="login_screen"
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    def get_quote(self, feel):
        feel= feel.lower()
        available_feeling = glob.glob("quotes/*txt")
        available_feeling= [Path(filename).stem for filename in available_feeling]
        if feel in available_feeling:
            with open(f"quotes/{feel}.txt",encoding="utf8") as file:
                quotes1 = file.readlines()
            self.ids.quote.text =random.choice(quotes1)
        else:
            self.ids.quote.text = "Try another feeling. Available feelings are: angry, anxious, bored, depressed, happy, lonely, lost, sad, stressed, unloved"
class ImageButton(ButtonBehavior,Image, HoverBehavior):
    pass
class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
