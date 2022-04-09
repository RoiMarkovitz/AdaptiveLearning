from tkinter import *

from utils.Constants import Constants
from views.BaseView import BaseView
from views.LoginView import LoginView
from views.RegistrationView import RegistrationView
from views.custom_widgets.PrimaryButton import PrimaryButton
from views.custom_widgets.TopicLabel import TopicLabel


class RegistrationLoginView(BaseView):

    def __init__(self, root):
        self.root = root
        self.__init_widgets()

    def __show_registration_view(self):
        self.win_frame.pack_forget()
        RegistrationView(self.root, self.win_frame)

    def __show_login_view(self):
        self.win_frame.pack_forget()
        LoginView(self.root, self.win_frame)

    def __init_widgets(self):
        self.win_frame = Frame(self.root, bg=Constants.BG_COLOR)
        self.win_frame.pack(fill='both', expand=1)

        self.topic_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.topic_frame.place(anchor='n', relx=0.5, rely=0.0)

        self.buttons_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.buttons_frame.place(anchor='center', relx=0.5, rely=0.5)

        topic_label = TopicLabel(self.topic_frame, "רישום/כניסה").get_label()
        topic_label.pack()

        button_registration = PrimaryButton(self.buttons_frame, "רישום משתמש חדש", 'white', 15,
                                            self.__show_registration_view).get_button()
        button_registration.pack(pady=20)
        button_login = PrimaryButton(self.buttons_frame, "כניסת משתמש קיים", 'white', 15,
                                     self.__show_login_view).get_button()
        button_login.pack(pady=20)
        button_exit = PrimaryButton(self.buttons_frame, "יציאה", 'white', 15, self.root.destroy).get_button()
        button_exit.pack(pady=20)

