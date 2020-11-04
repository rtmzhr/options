import numpy as np
from Project.Components.Managers.OptionTypes import *
from Project.Components.ValidationMethods import *
from Project.Components.Question import *
from Project.Components.Managers.QuestionManager import *
from Project.Consts.Stats import *


class Strategy:

    def __init__(self, option_manager):
        self.option_manager = option_manager
        self.option_period = option_manager.answers["option period"]
        self.likelihood = option_manager.answers["estimation likelihood"]
        self.increase_prob = option_manager.answers["stock increase likelihood"]
        self.decrease_prob = option_manager.answers["stock decrease likelihood"]
        self.risk_appetite = option_manager.answers["risk appetite"]
        self.estimated_price_by_user = option_manager.answers["price estimation"]
        self.estimated_price = ((1 + average_growth_per_year) ** (self.option_period / 12)) * current_stock_price
        data = self.option_manager.data
        self.strike_offset = (16 + 2 * (self.option_period - self.risk_appetite)) \
                             * np.array([self.increase_prob, self.decrease_prob])
        rounded_price = int(current_stock_price) - int(current_stock_price) % 5
        current_stock_price_index = int(data.index[data.iloc[:, 1] == rounded_price].to_numpy())
        lower_bound = data.iloc[current_stock_price_index - int(self.strike_offset[1]), 1]
        upper_bound = data.iloc[current_stock_price_index + int(self.strike_offset[0]), 1]
        self.lower_bound_index = int(data.index[data.iloc[:, 1] == lower_bound].to_numpy())
        self.upper_bound_index = int(data.index[data.iloc[:, 1] == upper_bound].to_numpy())

    def buy_call(self, strike):
        self.option_manager.options_list.append(BuyCallOption(self.option_manager.data, strike))

    def sell_call(self, strike):
        self.option_manager.options_list.append(SellCallOption(self.option_manager.data, strike))

    def buy_put(self, strike):
        self.option_manager.options_list.append(BuyPutOption(self.option_manager.data, strike))

    def sell_put(self, strike):
        self.option_manager.options_list.append(SellPutOption(self.option_manager.data, strike))


def get_option_choice(question):
    opt = input(question)
    while opt.isdigit() and 1 <= int(opt) <= 4:
        opt = input("Invalid Input! {}".format(question))
    return int(opt)


class Manually(Strategy):
    choose_opt_type_question = Question("option type", "Please Choose which open do you want\n"
                                                       "1 for Buy-Put    2 for Sell-Put\n"
                                        "3 for Buy-Call   4 for Sell-Call\n", one_to_four_range)
    choose_opt_strike_question = Question("option strike","what's the option's strike?\n"
                                          " Please write an Integer\n", validate_general_number)

    def __init__(self, option_manager):
        Strategy.__init__(self, option_manager)
        self.strategy_question_manager = QuestionManger([self.choose_opt_type_question,
                                                         self.choose_opt_strike_question])

    def execute(self):
        self.strategy_question_manager.start()
        if self.strategy_question_manager.answers["option type"] == 1:
            self.buy_put(self.strategy_question_manager.answers["option strike"])
        elif self.strategy_question_manager.answers["option type"] == 2:
            self.sell_put(self.strategy_question_manager.answers["option strike"])
        elif self.strategy_question_manager.answers["option type"] == 3:
            self.sell_call(self.strategy_question_manager.answers["option strike"])
        else:
            self.buy_call(self.strategy_question_manager.answers["option strike"])
        self.strategy_question_manager.reset_answers()
        if input("Do you want to choose another option?\n Press Y/N\n") == "Y":
            self.execute()


class IronCodorStrategy(Strategy):
    def __init__(self, option_manager):
        Strategy.__init__(self, option_manager)

    def execute(self):
        data = self.option_manager.data
        self.buy_put(data.iloc[self.lower_bound_index - 1, 1])
        self.sell_put(data.iloc[self.lower_bound_index, 1])
        self.sell_call(data.iloc[self.upper_bound_index, 1])
        self.buy_call(data.iloc[self.upper_bound_index + 1, 1])
