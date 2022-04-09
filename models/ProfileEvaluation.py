from utils.Constants import Constants
from utils.Database import Database


class ProfileEvaluation(object):
    __instance = None
    __WRONG_ANSWER_POINTS = -1
    __RIGHT_ANSWER_POINTS = {'easy': 1, 'intermediate': 2, 'hard': 3}

    def __init__(self, student):
        if ProfileEvaluation.__instance is not None:
            raise Exception('Singleton class - can only have one ProfileEvaluation class at once!')
        else:
            ProfileEvaluation.__instance = self
            self.__database = Database.get_instance()
            self.__student = student

    @staticmethod
    def get_instance():
        if ProfileEvaluation.__instance is None:
            return None
        return ProfileEvaluation.__instance

    def analyze_questionnaire_results(self):
        traditional_sum_choices, modern_sum_choices = 0, 0
        questions = self.__student.get_questions()
        for question in questions:
            question_style = self.__database.get_question_learning_style_questionnaire(question['question_id'])
            if question_style == 'traditional':
                traditional_sum_choices += question['choice']
            else:
                modern_sum_choices += question['choice']

        questions_per_category = self.__student.get_questions_per_category_questionnaire()
        traditional_percent = traditional_sum_choices / (
                Constants.MAX_CHOICE_PER_QUESTION_QUESTIONNAIRE * questions_per_category) * Constants.LEARNING_STYLE_MAX_PERCENT
        modern_percent = modern_sum_choices / (
                Constants.MAX_CHOICE_PER_QUESTION_QUESTIONNAIRE * questions_per_category) * Constants.LEARNING_STYLE_MAX_PERCENT
        username = self.__student.get_username()
        self.__student.set_learning_style_percent('traditional', traditional_percent)
        self.__database.update_user_learning_style(username, 'traditional', traditional_percent)
        self.__student.set_learning_style_percent('modern', modern_percent)
        self.__database.update_user_learning_style(username, 'modern', modern_percent)

    def analyze_quiz_results(self):
        username = self.__student.get_username()
        categories = self.__student.get_categories_quiz()
        for level_category in categories:
            number_solved_exercises = categories[level_category]['current_exercise_index']
            self.__update_learning_category_level_by_quiz(username, level_category, number_solved_exercises)
            self.__update_exercises_status_by_quiz(username, level_category, number_solved_exercises)

    def __update_learning_category_level_by_quiz(self, username, category_level, number_solved_exercises):
        learning_level = Constants.LEVEL_THRESHOLD_LIST[number_solved_exercises]
        self.__student.set_category_level(category_level, learning_level)
        self.__database.update_user_category_level(username, category_level, learning_level)

    def __update_exercises_status_by_quiz(self, username, level_category, number_solved_exercises):
        exercises_per_category = self.__student.get_exercises_per_category_quiz()
        exercises_id_list = self.__database.get_exercise_id_list_quiz(level_category)
        for index in range(number_solved_exercises + 1):
            if index < exercises_per_category:
                exercise_id = exercises_id_list[index]['exercise_id']
                exercise = self.__database.get_exercise(exercise_id)
                exercise_category = 'unseen_exercises'
                self.__student.remove_exercise(exercise_id, exercise_category, exercise)
                self.__database.remove_user_exercise(username, exercise_id, exercise_category)
                if index < number_solved_exercises:
                    count = 1
                else:
                    count = 0
                exercise_category = 'unlearned_exercises'
                self.__student.add_exercise(exercise_id, exercise_category, exercise, count)
                self.__database.add_user_exercise(username, exercise_id, exercise_category, count)

    def evaluate_student_profile(self, learning_style, exercise, success):
        username = self.__student.get_username()
        exercise_id = self.__student.get_exercise_id(exercise)
        exercise_category = self.__student.get_exercise_category(exercise_id)
        level_category = exercise['type'] + '_' + exercise['format']
        exercise_difficulty = exercise['difficulty']
        self.__update_points(username, exercise_difficulty, success)
        self.__update_learning_style(username, learning_style, success)
        self.__update_exercise_status(username, exercise, exercise_id, exercise_category, success)
        self.__update_learned_category_level(username, level_category, exercise_difficulty)
        self.__update_category_level(username, level_category, success)

    def __update_points(self, username, exercise_difficulty, success):
        current_points = self.__student.get_points()
        if success:
            points_to_update = current_points + self.__RIGHT_ANSWER_POINTS[exercise_difficulty]
        else:
            points_to_update = current_points + self.__WRONG_ANSWER_POINTS

        self.__student.set_points(points_to_update)
        self.__database.update_user_points(username, points_to_update)

    def __update_learning_style(self, username, learning_style, success):
        learning_style_percent = self.__student.get_learning_style_percent(learning_style)
        if success:
            value_to_update = learning_style_percent + Constants.LEARNING_STYLE_DELTA_PERCENT
        else:
            value_to_update = learning_style_percent + Constants.LEARNING_STYLE_DELTA_PERCENT * -1

        self.__student.set_learning_style_percent(learning_style, value_to_update)
        self.__database.update_user_learning_style(username, learning_style, value_to_update)

    def __update_exercise_status(self, username, exercise, exercise_id, exercise_category, success):
        if exercise_category == 'unseen_exercises':
            self.__student.remove_exercise(exercise_id, exercise_category, exercise)
            self.__database.remove_user_exercise(username, exercise_id, exercise_category)
            if success:
                count = 1
            else:
                count = 0
            exercise_category = 'unlearned_exercises'
            self.__student.add_exercise(exercise_id, exercise_category, exercise, count)
            self.__database.add_user_exercise(username, exercise_id, exercise_category, count)
        else:
            count = self.__student.get_exercise_count(exercise, exercise_id)
            if success:
                if count + 1 < Constants.EXERCISE_LEARN_COUNT:
                    self.__student.increment_exercise_counter(exercise_id, exercise_category, exercise, 1)
                    self.__database.increment_user_exercise_counter(username, exercise_id, 1)
                else:
                    self.__student.remove_exercise(exercise_id, exercise_category, exercise)
                    self.__database.remove_user_exercise(username, exercise_id, exercise_category)
                    exercise_category = 'learned_exercises'
                    self.__student.add_exercise(exercise_id, exercise_category, exercise, count)
                    self.__database.add_user_exercise(username, exercise_id, exercise_category, count)
            else:
                count *= -1
                self.__student.increment_exercise_counter(exercise_id, exercise_category, exercise, count)
                self.__database.increment_user_exercise_counter(username, exercise_id, count)

    def __update_learned_category_level(self, username, category_level, exercise_difficulty):
        type_format_list = category_level.split('_')
        exercise_type = type_format_list[0]
        exercise_format = type_format_list[1]

        unseen_exercise_list = self.__student.get_exercises_list('unseen_exercises', exercise_type, exercise_format,
                                                                 exercise_difficulty)
        unlearned_exercise_list = self.__student.get_exercises_list('unlearned_exercises', exercise_type,
                                                                    exercise_format,
                                                                    exercise_difficulty)

        if unseen_exercise_list is None and unlearned_exercise_list is None:
            self.__student.set_highest_learned_difficulty(category_level, exercise_difficulty)
            self.__database.update_highest_learned_difficulty(username, category_level, exercise_difficulty)

    def __update_category_level(self, username, category_level, success):
        category_level_value = self.__student.get_category_level_value(category_level)
        if success:
            value_to_update = category_level_value + Constants.LEARNING_LEVEL_DELTA
        else:
            value_to_update = category_level_value + Constants.LEARNING_LEVEL_DELTA * -1
            highest_learned_difficulty = self.__student.get_highest_learned_difficulty(category_level)
            if highest_learned_difficulty is not None:
                min_level_value = Constants.LEARNED_LEVEL_MIN_THRESHOLDS[highest_learned_difficulty]
                if value_to_update < min_level_value:
                    return

        self.__student.set_category_level(category_level, value_to_update)
        self.__database.update_user_category_level(username, category_level, value_to_update)
