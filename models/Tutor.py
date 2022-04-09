import copy
from secrets import randbelow

from models.Expert import Expert
from models.ProfileEvaluation import ProfileEvaluation
from utils.Constants import Constants
from utils.Database import Database
from utils.Exceptions import *
from utils.InputVerification import InputVerification


class Tutor(object):
    __instance = None
    __current_exercise = None
    __current_learning_style = None
    __exercise_list = []
    __is_game_finished = False

    __MIN_ANSWER_TIME_EQUATION = 10  # in seconds
    MIN_ANSWER_TIME_PHRASE = 20  # in seconds
    __TIME_TO_ANSWER_EQUATION = {'easy': 60, 'intermediate': 90, 'hard': 120}  # in seconds
    __TIME_TO_ANSWER_PHRASE = {'easy': 90, 'intermediate': 135, 'hard': 180}  # in seconds

    def __init__(self, student):
        if Tutor.__instance is not None:
            raise Exception('Singleton class - can only have one Tutor class at once!')
        else:
            Tutor.__instance = self
            self.__database = Database.get_instance()
            self.__student = student
            self.__expert = Expert(self.__student)
            self.__profile_evaluation = ProfileEvaluation.get_instance()

    @staticmethod
    def get_instance():
        if Tutor.__instance is None:
            return None
        return Tutor.__instance

    def get_game_turn_details(self):
        if self.__is_game_finished:
            return None

        if not self.__exercise_list:
            self.__exercise_list = self.__expert.get_exercise_list()
            self.__decide_learning_style()

        self.__current_exercise = self.__exercise_list.pop(0)
        game_turn_details = [copy.copy(self.__current_learning_style), copy.copy(self.__current_exercise),
                             self.__decide_time_to_answer(),
                             self.__student.get_points()]

        if not self.__exercise_list:
            self.__is_game_finished = True

        return game_turn_details

    def set_game_finished_false(self):
        self.__is_game_finished = False

    def check_game_turn_answer(self, answer='time over', answer_time=MIN_ANSWER_TIME_PHRASE + 1):
        if answer == 'time over':
            self.__profile_evaluation.evaluate_student_profile(self.__current_learning_style, self.__current_exercise,
                                                               False)
            return

        if InputVerification.verify_answer(answer):
            answer = int(answer)

        if self.__current_exercise['format'] == 'equation' and answer_time <= self.__MIN_ANSWER_TIME_EQUATION \
                or self.__current_exercise['format'] == 'phrase' and answer_time <= self.MIN_ANSWER_TIME_PHRASE:
            raise AnswerTimeTooFast()

        if self.__current_exercise['solution'] == answer:
            success = True
        else:
            success = False
        self.__profile_evaluation.evaluate_student_profile(self.__current_learning_style, self.__current_exercise,
                                                           success)

        return success

    def __decide_learning_style(self):
        sum_percent = 0
        learning_styles = self.__student.get_learning_styles()
        learning_styles_keys = learning_styles.keys()
        for learning_style in learning_styles_keys:
            sum_percent += learning_styles[learning_style]

        # calculate probabilities
        for learning_style, percent in learning_styles.items():
            if sum_percent > Constants.LEARNING_STYLE_MIN_PERCENT:
                learning_styles[learning_style] = percent / sum_percent * Constants.LEARNING_STYLE_MAX_PERCENT
            else:
                learning_styles[learning_style] = Constants.LEARNING_STYLE_MAX_PERCENT / len(learning_styles_keys)

        iter_learning_styles = iter(learning_styles)
        first_learning_style_key = next(iter_learning_styles)
        # check probabilities
        if randbelow(Constants.LEARNING_STYLE_MAX_PERCENT + 1) < learning_styles[first_learning_style_key]:
            self.__current_learning_style = first_learning_style_key
        else:
            self.__current_learning_style = next(iter_learning_styles)

    def __decide_time_to_answer(self):
        exercise_difficulty = self.__current_exercise['difficulty']
        if self.__current_exercise['format'] == 'equation':
            time_to_answer = self.__TIME_TO_ANSWER_EQUATION[exercise_difficulty]
        else:
            time_to_answer = self.__TIME_TO_ANSWER_PHRASE[exercise_difficulty]

        return time_to_answer
