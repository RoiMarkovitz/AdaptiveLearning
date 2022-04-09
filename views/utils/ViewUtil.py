from tkinter import *


class ViewUtil(object):
    """
    A helper class used to config windows with pre-made characteristics.
    """

    @staticmethod
    def config_window(root, window_size, is_resizable, title, icon_path, is_always_on_top, background_color):
        root.geometry(window_size)
        if not is_resizable:
            root.resizable(0, 0)
        root.title(title)
        icon = PhotoImage(file=icon_path)
        root.iconphoto(False, icon)
        if is_always_on_top:
            root.wm_attributes('-topmost', True)
        root.configure(bg=background_color)
