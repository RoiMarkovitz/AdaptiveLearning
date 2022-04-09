from views.ModernGameView import ModernGameView
from views.TraditionalGameView import *
from views.custom_widgets.PrimaryButton import PrimaryButton
from views.custom_widgets.TopicLabel import TopicLabel


class MainMenuView(BaseView):

    def __init__(self, root):
        self.root = root
        self.root.title('ראשי')
        self.__init_widgets()

    def __play(self):
        adaptive_learning = AdaptiveLearning.get_instance()
        try:
            game_turn_details = adaptive_learning.get_game_turn()
        except Exception as e:
            self.activate_text_error(e)
            return

        self.win_frame.pack_forget()
        if game_turn_details[0] == 'traditional':
            TraditionalGameView(self.root, game_turn_details, False, self.win_frame)
        else:
            ModernGameView(self.root, game_turn_details, self.win_frame)

    def get_win_frame(self):
        return self.win_frame

    def __init_widgets(self):
        self.win_frame = Frame(self.root, bg=Constants.BG_COLOR)
        self.win_frame.pack(fill='both', expand=1)

        self.topic_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.topic_frame.place(anchor='n', relx=0.5, rely=0.0)

        self.buttons_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.buttons_frame.place(anchor='center', relx=0.5, rely=0.5)

        self.error_frame = Frame(self.win_frame, bg=Constants.BG_COLOR, highlightbackground="black")
        self.error_frame.place(anchor='s', relx=0.5, rely=0.85)

        topic_label = TopicLabel(self.topic_frame, "Math Expert").get_label()
        topic_label.pack()

        button_play = PrimaryButton(self.buttons_frame, "משחק", 'white', 15, self.__play).get_button()
        button_play.pack(pady=20)
        button_exit = PrimaryButton(self.buttons_frame, "יציאה", 'white', 15, self.root.destroy).get_button()
        button_exit.pack(pady=20)

        self.label_error = Label(self.error_frame, text="", wraplength=800, justify="right", fg=Constants.ERROR_COLOR,
                                 bg=Constants.BG_COLOR, font=('Ariel', 18, 'bold'))
        self.label_error.pack()
