from tkinter import *

from utils.Constants import Constants


class TopicLabel(object):
    """
    A helper class used to create custom label widgets with pre-made characteristics.
    """

    def __init__(self, root, text, size=50):
        self.__topic_label = Label(root, text=text, fg=Constants.TITLE_COLOR, bg=Constants.BG_COLOR,
                                 font=('Tahoma', size, 'bold'))

    def get_label(self):
        return self.__topic_label
