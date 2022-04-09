class AnswerTimeTooFast(Exception):
    def __init__(self):
        self.message = '?האם אתה בטוח'
        super().__init__(self.message)


class InvalidAnswer(Exception):
    def __init__(self):
        self.message = 'יש להקליד מספר אי-שלילי שלם עד 5 ספרות כולל'
        super().__init__(self.message)


class UsernameNotInEnglish(Exception):
    def __init__(self):
        self.message = 'שם משתמש חוקי חייב להיות בשפה האנגלית בלבד'
        super().__init__(self.message)


class InvalidUsernameLength(Exception):
    def __init__(self):
        self.message = 'שם משתמש חוקי חייב להיות בטווח שבין 2 תווים עד 16 תווים כולל'
        super().__init__(self.message)


class UsernameNotAlpha(Exception):
    def __init__(self):
        self.message = 'שם משתמש חוקי חייב להיות מורכב מתווים בלבד'
        super().__init__(self.message)


class UsernameIsAlreadyTaken(Exception):
    def __init__(self):
        self.message = 'שם המשתמש כבר קיים במערכת. יש לבחור שם משתמש אחר'
        super().__init__(self.message)


class InvalidPassword(Exception):
    def __init__(self):
        self.message = 'הסיסמא איננה חוקית. סיסמא חוקית חייבת להיות מורכבת מאותיות באנגלית או מספרים בלבד ובטווח שבין 6 עד 12 תווים כולל'
        super().__init__(self.message)


class UsernameNotExist(Exception):
    def __init__(self):
        self.message = 'שם המשתמש איננו קיים במערכת. יש לבחור שם משתמש אחר'
        super().__init__(self.message)


class IncorrectPassword(Exception):
    def __init__(self):
        self.message = 'הסיסמא איננה נכונה. יש להקליד סיסמא נכונה'
        super().__init__(self.message)


class NoExercisesLeft(Exception):
    def __init__(self):
        self.message = 'כל הכבוד סיימת את כל התרגילים! נתראה בכיתה ד'
        super().__init__(self.message)

