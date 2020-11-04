from Project.Components.Managers.QuestionManager import QuestionManger
from Project.Components.Managers.OptionsManager import OptionsManager
from Project.Components.Simulator import simulate
from Project.Consts.OurQuestions import *


class Consultant:
    def __init__(self):
        self.question_manager = QuestionManger(questions_array)
        self.question_manager.start()
        self.options_manager = OptionsManager(self.question_manager.answers)
        self.options_manager.start()
        self.simulate()

    def simulate(self):
        simulate(self.options_manager)
        if input("Do you want to start over?\n"
                 "Press 1 for start over\n") == "1":
            self.__init__()
