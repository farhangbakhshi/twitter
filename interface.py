from core import Core

class Interface:
    core:Core = None
    menus = {
        "welcome_menu": ["1. sign up","2. log in", "3. quit"]
    }

    def __init__(self, core):
        self.core = core

    def show_menu(self, menu_type):
        for x in self.menus[menu_type]:
            print(x)
        user_choice = input("? ")
        return user_choice

    def welcome(self):
        while True:
            user_choice = self.show_menu("welcome_menu")
            if user_choice == 0:
                self.core.wrap_up()
                quit()
            elif user_choice == 1:
                if self.sign_up():
                    print("WELCOME!")
                    self.start()
                else:
                    print("sign up failed!")
                    continue
            elif user_choice == 2:
                if self.login():
                    print("WELCOME!")
                    self.start()
                else:
                    print("login failed!")
                    continue
    
    def sign_up(self):
        username = input("enter your handle below.\n")
        password = input("enter your password below.\n")
        name = input("enter your name below.\n")
        bio = input("enter your bio below.\n")
        return self.core.new_user(username, password, name, bio)
