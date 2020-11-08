from Project.Components.Strategies import *
from Project.Components.Managers.DataManager import option_data


class OptionsManager:
    def __init__(self, answers):
        self.answers = answers
        self.adjust_data()
        self.options_list = []
        self.total_cost = 0
        self.start()

    def adjust_data(self):
        option_data.data = option_data.data.replace('-', 0)

    def start(self):
        if input("For Choosing Options Manually Pres 1, Otherwise Press 2\n") == "1":
            s = Manually(self)
            s.execute()
        else:
            s = IronCodorStrategy(self)
            s.execute()
        return self.calc_total_cost()

    def calc_total_cost(self):
        for option in self.options_list:
            self.total_cost += option.get_cost()
        return self.total_cost

    def calc_future_total_profit(self, future_strike):
        overall_profit = 0
        for option in self.options_list:
            overall_profit += option.get_profit(future_strike)
        return overall_profit

    def simulate_profit(self, strike_after_option_period):
        return self.calc_future_total_profit(strike_after_option_period) - self.total_cost

    def __str__(self):
        text = ''
        index = 1
        for opt in self.options_list:
            text += "{}) {}\n".format(index, opt)
            index += 1
        text += "Total cost = {}$\n".format(self.total_cost)
        return text
