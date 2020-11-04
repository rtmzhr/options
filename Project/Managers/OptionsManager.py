import pandas as pd
from Project.Strategies.Strategies import Strategy
from Project.CurrentStockPrice import current_stock_price


class OptionsManager:
    def __init__(self, answers):
        self.current_stock_price = current_stock_price
        self.answers = answers
        path = "Data/{}.csv".format(answers["option period"])
        self.data = pd.read_csv(path)
        self.adjust_data()
        self.options_list = []
        self.total_cost = 0

    def adjust_data(self):
        self.data = self.data.replace('-', 0)
        calls = self.data.iloc[:, 0]
        strikes = self.data.iloc[:, 5]
        puts = self.data.iloc[:, 6]
        self.data = pd.concat([calls, strikes, puts], axis=1)

    def start(self):
        s = Strategy(self)
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
