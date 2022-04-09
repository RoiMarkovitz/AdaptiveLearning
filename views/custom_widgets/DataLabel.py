from tkinter import *

from utils.Constants import Constants


class DataLabel(object):
    """
    A helper class used to create custom label widgets with pre-made characteristics.
    """

    def __init__(self, root, text, color='black', bold='', size=16, background=Constants.BG_COLOR):
        self.__data_label = Label(root, text=text, font=('Ariel', size, bold), fg=color, bg=background)

    def get_data_label(self):
        return self.__data_label
