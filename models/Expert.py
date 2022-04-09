import random

from utils.Constants import Constants
from utils.Database import Database
from utils.Exceptions import NoExercisesLeft


class Expert(object):
    __instance = None

    __NUMBER_EXERCISES_PER_LIST = 2

    def __init__(self, student):
        if Expert.__instance is not None:
            raise Exception('Singleton class - can only have one Expert class at once!')
        else:
            Expert.__instance = self
            self.__database = Database.get_instance()
            self.__student = student

    @staticmethod
    def get_instance():
        if Expert.__instance is None:
            return None
        return Expert.__instance

    def get_exercise_list(self):
        return self.__create_exercise_list()

    def __create_exercise_list(self):
        categories_level = self.__student.get_level()
        lowest_category_level_one_dict = self.__find_lowest_category_level(categories_level)
        del categories_level[next(iter(lowest_category_level_one_dict))]
        lowest_category_level_two_dict = self.__find_lowest_category_level(categories_level)

        lowest_category_level_one_key = next(iter(lowest_category_level_one_dict))
        lowest_category_level_one_value = lowest_category_level_one_dict[lowest_category_level_one_key]
        lowest_category_level_two_key = next(iter(lowest_category_level_two_dict))
        lowest_category_level_two_value = lowest_category_level_two_dict[lowest_category_level_two_key]
        lowest_category_level_one_difficulty = self.__find_category_level_difficulty(lowest_category_level_one_value)
        lowest_category_level_two_difficulty = self.__find_category_level_difficulty(lowest_category_level_two_value)

        unseen_exercises_id_list_category_one = self.__find_exercise_list('unseen_exercises',
                                                                          lowest_category_level_one_key,
                                                                          lowest_category_level_one_difficulty)
        unlearned_exercises_id_list_category_one = self.__find_exercise_list('unlearned_exercises',
                                                                             lowest_category_level_one_key,
                                                                             lowest_category_level_one_difficulty)
        unseen_exercises_id_list_category_two = self.__find_exercise_list('unseen_exercises',
                                                                          lowest_category_level_two_key,
                                                                          lowest_category_level_two_difficulty)
        unlearned_exercises_id_list_category_two = self.__find_exercise_list('unlearned_exercises',
                                                                             lowest_category_level_two_key,
                                                                             lowest_category_level_two_difficulty)

        exercise_id_list = []
        self.__fill_exercise_list(exercise_id_list, unseen_exercises_id_list_category_one,
                                  unlearned_exercises_id_list_category_one)
        self.__fill_exercise_list(exercise_id_list, unseen_exercises_id_list_category_two,
                                  unlearned_exercises_id_list_category_two)

        exercise_list_for_student = []
        for exercise_id in exercise_id_list:
            exercise_list_for_student.append(self.__database.get_exercise(exercise_id['exercise_id']))

        return exercise_list_for_student

    def __find_lowest_category_level(self, categories_level):
        keys_list = list(categories_level.keys())
        min_level_category_key = keys_list.pop(0)
        for key in keys_list:
            if categories_level[min_level_category_key]['level'] > categories_level[key]['level']:
                min_level_category_key = key

        return {min_level_category_key: categories_level[min_level_category_key]['level']}

    def __find_category_level_difficulty(self, level_value):
        if level_value in range(Constants.MIN_LEARNING_LEVEL,
                                Constants.MIN_INTERMEDIATE_LEARNING_LEVEL):
            lowest_category_level_difficulty = 'easy'
        elif level_value in range(
                Constants.MIN_INTERMEDIATE_LEARNING_LEVEL,
                Constants.MIN_HARD_LEARNING_LEVEL):
            lowest_category_level_difficulty = 'intermediate'
        elif level_value in range(Constants.MIN_HARD_LEARNING_LEVEL,
                                Constants.MAX_LEARNING_LEVEL + 1):
            lowest_category_level_difficulty = 'hard'
        else:  # student finished all exercises
            raise NoExercisesLeft()

        return lowest_category_level_difficulty

    def __find_exercise_list(self, exercise_category, level_category, exercise_difficulty):
        type_format_list = level_category.split('_')
        exercise_type = type_format_list[0]
        exercise_format = type_format_list[1]
        exercise_list = self.__student.get_exercises_list(exercise_category, exercise_type, exercise_format,
                                                          exercise_difficulty)
        random.shuffle(exercise_list)
        return exercise_list

    def __fill_exercise_list(self, exercise_id_list_to_fill, unseen_exercises_id_list, unlearned_exercises_id_list):
        count = 0
        while (count != self.__NUMBER_EXERCISES_PER_LIST * 2) or (
                not unseen_exercises_id_list and not unlearned_exercises_id_list):
            if unseen_exercises_id_list:
                exercise_id_list_to_fill.append(unseen_exercises_id_list.pop(0))
                count += 1
            if unlearned_exercises_id_list:
                exercise_id_list_to_fill.append(unlearned_exercises_id_list.pop(0))
                count += 1
