from tkinter import *

from models.AdaptiveLearning import AdaptiveLearning
from utils.Constants import Constants
from views.BaseView import BaseView
from views.MainMenuView import MainMenuView
from views.QuestionnaireView import QuestionnaireView
from views.TraditionalGameView import TraditionalGameView
from views.custom_widgets.DataLabel import DataLabel
from views.custom_widgets.PrimaryButton import PrimaryButton
from views.custom_widgets.TopicLabel import TopicLabel


class LoginView(BaseView):

    def __init__(self, root, registration_login_frame):
        self.root = root
        self.registration_login_frame = registration_login_frame
        self.root.title('כניסה')
        self.__init_widgets()

    def __login(self):
        adaptive_learning = AdaptiveLearning.get_instance()
        try:
            result = adaptive_learning.login_student(self.username_stringVar.get(), self.password_stringVar.get())
        except Exception as e:
            self.activate_text_error(e)
            return

        self.win_frame.pack_forget()
        main_menu = MainMenuView(self.root)
        main_menu_frame = main_menu.get_win_frame()
        main_menu_frame.pack_forget()
        if type(result) != bool and result.get('questionnaire'):
            QuestionnaireView(self.root, result['questionnaire'])
        elif type(result) != bool and result.get('exercise'):
            TraditionalGameView(self.root, result['exercise'], True, main_menu_frame)
        else:
            MainMenuView(self.root)

    def __show_registration_login_view(self):
        self.root.title('רישום/כניסה')
        self.registration_login_frame.pack(fill='both', expand=1)
        self.win_frame.pack_forget()

    def __init_widgets(self):
        self.win_frame = Frame(self.root, bg=Constants.BG_COLOR)
        self.win_frame.pack(fill='both', expand=1)

        self.topic_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.topic_frame.place(anchor='n', relx=0.5, rely=0.0)

        self.input_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.input_frame.place(anchor='center', relx=0.5, rely=0.28)

        self.buttons_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.buttons_frame.place(anchor='center', relx=0.5, rely=0.55)

        self.error_frame = Frame(self.win_frame, bg=Constants.BG_COLOR, highlightbackground="black")
        self.error_frame.place(anchor='s', relx=0.5, rely=0.85)

        topic_label = TopicLabel(self.topic_frame, "כניסה").get_label()
        topic_label.pack()

        username_label = DataLabel(self.input_frame, ':משתמש').get_data_label()
        username_label.grid(row=0, column=1, padx=5, pady=15, sticky=W)
        # define stringVar for username input
        self.username_stringVar = StringVar(self.buttons_frame)
        # create entry widget for username, attach it to screen and bind mouse left click to it
        username_entry = Entry(self.input_frame, textvariable=self.username_stringVar,
                               width=15, font=('Ariel', 18))
        username_entry.bind("<Button-1>", self.clear_text)
        username_entry.grid(row=0, column=0, pady=10, sticky=E)

        password_label = DataLabel(self.input_frame, ':סיסמא').get_data_label()
        password_label.grid(row=1, column=1, padx=5, pady=10, sticky=W)
        # define stringVar for password input
        self.password_stringVar = StringVar(self.buttons_frame)
        # create entry widget for password, attach it to screen and bind mouse left click to it
        password_entry = Entry(self.input_frame, textvariable=self.password_stringVar, show='*',
                               width=15, font=('Ariel', 18))
        password_entry.bind("<Button-1>", self.clear_text)
        password_entry.grid(row=1, column=0, pady=10, sticky=E)

        button_registration = PrimaryButton(self.buttons_frame, "כניסה", 'white', 15, self.__login).get_button()
        button_registration.grid(row=0, pady=20)
        button_return = PrimaryButton(self.buttons_frame, "חזור", 'white', 15,
                                      self.__show_registration_login_view).get_button()
        button_return.grid(row=1, pady=20)

        self.label_error = Label(self.error_frame, text="", wraplength=800, justify="right", fg=Constants.ERROR_COLOR,
                                 bg=Constants.BG_COLOR, font=('Ariel', 18, 'bold'))
        self.label_error.pack()

