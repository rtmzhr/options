from Project.Managers.QuestionManager import QuestionManger
from Project.Managers.OptionsManager import OptionsManager
from Project.Simulator import simulate


class Consultant:
    def __init__(self):
        self.question_manager = QuestionManger()
        self.question_manager.start()
        self.options_manager = OptionsManager(self.question_manager.answers)
        self.options_manager.start()
        self.simulate()

    def simulate(self):
        simulate(self.options_manager)
        if input("Do you want to start over?\n"
                 "Press 1 for start over\n") == "1":
            self.__init__()
