from tkinter import *

from utils.Constants import Constants
from utils.Database import Database
from views.RegistrationLoginView import RegistrationLoginView
from views.utils.ViewUtil import ViewUtil

root = Tk()  # creating a blank window
ViewUtil.config_window(root, Constants.WINDOW_SIZE, False, 'רישום/כניסה', Constants.ICON_PATH, True, Constants.BG_COLOR)
root.protocol("WM_DELETE_WINDOW", lambda: Database.get_instance().on_closing(root))
RegistrationLoginView(root)

root.mainloop()  # infinite loop to display custom_widgets
