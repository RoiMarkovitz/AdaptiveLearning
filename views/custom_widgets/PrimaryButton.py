from tkinter import *

from utils.Constants import Constants


class PrimaryButton(object):
    """
    A helper class used to create custom button widgets with pre-made characteristics.
    """

    def __init__(self, root, text, color, width, command):
        self.__button = Button(root, text=text, fg=color, bg=Constants.BUTTON_BG_COLOR,
                             font=('Ariel', 24), width=width, command=command)

    def get_button(self):
        return self.__button
