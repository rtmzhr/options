from Project.Components.Managers.QuestionManager import QuestionManger
from Project.Components.Managers.OptionsManager import OptionsManager
from Project.Components.Simulator import simulate
from Project.Components.Managers.DataManager import *


class Consultant:
    def __init__(self):
        welcome_message = "Hi!\n" \
                               "We will ask you a few questions to get to know you better\n" \
                               "The current Facebook stock is {}\n".format(current_stock_price)
        self.question_manager = QuestionManger(questions_array, welcome_message)
        option_data.set_options_date(self.question_manager.answers["option period"])
        self.options_manager = OptionsManager(self.question_manager.answers)
        self.simulate()

    def simulate(self):
        simulate(self.options_manager)
        if input("Do you want to start over?\n"
                 "Press 1 for start over\n") == "1":
            self.__init__()
