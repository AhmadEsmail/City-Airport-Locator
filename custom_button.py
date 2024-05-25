# custom_button.py
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
<CustomButton>:
    ize_hint: None, None
    size: dp(150), dp(45)
    font_size: '18sp'
    bold: True
    background_color: 0.2, 0.8, 0.2, 0.8
    color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1  # Border color (white)
        Line:
            width: 1.2
            rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
''')

class CustomButton(Button):
    pass
