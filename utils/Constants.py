import os


class Constants(object):
    # GUI RELATED ################################################
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768
    WINDOW_SIZE = str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT)

    BG_COLOR = 'deep sky blue4'
    BUTTON_BG_COLOR = 'OrangeRed3'
    TITLE_COLOR = 'goldenrod2'
    ERROR_COLOR = 'black'

    ROOT_PATH, tail = os.path.split(os.path.abspath(__file__).replace("\\", "/"))
    ROOT_PATH = ROOT_PATH[:-6]
    ICON_PATH = ROOT_PATH + "/icons/ic_arithmetics3.png"
    TIMER_IMG_PATH = ROOT_PATH + "/images/img_timer.png"
    POINTS_IMG_PATH = ROOT_PATH + "/images/img_treasure1.png"
    ASTRONAUT_IMG_PATH = ROOT_PATH + "/images/img_astronaut.png"
    SPACE_BG_IMG_PATH = ROOT_PATH + "/images/img_space_background.png"
    PLAYER_IMG_LIST_PATH = [ROOT_PATH + "/images/img_battleship1.png", ROOT_PATH + "/images/img_battleship2.png",
                            ROOT_PATH + "/images/img_battleship3.png", ROOT_PATH + "/images/img_battleship4.png"]
    LASER_IMG_LIST_PATH = [ROOT_PATH + "/images/img_laser_blue1.png", ROOT_PATH + "/images/img_laser_red1.png",
                           ROOT_PATH + "/images/img_laser_green1.png"]

    CORRECT_ANSWER_FEEDBACK_LIST = ['!כל הכבוד, המשך כך', '!נהדר', '!מצוין', '!יפה מאוד']
    INCORRECT_ANSWER_FEEDBACK_LIST = ['!פעם הבאה תצליח', '!מטעויות לומדים', '!לא נורא']
    CORRECT_ANSWER_SOUND_PATH_LIST = [ROOT_PATH + "/audio/aud_correct_answer1.wav",
                                      ROOT_PATH + "/audio/aud_correct_answer2.wav",
                                      ROOT_PATH + "/audio/aud_correct_answer3.wav"]
    INCORRECT_ANSWER_SOUND_PATH_LIST = [ROOT_PATH + "/audio/aud_incorrect_answer1.wav",
                                        ROOT_PATH + "/audio/aud_incorrect_answer2.wav",
                                        ROOT_PATH + "/audio/aud_incorrect_answer3.wav"]

    BUZZER_SOUND_PATH = ROOT_PATH + "/audio/aud_buzzer.wav"
    SHOT_SOUND_PATH = ROOT_PATH + "/audio/aud_laser_shot.wav"

    DIFFICULTY_ENGLISH_TO_HEBREW_DICT = {'easy': 'קלה', 'intermediate': 'ביניים', 'hard': 'קשה'}
    OPERATOR_DICT = {'subtraction': '-', 'multiplication': '*'}

    # LOGIC RELATED ################################################
    MAX_NUMBER_DIGITS_ANSWER = 5

    MAX_CHOICE_PER_QUESTION_QUESTIONNAIRE = 5
    MIN_CHOICE_PER_QUESTION_QUESTIONNAIRE = 1

    MIN_LEARNING_LEVEL = 0
    MIN_INTERMEDIATE_LEARNING_LEVEL = 9
    MIN_HARD_LEARNING_LEVEL = 17
    MAX_LEARNING_LEVEL = 24

    LEVEL_THRESHOLD_LIST = [MIN_LEARNING_LEVEL, MIN_INTERMEDIATE_LEARNING_LEVEL,
                            MIN_HARD_LEARNING_LEVEL, MAX_LEARNING_LEVEL]

    LEARNED_LEVEL_MIN_THRESHOLDS = {'easy': 9, 'intermediate': 17, 'hard': 25}

    LEARNING_STYLE_DELTA_PERCENT = 1
    LEARNING_LEVEL_DELTA = 1

    EXERCISE_LEARN_COUNT = 3

    LEARNING_STYLE_MIN_PERCENT = 0
    LEARNING_STYLE_MAX_PERCENT = 100

    MIN_POINTS = 0

    TYPE_LIST = ['subtraction', 'multiplication']
    FORMAT_LIST = ['equation', 'phrase']

