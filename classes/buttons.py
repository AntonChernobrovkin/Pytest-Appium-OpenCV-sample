from pathlib import Path

from classes.cv import CvImage


class Button:
    """
    Class that holds button properties and it's image in Cv ready format
    :var image: CvImage object
    :var x: x coordinate of the button
    :var y: y coordinate of the button
    """
    def __init__(self, image: Path or str):
        self.image = CvImage(image)
        self.x = None
        self.y = None


class Buttons:
    """
    Class that holds all buttons
    """
    def add_button(self, btn_name, image: Path or str):
        button = Button(image)
        self.__setattr__(btn_name, button)
