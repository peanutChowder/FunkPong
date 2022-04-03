from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window


from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock

class Shapey(Widget):
    pass



class Base(Widget):
    def __init__(self):
        super(Base, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)



class Test1App(App):
    def build(self):
        a = Base()
        # a.create()
        return a


Test1App().run()


