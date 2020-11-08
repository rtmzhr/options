class Option:
    def __init__(self, data, strike, column, amount):
        self.amount = amount
        self.price = float(data[data.iloc[:, 1] == strike].iloc[0, column])
        self.strike = strike

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
    def __init__(self, data, strike, amount):
        self.option_type = "put"
        Option.__init__(self, data, strike, 2, amount)


class BuyPutOption(PutOption):
    def __init__(self, data, strike, amount=1):
        self.option_execution = "buy"
        PutOption.__init__(self, data, strike, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike < self.strike:
            profit = (self.strike - future_strike) * self.amount
        return profit


class SellPutOption(PutOption):
    def __init__(self, data, strike, amount=1):
        self.option_execution = "sell"
        PutOption.__init__(self, data, strike, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike < self.strike:
            profit = (future_strike - self.strike) * self.amount
        return profit


class CallOption(Option):
    def __init__(self, data, strike, amount):
        self.option_type = "call"
        Option.__init__(self, data, strike, 0, amount)


class BuyCallOption(CallOption):
    def __init__(self, data, strike, amount=1):
        self.option_execution = "buy"
        PutOption.__init__(self, data, strike, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike > self.strike:
            profit = (future_strike - self.strike) * self.amount
        return profit


class SellCallOption(CallOption):
    def __init__(self, data, strike, amount=1):
        self.option_execution = "sell"
        PutOption.__init__(self, data, strike, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike > self.strike:
            profit = (self.strike - future_strike) * self.amount
        return profit