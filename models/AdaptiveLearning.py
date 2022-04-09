from models.Examination import Examination
from models.Student import Student
from models.Tutor import Tutor
from utils.Database import Database


# Manager class

class AdaptiveLearning(object):
    __instance = None
    __student = None

    def __init__(self):
        if AdaptiveLearning.__instance is not None:
            raise Exception('Singleton class - can only have one manager class at once!')
        else:
            AdaptiveLearning.__instance = self
            self.__database = Database.get_instance()

    @staticmethod
    def get_instance():
        if AdaptiveLearning.__instance is None:
            AdaptiveLearning()
        return AdaptiveLearning.__instance

    def login_student(self, username, password):
        student_details = self.__database.login(username, password)
        self.__student = Student(username, student_details['points'], student_details['level'],
                                 student_details['learning_styles'], student_details['exercises'],
                                 student_details['questionnaire'], student_details['quiz'])

        self.__examination = Examination(self.__student)
        self.__tutor = Tutor(self.__student)

        questionnaire = {'questionnaire': self.__examination.get_questionnaire()}
        if questionnaire['questionnaire']:
            return questionnaire
        exercise = {'exercise': self.__examination.get_exercise_quiz('first_exercise')}
        if exercise['exercise']:
            return exercise

        return True

    def register_student(self, username, password):
        self.__database.registration(username, password)
        return self.login_student(username, password)

    def finish_questionnaire(self, choices):
        return self.__examination.finish_questionnaire(choices)

    def answer_and_get_next_exercise_quiz(self, answer):
        return self.__examination.get_exercise_quiz(answer)

    def get_game_turn(self):
        game_turn_details = self.__tutor.get_game_turn_details()
        if game_turn_details is None:
            self.__tutor.set_game_finished_false()
        return game_turn_details

    def answer_game_turn(self, answer='time over', answer_time=Tutor.MIN_ANSWER_TIME_PHRASE + 1):
        return self.__tutor.check_game_turn_answer(answer, answer_time)
