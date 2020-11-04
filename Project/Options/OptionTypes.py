class Option:
    def __init__(self, buy_or_sell, data, center, amount):
        self.option_execution = buy_or_sell
        self.amount = amount
        rounded_center = int(center) - int(center) % 5
        self.strike_offset = int(data.index[data.iloc[:, 1] == rounded_center].to_numpy())

    def get_cost(self):
        x = -1
        if self.option_execution == "buy":
            x = 1
        return x * self.price * self.amount

    def get_profit_after_costs(self, future_strike):
        return self.get_profit(future_strike) - self.get_cost()

    def __str__(self):
        x = 1
        if self.option_execution == "buy":
            x = -1
        return "{} {} option :\n strike = {}    price per unit = {}$    amount = {}     total cost = {}$"\
            .format(self.option_execution, self.option_type,
                    self.strike, self.price, self.amount, self.get_cost())


class PutOption(Option):
    def __init__(self, buy_or_sell, data, offset, center, amount=1):
        self.option_type = "put"
        Option.__init__(self, buy_or_sell, data, center, amount)
        self.strike = int(data.iloc[self.strike_offset - offset, 1])
        self.price = float(data[data.iloc[:, 1] == self.strike].iloc[0, 2])
        print()

    def get_cost(self):

        return Option.get_cost(self)

    def get_profit(self, future_strike):
        profit = 0
        if self.option_execution == "buy" and future_strike < self.strike:
            profit = (self.strike - future_strike) * self.amount
        if self.option_execution == "sell" and future_strike < self.strike:
            profit = (future_strike - self.strike) * self.amount
        return profit


class CallOption(Option):
    def __init__(self, buy_or_sell, data, offset, center, amount=1):
        self.option_type = "call"
        Option.__init__(self, buy_or_sell, data, center, amount)
        self.strike = int(data.iloc[self.strike_offset + offset, 1])
        self.price = float(data[data.iloc[:, 1] == self.strike].iloc[0, 0])

    def get_cost(self):
        return Option.get_cost(self)

    def get_profit(self, future_strike):
        profit = 0
        if self.option_execution == "buy" and future_strike > self.strike:
            profit = (future_strike - self.strike) * self.amount
        elif self.option_execution == "sell" and future_strike > self.strike:
            profit = (self.strike - future_strike) * self.amount
        return profit
