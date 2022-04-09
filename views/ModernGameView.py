import random
from secrets import randbelow
from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image
from pygame import mixer

from models.AdaptiveLearning import AdaptiveLearning
from utils.Constants import Constants
from utils.Exceptions import AnswerTimeTooFast
from views.BaseView import BaseView
from views.custom_widgets.DataLabel import DataLabel
from views.custom_widgets.TopicLabel import TopicLabel


class ModernGameView(BaseView):
    __NUM_OPTIONAL_SOLUTIONS = 8

    def __init__(self, root, game_turn_details, main_menu_frame):
        self.root = root
        self.main_menu_frame = main_menu_frame
        self.root.title('סגנון למידה מודרני')
        mixer.init()
        self.exercise = game_turn_details[1]
        self.time_to_answer = game_turn_details[2]
        self.current_time_to_answer = game_turn_details[2]
        self.points = game_turn_details[3]
        self.numbers_move_speed = (Constants.WINDOW_HEIGHT - 150) / self.time_to_answer
        self.timer_on = True
        self.shot_allowed = True

        self.__init_widgets()

    def __left(self, event):
        x_cord, y_cord = self.game_canvas.coords(self.player)
        x = -10  # move 10 left each press
        y = 0  # move 0 up each press
        if x_cord + x > 25:
            self.game_canvas.move(self.player, x, y)

    def __right(self, event):
        x_cord, y_cord = self.game_canvas.coords(self.player)
        x = 10  # move 10 right each press
        y = 0  # move 0 up each press
        if x_cord + x < ((Constants.WINDOW_WIDTH / 3) * 2) - 25:
            self.game_canvas.move(self.player, x, y)

    def __pressing(self, event):
        x_cord, y_cord = self.game_canvas.coords(self.player)
        x = 0
        y = 0
        if event.char == "a" and x_cord + -10 > 25: x = -10
        if event.char == "d" and x_cord + 10 < ((Constants.WINDOW_WIDTH / 3) * 2) - 25: x = 10
        self.game_canvas.move(self.player, x, y)

    def __shoot(self, event):
        if self.shot_allowed:
            self.shot_allowed = False
            mixer.Sound(Constants.SHOT_SOUND_PATH).play()
            self.shot = self.__draw_shot()
            self.__move_shot(self.shot)

    def __draw_shot(self):
        x_cord, y_cord = self.game_canvas.coords(self.player)
        laser_image_path = Constants.LASER_IMG_LIST_PATH[randbelow(len(Constants.LASER_IMG_LIST_PATH))]
        self.laser_shot_image = ImageTk.PhotoImage(Image.open(laser_image_path))
        return self.game_canvas.create_image(x_cord, y_cord - 50, image=self.laser_shot_image)

    def __move_shot(self, shot):
        y_speed = -5
        self.game_canvas.move(shot, 0, y_speed)
        x_cord, y_cord = self.game_canvas.coords(shot)
        y_cord -= 28
        if y_cord <= 0:
            self.game_canvas.delete(shot)
            self.shot_allowed = True
            return
        if self.__number_hit(x_cord, y_cord):
            self.game_canvas.delete(shot)
            return

        self.root.after(10, self.__move_shot, shot)

    def __number_hit(self, x, y):
        for text_id in self.possible_solutions_text_list:
            x_cord, y_cord = self.game_canvas.coords(text_id)
            number_str = self.game_canvas.itemcget(text_id, 'text')
            x_range_delta_list = [8, 16, 22, 28]
            delta = x_range_delta_list[len(number_str) - 1]
            x_min_limit, x_max_limit = x_cord - delta, x_cord + delta
            y_min_limit, y_max_limit = y_cord - 12, y_cord + 12

            if x_min_limit <= x <= x_max_limit and y_min_limit <= y <= y_max_limit:
                self.__check_answer(number_str)
                return True

    def __move_numbers_down(self):
        for text_id in self.possible_solutions_text_list:
            self.game_canvas.move(text_id, 0, self.numbers_move_speed)

    def __restore_numbers_start_position(self):
        for text_id in self.possible_solutions_text_list:
            self.game_canvas.delete(text_id)
        self.__create_numbers_text()

    def __check_answer(self, answer):
        self.shot_allowed = False
        adaptive_learning = AdaptiveLearning.get_instance()
        try:
            answer_time = self.time_to_answer - self.current_time_to_answer
            success = adaptive_learning.answer_game_turn(answer, answer_time)
        except Exception as e:
            class_name = e.__class__.__name__
            if class_name == AnswerTimeTooFast.__name__:
                reply = messagebox.askquestion("זמן מענה מהיר מידי", e)
                if reply == 'yes':
                    success = adaptive_learning.answer_game_turn(answer)
                else:
                    self.shot_allowed = True
                    return

        self.timer_on = False
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
        game_turn_details = AdaptiveLearning.get_instance().get_game_turn()
        if game_turn_details is None:
            self.__show_main_menu()
        else:
            self.exercise = game_turn_details[1]
            self.time_to_answer = game_turn_details[2]
            self.current_time_to_answer = game_turn_details[2]
            self.points = game_turn_details[3]
            self.numbers_move_speed = (Constants.WINDOW_HEIGHT - 150) / self.time_to_answer
            self.__restore_numbers_start_position()
            self.__update_widgets()
            self.deactivate_text()
            self.shot_allowed = True
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
            mixer.Sound(Constants.BUZZER_SOUND_PATH).play()
            AdaptiveLearning.get_instance().answer_game_turn()
            self.__next_turn()
            return

        self.__move_numbers_down()
        self.current_time_to_answer -= 1
        if self.timer_on:
            self.root.after(1000, self.__run_timer)

    def __update_widgets(self):
        self.__update_topic_label()
        self.__update_exercise_label()
        self.__update_points_label()
        self.__update_numbers_text()

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
            self.exercise_label['font'] = ('Ariel', 46, 'bold')
        else:
            exercise_text = self.exercise['question']
            self.exercise_label['font'] = ('Ariel', 22)
            sentences = exercise_text.split('. ')
            exercise_text = ""
            for index, sentence in enumerate(sentences):
                if index < len(sentences) - 1:
                    exercise_text += sentence + "\n\n"
                else:
                    exercise_text += sentence

        self.exercise_label['text'] = exercise_text

    def __update_points_label(self):
        self.game_canvas.itemconfig(self.points_count_text, text=self.points)

    def __update_numbers_text(self):
        exercise_solution = self.exercise['solution']
        possible_solutions_list = [exercise_solution]
        count = 1
        while count != self.__NUM_OPTIONAL_SOLUTIONS:
            number = self.__generate_possible_solution_number(exercise_solution)
            if number not in possible_solutions_list:
                possible_solutions_list.append(number)
                count += 1

        random.shuffle(possible_solutions_list)

        for index, text_id in enumerate(self.possible_solutions_text_list):
            self.game_canvas.itemconfig(text_id, text=possible_solutions_list[index])

    def __create_numbers_text(self):
        exercise_solution = self.exercise['solution']
        possible_solutions_list = [exercise_solution]
        count = 1
        while count != self.__NUM_OPTIONAL_SOLUTIONS:
            number = self.__generate_possible_solution_number(exercise_solution)
            if number not in possible_solutions_list:
                possible_solutions_list.append(number)
                count += 1

        random.shuffle(possible_solutions_list)

        x_distance = 35
        self.possible_solutions_text_list = []
        for number in possible_solutions_list:
            self.possible_solutions_text_list.append(
                self.game_canvas.create_text(x_distance, 50, text=number, fill='yellow2', font=('Ariel 20 bold')))
            x_distance += 78

    def __generate_possible_solution_number(self, exercise_solution):
        min_value = exercise_solution - 5
        max_value = exercise_solution + 5
        return randbelow(max_value - min_value + 1) + min_value

    def __init_widgets(self):
        self.win_frame = Frame(self.root, bg=Constants.BG_COLOR)
        self.win_frame.pack(fill='both', expand=1)

        self.info_canvas = Canvas(self.win_frame, width=Constants.WINDOW_WIDTH / 3, height=Constants.WINDOW_HEIGHT,
                                  highlightthickness=0, bg=Constants.BG_COLOR)
        self.info_canvas.pack(side=LEFT)

        self.game_canvas = Canvas(self.win_frame, width=(Constants.WINDOW_WIDTH / 3) * 2, height=Constants.WINDOW_HEIGHT,
                                  highlightthickness=0, bg='black')
        self.game_canvas.pack(side=LEFT)

        self.game_background_image = ImageTk.PhotoImage(Image.open(Constants.SPACE_BG_IMG_PATH))
        self.game_canvas.create_image(0, 0, image=self.game_background_image, anchor=NW)

        self.astronaut_image = ImageTk.PhotoImage(Image.open(Constants.ASTRONAUT_IMG_PATH))
        self.game_canvas.create_image(((Constants.WINDOW_WIDTH / 3) * 2) - 65, 0, image=self.astronaut_image, anchor=NW)

        player_image_path = Constants.PLAYER_IMG_LIST_PATH[randbelow(len(Constants.PLAYER_IMG_LIST_PATH))]
        self.player_image = ImageTk.PhotoImage(Image.open(player_image_path))
        self.player = self.game_canvas.create_image(((Constants.WINDOW_WIDTH / 3) * 2) / 2,
                                                    Constants.WINDOW_HEIGHT - 50,
                                                    image=self.player_image)

        self.topic_label = TopicLabel(self.info_canvas, '', 20).get_label()
        self.topic_label.place(anchor='n', relx=0.5, rely=0.0)
        self.__update_topic_label()

        self.exercise_frame = Frame(self.info_canvas, bg=Constants.BG_COLOR, highlightbackground="black",
                                    highlightthickness=3)
        self.exercise_frame.place(anchor='n', relx=0.5, rely=0.1)

        self.exercise_label = DataLabel(self.exercise_frame, '').get_data_label()
        self.exercise_label.config(wraplength=300, justify='right')
        self.exercise_label.pack()
        self.__update_exercise_label()

        self.error_frame = Frame(self.info_canvas, bg=Constants.BG_COLOR, highlightbackground="black")
        self.error_frame.place(anchor='s', relx=0.5, rely=0.9)

        self.label_error = Label(self.error_frame, text="", wraplength=300, justify="right",
                                 fg=Constants.ERROR_COLOR,
                                 bg=Constants.BG_COLOR, font=('Ariel', 18, 'bold'))
        self.label_error.pack()

        self.points_count_text = self.game_canvas.create_text(((Constants.WINDOW_WIDTH / 3) * 2) - 55, 60,
                                                              text=self.points, anchor=NW, fill='white',
                                                              font=('Ariel 20 bold'))

        self.__create_numbers_text()

        # bind keys
        self.root.bind("<Key>", self.__pressing)
        self.root.bind("<Left>", self.__left)
        self.root.bind("<Right>", self.__right)
        self.root.bind("<space>", self.__shoot)

        self.__run_timer()
