import kivy
from kivy.clock import Clock
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from datetime import date
import time

Builder.load_file('design.kv')
        
class MainApp(App):
    def build(self):
        return RootWidget()

class LoginScreen(Screen):
    
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def  login(self, uname, pword):
        with open('users.json') as file:
            users=json.load(file)
        if uname in users and users[uname]['password'] == pword:
            global current_user
            current_user = uname
            self.manager.current='dashboard_screen'
        else:
            self.ids.login_wrong.text='Wrong username or password'

class SignUpScreen(Screen):

    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        #if len(uname) < 6:
            #self.ids.username_creation_response.text='Username must be at least 6 characters long'
        if uname in users:
            self.ids.username_creation_response.text='That username is already taken'
        #elif len(pword) < 6:
            #self.ids.username_creation_response.text='Password must be at least 6 characters long'
        else:
            users[uname] = {'username': uname, 'password': pword,
            'created': datetime.now().strftime("%Y-%M-%D %H-%M-%S")}
            with open("users.json", 'w') as file:
                json.dump(users, file)

            with open ('entries.json', 'r+') as entry_file:
                entries = json.load(entry_file)
            entries[uname] = []
            with open ('entries.json', 'w') as entry_file:
                json.dump(entries, entry_file)

            self.manager.current="sign_up_success"

    def go_to_login_screen(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"

class SignUpSuccess(Screen):

    def go_to_login_screen(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"

class DashboardScreen(Screen):

    def on_start(self, *args):
        global start_time
        start_time=int(time.time())
        self.function_interval = Clock.schedule_interval(self.update_label, 1)

    def update_label(self, t):

        def time_convert(sec):
            mins = sec // 60
            sec = sec % 60
            hours = mins // 60
            mins = mins % 60
            return("{0}:{1}:{2}".format(int(hours),int(mins),sec))
        
        global time_elapsed
        time_elapsed=time_convert(int(time.time()-start_time))
        self.ids.elapsed_time.text=str(time_elapsed)

# definition updated

    def on_stop(self, description, time):
        current_date = str(date.today())
        self.function_interval.cancel()
        self.ids.elapsed_time.text="0:0:0"
        with open ('entries.json', 'r+') as file:
            entries = json.load(file)

        b=False
        for i in entries[current_user]:
            if current_date in i:
                b=True
                
        if b == True:
            a = [a for a,d in enumerate(entries[current_user]) if current_date in d]
            entries[current_user][a[0]][current_date][description]=time
        else:
            entries[current_user].append({current_date:{description:time}})

        with open ('entries.json', 'r+') as file:
            json.dump(entries, file)

    def go_to_login_screen(self):
        global current_user
        current_user = None
        self.manager.transition.direction="right"
        self.manager.current="login_screen"

class RootWidget(ScreenManager):
    pass

if __name__ == "__main__":
    MainApp().run()