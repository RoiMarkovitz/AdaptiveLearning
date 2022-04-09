import base64
import json
import re

import pymongo

from utils.Constants import Constants
from utils.Exceptions import *
from utils.InputVerification import InputVerification


class Database(object):
    __instance = None
    __client = None

    __unseen_easy_subtraction_equation_exercises_id = []
    __unseen_intermediate_subtraction_equation_exercises_id = []
    __unseen_hard_subtraction_equation_exercises_id = []
    __unseen_easy_subtraction_phrase_exercises_id = []
    __unseen_intermediate_subtraction_phrase_exercises_id = []
    __unseen_hard_subtraction_phrase_exercises_id = []
    __unseen_easy_multiplication_equation_exercises_id = []
    __unseen_intermediate_multiplication_equation_exercises_id = []
    __unseen_hard_multiplication_equation_exercises_id = []
    __unseen_easy_multiplication_phrase_exercises_id = []
    __unseen_intermediate_multiplication_phrase_exercises_id = []
    __unseen_hard_multiplication_phrase_exercises_id = []

    __collection_users = None
    __collection_sequences = None
    __collection_exercises = None
    __collection_quiz = None
    __collection_questionnaire = None

    def __init__(self):
        if Database.__instance is not None:
            raise Exception('Singleton class - can only have one database object at once!')
        else:
            Database.__instance = self
            self.__db = self.__connect_to_database()
            self.__init_collections()
            if not self.__db.list_collection_names():
                self.__init_database()
            self.__fill_all_exercises_id_lists()

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def on_closing(self, root):
        if self.__client is not None:
            self.__client.close()
        root.destroy()

    def __connect_to_database(self):
        conn_str = 'mongodb://localhost:27017/'
        self.__client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
        return self.__client['math-expert']

    def __init_collections(self):
        self.__collection_users = self.__db['users']
        self.__collection_sequences = self.__db['sequences']
        self.__collection_exercises = self.__db['exercises']
        self.__collection_quiz = self.__db['quiz']
        self.__collection_questionnaire = self.__db['questionnaire']

    def __fill_exercise_id_lists(self, easy_id_list, intermediate_id_list, hard_id_list, exercise_type,
                                 exercise_format):
        cursor = self.__collection_exercises.find({'type': exercise_type, 'format': exercise_format})
        for doc in cursor:
            if doc['difficulty'] == 'easy':
                easy_id_list.append({'exercise_id': doc['_id']})
            elif doc['difficulty'] == 'intermediate':
                intermediate_id_list.append({'exercise_id': doc['_id']})
            else:
                hard_id_list.append({'exercise_id': doc['_id']})
        cursor.close()

    def __fill_all_exercises_id_lists(self):
        self.__fill_exercise_id_lists(self.__unseen_easy_subtraction_equation_exercises_id,
                                      self.__unseen_intermediate_subtraction_equation_exercises_id,
                                      self.__unseen_hard_subtraction_equation_exercises_id, 'subtraction', 'equation')
        self.__fill_exercise_id_lists(self.__unseen_easy_subtraction_phrase_exercises_id,
                                      self.__unseen_intermediate_subtraction_phrase_exercises_id,
                                      self.__unseen_hard_subtraction_phrase_exercises_id, 'subtraction', 'phrase')
        self.__fill_exercise_id_lists(self.__unseen_easy_multiplication_equation_exercises_id,
                                      self.__unseen_intermediate_multiplication_equation_exercises_id,
                                      self.__unseen_hard_multiplication_equation_exercises_id, 'multiplication',
                                      'equation')
        self.__fill_exercise_id_lists(self.__unseen_easy_multiplication_phrase_exercises_id,
                                      self.__unseen_intermediate_multiplication_phrase_exercises_id,
                                      self.__unseen_hard_multiplication_phrase_exercises_id, 'multiplication', 'phrase')

    def __get_user(self, username):
        user = None
        cursor = self.__collection_users.find({'username': username})
        if cursor.collection.count_documents({'username': username}) != 0:
            user = cursor.next()
        cursor.close()
        return user

    def get_exercise(self, exercise_id):
        exercise = None
        cursor = self.__collection_exercises.find({'_id': exercise_id})
        if cursor.collection.count_documents({'_id': exercise_id}) != 0:
            exercise = cursor.next()
        cursor.close()
        return exercise

    def __get_question(self, question_id):
        question = None
        cursor = self.__collection_questionnaire.find({'_id': question_id})
        if cursor.collection.count_documents({'_id': question_id}) != 0:
            question = cursor.next()
        cursor.close()
        return question

    def update_highest_learned_difficulty(self, username, category_level, learned_difficulty):
        path = 'level.' + category_level + '.highest_learned_difficulty'
        self.__collection_users.update_one({'username': username}, {'$set': {path: learned_difficulty}})

    def update_user_category_level(self, username, category_level, level):
        if InputVerification.verify_category_level(level):
            path = 'level.' + category_level + '.level'
            self.__collection_users.update_one({'username': username}, {'$set': {path: level}})

    def update_user_learning_style(self, username, learning_style, percent):
        if InputVerification.verify_learning_style(percent):
            self.__collection_users.update_one({'username': username},
                                               {'$set': {'learning_styles.' + learning_style: percent}})

    def update_user_points(self, username, points):
        if InputVerification.verify_points(points):
            self.__collection_users.update_one({'username': username}, {'$set': {'points': points}})

    def get_user_exercise_array_path(self, exercise_id, exercise_category):
        exercise = self.get_exercise(exercise_id)
        if exercise is None:
            return None
        exercise_difficulty = exercise['difficulty']
        exercise_type = exercise['type']
        exercise_format = exercise['format']
        return 'exercises.' + exercise_category + '.' + exercise_type + '.' + exercise_format + '.' + exercise_difficulty

    def __get_user_exercises_list(self, username, exercise_category, exercise_type, exercise_format,
                                  exercise_difficulty):
        user = self.__get_user(username)
        if user:
            return user['exercises'][exercise_category][exercise_type][exercise_format][exercise_difficulty]
        else:
            return None

    def remove_user_exercise(self, username, exercise_id, exercise_category):
        path = self.get_user_exercise_array_path(exercise_id, exercise_category)
        if path is None:
            return None
        self.__collection_users.update_one({'username': username}, {'$pull': {path: {'exercise_id': exercise_id}}})

    def add_user_exercise(self, username, exercise_id, exercise_category, count):
        path = self.get_user_exercise_array_path(exercise_id, exercise_category)
        if path is None:
            return None
        if exercise_category == 'unlearned_exercises':
            self.__collection_users.update_one({'username': username},
                                               {'$push': {path: {'exercise_id': exercise_id, 'counter': count}}})
        else:
            self.__collection_users.update_one({'username': username}, {'$push': {path: {'exercise_id': exercise_id}}})

    def increment_user_exercise_counter(self, username, exercise_id, value):
        path = self.get_user_exercise_array_path(exercise_id, 'unlearned_exercises')
        if path is None:
            return None
        path_list = path.split('.')
        exercises_list = self.__get_user_exercises_list(username, 'unlearned_exercises', path_list[2], path_list[3],
                                                        path_list[4])
        if exercises_list is None:
            return None
        index = None
        for i, exercise in enumerate(exercises_list):
            if exercise['exercise_id'] == exercise_id:
                index = i
        if index is not None:
            path = path + '.' + str(index) + '.' + 'counter'
            self.__collection_users.update_one({'username': username}, {'$inc': {path: value}})

    def finish_quiz(self, username):
        self.__collection_users.update_one({'username': username}, {'$set': {'quiz.finished': True}})

    def increment_current_exercise_index_quiz(self, username, exercise_category):
        path = 'quiz.categories.' + exercise_category + '.current_exercise_index'
        self.__collection_users.update_one({'username': username}, {'$inc': {path: 1}})

    def get_exercise_quiz(self, exercise_index, exercise_category):
        exercise_id_list = self.get_exercise_id_list_quiz(exercise_category)
        return self.get_exercise(exercise_id_list[exercise_index]['exercise_id'])

    def get_exercise_id_list_quiz(self, exercise_category):
        return self.__collection_quiz.find({'_id': 1}).next()['categories'][exercise_category]

    def update_current_category_quiz(self, username, exercise_category):
        path = 'quiz.current_category'
        self.__collection_users.update_one({'username': username}, {'$set': {path: exercise_category}})

    def get_questionnaire(self):
        questionnaire = []
        cursor = self.__collection_questionnaire.find({})
        for doc in cursor:
            questionnaire.append(doc)
        cursor.close()
        return questionnaire

    def finish_questionnaire(self, username):
        path = 'questionnaire.finished'
        self.__collection_users.update_one({'username': username}, {'$set': {path: True}})

    def __get_questionnaire_user_questions(self, username):
        user = self.__get_user(username)
        if user:
            return user['questionnaire']['questions']
        else:
            return None

    def fill_questionnaire(self, username, choices):
        user_questions = self.__get_questionnaire_user_questions(username)
        if user_questions is None:
            return None
        for index in range(len(user_questions)):
            user_questions[index]['choice'] = choices[index]
        path = 'questionnaire.questions'
        self.__collection_users.update_one({'username': username}, {'$set': {path: user_questions}})

    def get_question_learning_style_questionnaire(self, question_id):
        question = self.__get_question(question_id)
        if question:
            return question['style']
        else:
            return None

    def __validate_username(self, username):
        if not username.isascii():
            raise UsernameNotInEnglish()
        if not 2 <= len(username) <= 16:
            raise InvalidUsernameLength()
        if not username.isalpha():
            raise UsernameNotAlpha()
        if self.__get_user(username) is not None:
            raise UsernameIsAlreadyTaken()

        return True

    def __validate_password(self, password):
        if not re.fullmatch(r'[A-Za-z0-9]{6,12}', password):
            raise InvalidPassword()
        return True

    def __encode_password(self, decoded_password):
        return base64.b64encode(decoded_password.encode('utf-8'))

    def __decode_password(self, encoded_password):
        return base64.b64decode(encoded_password).decode('utf-8')

    def login(self, username, login_password):
        user = self.__get_user(username)
        if user is None:
            raise UsernameNotExist()
        if self.__decode_password(user['password']) != login_password:
            raise IncorrectPassword()
        return user

    def registration(self, username, password):
        self.__validate_username(username)
        self.__validate_password(password)
        self.__insert_new_user(username, self.__encode_password(password))

    def __get_new_user_id(self):
        self.__collection_sequences.update_one({'collection': 'users_collection'}, {'$inc': {'seq_id': 1}})
        return self.__collection_sequences.find({'collection': 'users_collection'}).next()['seq_id']

    def __insert_new_user(self, username, password):
        user_id = self.__get_new_user_id()
        user_document = self.__create_user_document(user_id, username, password)
        self.__collection_users.insert_one(user_document)

    def __create_user_document(self, user_id, username, password):
        file_path = f"{Constants.ROOT_PATH}/json/user_document.json"
        with open(file_path) as json_file:
            user_document = json.load(json_file)
        user_document['_id'], user_document['username'], user_document['password'] = user_id, username, password

        return self.__add_unseen_exercise_lists_to_user_document(user_document)

    def __add_unseen_exercise_lists_to_user_document(self, user_document):
        user_document['exercises']['unseen_exercises']['subtraction']['equation'][
            'easy'] = self.__unseen_easy_subtraction_equation_exercises_id
        user_document['exercises']['unseen_exercises']['subtraction']['equation'][
            'intermediate'] = self.__unseen_intermediate_subtraction_equation_exercises_id
        user_document['exercises']['unseen_exercises']['subtraction']['equation'][
            'hard'] = self.__unseen_hard_subtraction_equation_exercises_id
        user_document['exercises']['unseen_exercises']['subtraction']['phrase'][
            'easy'] = self.__unseen_easy_subtraction_phrase_exercises_id
        user_document['exercises']['unseen_exercises']['subtraction']['phrase'][
            'intermediate'] = self.__unseen_intermediate_subtraction_phrase_exercises_id
        user_document['exercises']['unseen_exercises']['subtraction']['phrase'][
            'hard'] = self.__unseen_hard_subtraction_phrase_exercises_id
        user_document['exercises']['unseen_exercises']['multiplication']['equation'][
            'easy'] = self.__unseen_easy_multiplication_equation_exercises_id
        user_document['exercises']['unseen_exercises']['multiplication']['equation'][
            'intermediate'] = self.__unseen_intermediate_multiplication_equation_exercises_id
        user_document['exercises']['unseen_exercises']['multiplication']['equation'][
            'hard'] = self.__unseen_hard_multiplication_equation_exercises_id
        user_document['exercises']['unseen_exercises']['multiplication']['phrase'][
            'easy'] = self.__unseen_easy_multiplication_phrase_exercises_id
        user_document['exercises']['unseen_exercises']['multiplication']['phrase'][
            'intermediate'] = self.__unseen_intermediate_multiplication_phrase_exercises_id
        user_document['exercises']['unseen_exercises']['multiplication']['phrase'][
            'hard'] = self.__unseen_hard_multiplication_phrase_exercises_id

        return user_document

    def __init_database(self):
        self.__insert_document(self.__collection_quiz, f"{Constants.ROOT_PATH}/json/quiz.json", True)
        self.__insert_document(self.__collection_questionnaire, f"{Constants.ROOT_PATH}/json/questionnaire.json", False)
        self.__insert_document(self.__collection_sequences, f"{Constants.ROOT_PATH}/json/sequences.json", True)
        self.__insert_document(self.__collection_exercises, f"{Constants.ROOT_PATH}/json/exercises.json", False)

    def __insert_document(self, collection_name, json_file_name, is_one):
        with open(json_file_name, encoding='utf-8-sig') as json_file:
            document = json.load(json_file)
        if is_one:
            collection_name.insert_one(document)
        else:
            collection_name.insert_many(document)
