import numpy as np
from Project.Options.OptionTypes import PutOption, CallOption
from Project.CurrentStockPrice import current_stock_price
average_growth_per_year = 0.2


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
        self.center = self.estimated_price * (1 - self.likelihood) + self.estimated_price_by_user * self.likelihood
        self.offset = (14 + 2 * self.option_period) * ( (1 / self.risk_appetite) * \
            np.array([1 + self.increase_prob * (1 - self.decrease_prob), 1 + self.decrease_prob * (1 - self.increase_prob)]))
        self.execute()

    def execute(self):
        if (self.decrease_prob < 0.5 and self.increase_prob < 0.5) or self.risk_appetite >= 2 or \
                np.abs(self.decrease_prob - self.increase_prob < 0.35):
            self.execute_iron_codor()
        elif self.increase_prob - self.decrease_prob > 0.35:
            self.execute_up()
        else:
            self.execute_down()

    def execute_iron_codor(self):
        self.execute_down()
        self.execute_up()

    def execute_up(self):
        self.sell_put(int(self.offset[1]))
        self.buy_put(int(self.offset[1]) + 1)

    def execute_down(self):
        self.buy_call(int(self.offset[0]) + 1)
        self.sell_call(int(self.offset[0]))

    def buy_call(self, offset):
        self.option_manager.options_list.append(CallOption("buy", self.option_manager.data, offset, self.center))

    def sell_call(self, offset):
        self.option_manager.options_list.append(CallOption("sell", self.option_manager.data, offset, self.center))

    def buy_put(self, offset):
        self.option_manager.options_list.append(PutOption("buy", self.option_manager.data, offset, self.center))

    def sell_put(self, offset):
        self.option_manager.options_list.append(PutOption("sell", self.option_manager.data, offset, self.center))


