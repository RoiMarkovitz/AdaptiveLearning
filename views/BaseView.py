from abc import ABC


class BaseView(ABC):
    label_error = None
    error_frame = None

    def activate_text_error(self, text):
        self.error_frame.config(highlightthickness=3)
        self.label_error['text'] = text

    def deactivate_text(self):
        self.error_frame.config(highlightthickness=0)
        self.label_error['text'] = ''

    def clear_text(self, event):
        event.widget.delete(0, "end")


