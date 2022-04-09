from models.ProfileEvaluation import ProfileEvaluation
from utils.Database import Database
from utils.InputVerification import InputVerification


class Examination(object):
    __instance = None
    __current_exercise = None

    def __init__(self, student):
        if Examination.__instance is not None:
            raise Exception('Singleton class - can only have one Examination class at once!')
        else:
            Examination.__instance = self
            self.__database = Database.get_instance()
            self.__student = student
            self.__profile_evaluation = ProfileEvaluation(self.__student)

    @staticmethod
    def get_instance():
        if Examination.__instance is None:
            return None
        return Examination.__instance

    def get_questionnaire(self):
        if self.__student.is_questionnaire_finished():
            return False

        return self.__database.get_questionnaire()

    def finish_questionnaire(self, choices):
        username = self.__student.get_username()
        self.__database.fill_questionnaire(username, choices)
        self.__student.fill_questionnaire(choices)
        self.__database.finish_questionnaire(username)
        self.__student.finish_questionnaire()
        self.__profile_evaluation.analyze_questionnaire_results()
        return self.get_exercise_quiz('first_exercise')

    def get_exercise_quiz(self, answer):
        if self.__student.is_quiz_finished():
            return None
        if answer != 'first_exercise':
            self.__answer_exercise(answer)
        self.__current_exercise = self.__get_next_exercise_quiz()
        if self.__current_exercise is None:
            self.__profile_evaluation.analyze_quiz_results()
            return None
        else:
            return self.__current_exercise

    def __answer_exercise(self, answer):
        if InputVerification.verify_answer(answer):
            answer = int(answer)

        if self.__current_exercise is not None and self.__current_exercise['solution'] == answer:
            self.__database.increment_current_exercise_index_quiz(self.__student.get_username(),
                                                                  self.__student.get_current_category_quiz())
            self.__student.increment_current_exercise_index()
        else:  # wrong answer
            self.__get_next_category_quiz()

    def __get_next_exercise_quiz(self):
        if self.__student.is_quiz_finished():
            return None
        max_exercises_per_category_quiz = self.__student.get_exercises_per_category_quiz()
        current_category = self.__student.get_current_category_quiz()
        current_exercise_index = self.__student.get_current_exercise_index_quiz()
        if max_exercises_per_category_quiz > current_exercise_index:
            exercise = self.__database.get_exercise_quiz(current_exercise_index, current_category)
        else:
            current_category = self.__get_next_category_quiz()
            if not current_category:
                return None  # quiz has ended
            current_exercise_index = self.__student.get_current_exercise_index_quiz()
            exercise = self.__database.get_exercise_quiz(current_exercise_index, current_category)

        return exercise

    def __get_next_category_quiz(self):
        if not self.__student.is_quiz_finished():
            next_category_index = None
            current_category = self.__student.get_current_category_quiz()
            quiz_categories = self.__student.get_categories_quiz()
            quiz_categories_list = []
            for category in quiz_categories.keys():
                quiz_categories_list.append(category)

            for index, category in enumerate(quiz_categories_list):
                if category == current_category:
                    next_category_index = index + 1

            if len(quiz_categories_list) > next_category_index:
                self.__database.update_current_category_quiz(self.__student.get_username(),
                                                             quiz_categories_list[next_category_index])
                self.__student.set_current_category_quiz(quiz_categories_list[next_category_index])
                return quiz_categories_list[next_category_index]
            else:
                self.__database.finish_quiz(self.__student.get_username())
                self.__student.finish_quiz()

        return None
