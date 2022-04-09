from tkinter import *

from models.AdaptiveLearning import AdaptiveLearning
from utils.Constants import Constants
from views.BaseView import BaseView
from views.MainMenuView import MainMenuView
from views.TraditionalGameView import TraditionalGameView
from views.custom_widgets.DataLabel import DataLabel
from views.custom_widgets.PrimaryButton import PrimaryButton
from views.custom_widgets.TopicLabel import TopicLabel


class QuestionnaireView(BaseView):

    def __init__(self, root, questionnaire):
        self.root = root
        self.root.title('שאלון התאמת סגנונות לימוד')
        self.questionnaire = questionnaire

        self.__init_widgets()

    def __submit(self):
        choices = []
        for option in self.selected_options:
            choices.append(option.get())

        exercise = AdaptiveLearning.get_instance().finish_questionnaire(choices)
        self.win_frame.pack_forget()
        main_menu = MainMenuView(self.root)
        main_menu_frame = main_menu.get_win_frame()
        main_menu_frame.pack_forget()
        TraditionalGameView(self.root, exercise, True, main_menu_frame)

    def __init_widgets(self):
        self.win_frame = Frame(self.root, bg=Constants.BG_COLOR)
        self.win_frame.pack(fill='both', expand=1)

        self.topic_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.topic_frame.place(anchor='n', relx=0.5, rely=0.0)

        self.questions_frame = Frame(self.win_frame, bg=Constants.BG_COLOR, highlightbackground="black", highlightthickness=5)
        self.questions_frame.place(anchor='center', relx=0.5, rely=0.5)

        self.buttons_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.buttons_frame.place(anchor='s', relx=0.5, rely=0.9)

        topic_label = TopicLabel(self.topic_frame, "שאלון סגנונות לימוד").get_label()
        topic_label.pack()

        header_list = ['מעט מאוד', 'מעט', 'ככה ככה', 'הרבה', 'הרבה מאוד']
        for i in range(len(header_list)):
            header = DataLabel(self.questions_frame, header_list[i], 'white', 'bold').get_data_label()
            header.grid(row=0, column=i, padx=5, pady=10)

        self.selected_options = []
        for i, doc in enumerate(self.questionnaire):
            question = DataLabel(self.questions_frame, doc['question'], 'white').get_data_label()
            question.grid(row=i + 1, column=5, padx=5, pady=10, sticky=E)
            self.selected_options.append(IntVar())
            for j in range(Constants.MAX_CHOICE_PER_QUESTION_QUESTIONNAIRE):
                radio_button = Radiobutton(self.questions_frame, fg='red', activeforeground='red',
                                           bg=Constants.BG_COLOR, activebackground=Constants.BG_COLOR,
                                           variable=self.selected_options[i], value=j + 1)
                if j == 2:
                    radio_button.select()
                radio_button.grid(row=i + 1, column=j, padx=5, pady=10)

        button_play = PrimaryButton(self.buttons_frame, "שלח שאלון", 'white', 15, self.__submit).get_button()
        button_play.pack()
