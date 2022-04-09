from utils.Constants import Constants
from utils.Exceptions import InvalidAnswer


class InputVerification(object):

    @staticmethod
    def verify_category_level(level):
        return Constants.MIN_LEARNING_LEVEL <= level <= Constants.MAX_LEARNING_LEVEL

    @staticmethod
    def verify_learning_style(percent):
        return Constants.LEARNING_STYLE_MIN_PERCENT <= percent <= Constants.LEARNING_STYLE_MAX_PERCENT

    @staticmethod
    def verify_answer(answer):
        if not answer.isdigit() or (answer[0] == '0' and len(answer) > 1) or (
                len(answer) > Constants.MAX_NUMBER_DIGITS_ANSWER):
            raise InvalidAnswer()
        return True

    @staticmethod
    def verify_points(points):
        return points >= Constants.MIN_POINTS
