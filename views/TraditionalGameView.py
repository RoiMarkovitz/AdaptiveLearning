from secrets import randbelow
from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image
from pygame import mixer

from models.AdaptiveLearning import AdaptiveLearning
from utils.Constants import Constants
from utils.Exceptions import AnswerTimeTooFast, InvalidAnswer
from views.BaseView import BaseView
from views.custom_widgets.DataLabel import DataLabel
from views.custom_widgets.PrimaryButton import PrimaryButton
from views.custom_widgets.TopicLabel import TopicLabel


class TraditionalGameView(BaseView):

    def __init__(self, root, game_turn_details, is_quiz, main_menu_frame):
        self.root = root
        self.main_menu_frame = main_menu_frame
        self.is_quiz = is_quiz
        if is_quiz:
            self.root.title('מבדק סיווג רמות לימוד')
            self.exercise = game_turn_details
        else:
            self.root.title('סגנון למידה מסורתי')
            mixer.init()
            self.exercise = game_turn_details[1]
            self.time_to_answer = game_turn_details[2]
            self.current_time_to_answer = game_turn_details[2]
            self.points = game_turn_details[3]
            self.timer_on = True

        self.__init_widgets()

    def __check_answer(self):
        adaptive_learning = AdaptiveLearning.get_instance()
        answer = self.answer.get()
        self.answer_entry.delete(0, END)
        if self.is_quiz:
            try:
                self.exercise = adaptive_learning.answer_and_get_next_exercise_quiz(answer)
            except Exception as e:
                self.activate_text_error(e)
                self.root.after(3000, self.deactivate_text)
                return
            if self.exercise:  # present new exercise
                self.__update_widgets()
            else:  # quiz is finished
                self.__show_main_menu()
        else:  # regular game
            try:
                answer_time = self.time_to_answer - self.current_time_to_answer
                success = adaptive_learning.answer_game_turn(answer, answer_time)
            except Exception as e:
                class_name = e.__class__.__name__
                if class_name == InvalidAnswer.__name__:
                    self.activate_text_error(e)
                    self.root.after(3000, self.deactivate_text)
                    return
                elif class_name == AnswerTimeTooFast.__name__:
                    reply = messagebox.askquestion("זמן מענה מהיר מידי", e)
                    if reply == 'yes':
                        success = adaptive_learning.answer_game_turn(answer)
                    else:
                        return

            self.timer_on = False
            self.button_answer['state'] = 'disabled'
            if success:
                feedback_text = Constants.CORRECT_ANSWER_FEEDBACK_LIST[
                    randbelow(len(Constants.CORRECT_ANSWER_FEEDBACK_LIST))]
                feedback_sound_path = Constants.CORRECT_ANSWER_SOUND_PATH_LIST[
                    randbelow(len(Constants.CORRECT_ANSWER_SOUND_PATH_LIST))]
                feedback_sound = mixer.Sound(feedback_sound_path)
            else:
                feedback_text = Constants.INCORRECT_ANSWER_FEEDBACK_LIST[
                    randbelow(len(Constants.INCORRECT_ANSWER_FEEDBACK_LIST))]
                feedback_text = feedback_text + '\n' + 'התשובה הנכונה היא ' + str(self.exercise['solution'])
                feedback_sound_path = Constants.INCORRECT_ANSWER_SOUND_PATH_LIST[
                    randbelow(len(Constants.INCORRECT_ANSWER_SOUND_PATH_LIST))]
                feedback_sound = mixer.Sound(feedback_sound_path)

            self.activate_text_error(feedback_text)
            feedback_sound.play()
            self.root.after(3000, self.__next_turn)

    def __next_turn(self):
        self.deactivate_text()
        game_turn_details = AdaptiveLearning.get_instance().get_game_turn()
        if game_turn_details is None:
            self.__show_main_menu()
        else:
            self.exercise = game_turn_details[1]
            self.time_to_answer = game_turn_details[2]
            self.current_time_to_answer = game_turn_details[2]
            self.points = game_turn_details[3]
            self.__update_widgets()
            self.deactivate_text()
            self.button_answer['state'] = 'normal'
            self.timer_on = True
            self.__run_timer()

    def __show_main_menu(self):
        self.root.title('ראשי')
        self.main_menu_frame.pack(fill='both', expand=1)
        self.win_frame.pack_forget()

    def __run_timer(self):
        if not self.timer_on:
            return
        if self.current_time_to_answer == 0:
            self.button_answer['state'] = 'disabled'
            mixer.Sound(Constants.BUZZER_SOUND_PATH).play()
            AdaptiveLearning.get_instance().answer_game_turn()
            self.__next_turn()
            return

        self.current_time_to_answer -= 1
        self.__update_timer_label()
        if self.timer_on:
            self.root.after(1000, self.__run_timer)

    def __update_widgets(self):
        self.__update_topic_label()
        self.__update_exercise_label()
        if not self.is_quiz:
            self.__update_timer_label()
            self.__update_points_label()

    def __update_topic_label(self):
        topic_text = Constants.DIFFICULTY_ENGLISH_TO_HEBREW_DICT[self.exercise['difficulty']]
        if self.exercise['difficulty'] == 'intermediate':
            topic_text = 'שאלה ברמת ' + topic_text
        else:
            topic_text = 'שאלה ברמה ' + topic_text
        self.topic_label['text'] = topic_text

    def __update_exercise_label(self):
        if self.exercise['format'] == 'equation':
            numbers = self.exercise['question']
            exercise_text = f"{numbers[0]} {Constants.OPERATOR_DICT[self.exercise['type']]} {numbers[1]}"
            self.exercise_label['font'] = ('Ariel', 60, 'bold')
        else:
            exercise_text = self.exercise['question']
            self.exercise_label['font'] = ('Ariel', 24)
            sentences = exercise_text.split('. ')
            exercise_text = ""
            for index, sentence in enumerate(sentences):
                if index < len(sentences) - 1:
                    exercise_text += "." + sentence + "\n\n"
                else:
                    exercise_text += "?" + sentence

        self.exercise_label['text'] = exercise_text

    def __update_timer_label(self):
        self.time_count_label['text'] = self.current_time_to_answer

    def __update_points_label(self):
        self.points_count_label['text'] = self.points

    def __init_widgets(self):
        self.win_frame = Frame(self.root, bg=Constants.BG_COLOR)
        self.win_frame.pack(fill='both', expand=1)

        self.topic_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.topic_frame.place(anchor='n', relx=0.5, rely=0.0)

        self.timer_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.timer_frame.place(anchor='n', relx=0.03, rely=0.0)

        self.points_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.points_frame.place(anchor='n', relx=0.97, rely=0.0)

        self.exercise_frame = Frame(self.win_frame, bg=Constants.BG_COLOR, highlightthickness=3, highlightbackground="black",
                                    highlightcolor='black')
        self.exercise_frame.place(anchor='n', relx=0.5, rely=0.15)

        self.buttons_frame = Frame(self.win_frame, bg=Constants.BG_COLOR)
        self.buttons_frame.place(anchor='n', relx=0.5, rely=0.7)

        self.error_frame = Frame(self.win_frame, bg=Constants.BG_COLOR, highlightbackground="black")
        self.error_frame.place(anchor='s', relx=0.5, rely=0.9)

        self.topic_label = TopicLabel(self.topic_frame, '').get_label()
        self.topic_label.pack()
        self.__update_topic_label()

        if not self.is_quiz:
            # create an object of tkinter ImageTk
            self.timer_image = ImageTk.PhotoImage(Image.open(Constants.TIMER_IMG_PATH))
            time_image_label = Label(self.timer_frame, image=self.timer_image, bg=Constants.BG_COLOR)
            time_image_label.pack()

            self.time_count_label = DataLabel(self.timer_frame, self.current_time_to_answer, 'white', 'bold',
                                              20).get_data_label()
            self.time_count_label.pack()

            self.points_image = ImageTk.PhotoImage(Image.open(Constants.POINTS_IMG_PATH))
            points_image_label = Label(self.points_frame, image=self.points_image, bg=Constants.BG_COLOR)
            points_image_label.pack()

            self.points_count_label = DataLabel(self.points_frame, self.points, 'white', 'bold', 20).get_data_label()
            self.points_count_label.pack()

        self.exercise_label = DataLabel(self.exercise_frame, '').get_data_label()
        self.exercise_label.config(wraplength=900, justify='right')
        self.exercise_label.pack(pady=30)
        self.__update_exercise_label()

        # define stringVar for answer input
        self.answer = StringVar(self.exercise_frame)
        # create entry widget for answer, attach it to screen and bind mouse left click to it
        self.answer_entry = Entry(self.exercise_frame, textvariable=self.answer,
                                  width=5, font=('Ariel', 18))
        self.answer_entry.bind("<Button-1>", self.clear_text)
        self.answer_entry.pack(pady=20)

        self.button_answer = PrimaryButton(self.buttons_frame, "בדוק תשובה", 'white', 15,
                                           self.__check_answer).get_button()
        self.button_answer.pack()

        self.label_error = Label(self.error_frame, text="", wraplength=600, justify="right", fg=Constants.ERROR_COLOR,
                                 bg=Constants.BG_COLOR, font=('Ariel', 18, 'bold'))
        self.label_error.pack()

        if not self.is_quiz:
            self.__run_timer()
