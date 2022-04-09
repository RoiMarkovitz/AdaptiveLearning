import copy

from utils.Constants import Constants
from utils.InputVerification import InputVerification


class Student(object):

    def __init__(self, username, points, level, learning_styles, exercises, questionnaire, quiz):
        self.__username = username
        self.__points = points
        self.__level = level
        self.__learning_styles = learning_styles
        self.__exercises = exercises
        self.__questionnaire = questionnaire
        self.__quiz = quiz

    def get_username(self):
        return copy.copy(self.__username)

    def get_points(self):
        return copy.copy(self.__points)

    def set_points(self, points):
        if InputVerification.verify_points(points):
            self.__points = points

    def get_level(self):
        return copy.copy(self.__level)

    def set_category_level(self, category_level, level):
        if InputVerification.verify_category_level(level):
            self.__level[category_level]['level'] = level

    def set_highest_learned_difficulty(self, category_level, learned_difficulty):
        self.__level[category_level]['highest_learned_difficulty'] = learned_difficulty

    def get_highest_learned_difficulty(self, category_level):
        return self.__level[category_level]['highest_learned_difficulty']

    def get_category_level_value(self, category_level):
        return self.__level[category_level]['level']

    def get_learning_styles(self):
        return copy.copy(self.__learning_styles)

    def get_learning_style_percent(self, learning_style):
        return self.__learning_styles[learning_style]

    def set_learning_style_percent(self, learning_style, percent):
        if InputVerification.verify_learning_style(percent):
            self.__learning_styles[learning_style] = percent

    def get_exercises_list(self, exercise_category, exercise_type, exercise_format, exercise_difficulty):
        return copy.copy(self.__exercises[exercise_category][exercise_type][exercise_format][exercise_difficulty])

    def get_exercise_id(self, exercise):
        return exercise['_id']

    def __get_exercise_array_path(self, exercise_category, exercise):
        exercise_difficulty = exercise['difficulty']
        exercise_type = exercise['type']
        exercise_format = exercise['format']
        return 'exercises.' + exercise_category + '.' + exercise_type + '.' + exercise_format + '.' + exercise_difficulty

    def get_exercise_category(self, exercise_id):
        unseen_exercises = self.__exercises['unseen_exercises']
        unlearned_exercises = self.__exercises['unlearned_exercises']
        type_list = Constants.TYPE_LIST
        format_list = Constants.FORMAT_LIST
        for index_type in range(len(type_list)):
            for index_format in range(len(format_list)):
                if self.__is_exercise_in_category(exercise_id,
                                                  type_list[index_type], format_list[index_format], unseen_exercises):
                    return 'unseen_exercises'
        for index_type in range(len(type_list)):
            for index_format in range(len(format_list)):
                if self.__is_exercise_in_category(exercise_id,
                                                  type_list[index_type], format_list[index_format],
                                                  unlearned_exercises):
                    return 'unlearned_exercises'

    def __is_exercise_in_category(self, exercise_id, exercise_type, exercise_format, exercise_category):
        exercise_lists = exercise_category[exercise_type][exercise_format]
        for _, exercise_list in exercise_lists.items():
            for exercise in exercise_list:
                if exercise_id == exercise['exercise_id']:
                    return True
        return False

    def get_exercise_count(self, exercise, exercise_id):
        exercise_list = self.__exercises['unlearned_exercises'][exercise['type']][exercise['format']][
            exercise['difficulty']]
        for e in exercise_list:
            if exercise_id == e['exercise_id']:
                return e['counter']

    def remove_exercise(self, exercise_id, exercise_category, exercise):
        path_list = self.__get_exercise_array_path(exercise_category, exercise).split('.')
        exercise_list = self.__exercises[path_list[1]][path_list[2]][path_list[3]][path_list[4]]
        exercise_index_to_remove = None
        for index, exercise in enumerate(exercise_list):
            if exercise_id == exercise['exercise_id']:
                exercise_index_to_remove = index
        if exercise_index_to_remove is not None:
            exercise_list.pop(exercise_index_to_remove)

    def add_exercise(self, exercise_id, exercise_category, exercise, count):
        path_list = self.__get_exercise_array_path(exercise_category, exercise).split('.')
        exercise_category = path_list[1]
        exercise_list = self.__exercises[path_list[1]][path_list[2]][path_list[3]][path_list[4]]
        if exercise_category == 'unlearned_exercises':
            exercise_list.append({'exercise_id': exercise_id, 'counter': count})
        else:
            exercise_list.append({'exercise_id': exercise_id})

    def increment_exercise_counter(self, exercise_id, exercise_category, exercise, value):
        path_list = self.__get_exercise_array_path(exercise_category, exercise).split('.')
        exercise_list = self.__exercises[path_list[1]][path_list[2]][path_list[3]][path_list[4]]
        exercise_index_to_update = None
        for index, exercise in enumerate(exercise_list):
            if exercise_id == exercise['exercise_id']:
                exercise_index_to_update = index
        if exercise_index_to_update is not None:
            value_to_update = exercise_list[exercise_index_to_update]['counter'] + value
            exercise_list[exercise_index_to_update]['counter'] = value_to_update

    def is_questionnaire_finished(self):
        return self.__questionnaire['finished']

    def finish_questionnaire(self):
        self.__questionnaire['finished'] = True

    def fill_questionnaire(self, choices):
        questions = self.__questionnaire['questions']
        for index in range(len(questions)):
            questions[index]['choice'] = choices[index]

    def get_questions(self):
        return self.__questionnaire['questions']

    def get_questions_per_category_questionnaire(self):
        return self.__questionnaire['questions_per_category']

    def finish_quiz(self):
        self.__quiz['finished'] = True

    def is_quiz_finished(self):
        return self.__quiz['finished']

    def get_current_category_quiz(self):
        return self.__quiz['current_category']

    def get_categories_quiz(self):
        return self.__quiz['categories']

    def set_current_category_quiz(self, current_category):
        self.__quiz['current_category'] = current_category

    def get_current_exercise_index_quiz(self):
        return self.__quiz['categories'][self.get_current_category_quiz()]['current_exercise_index']

    def get_exercises_per_category_quiz(self):
        return self.__quiz['exercises_per_category']

    def increment_current_exercise_index(self):
        self.__quiz['categories'][self.__quiz['current_category']]['current_exercise_index'] += 1
