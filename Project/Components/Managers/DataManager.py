import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Project.Components.Question import Question
from Project.Components.ValidationMethods import validate_int_range

average_growth_per_year = 0.2


class OptionTrainingData:
    def __init__(self):
        self.data = pd.read_csv("Project/Data/4.csv")
        self.strikes_array = np.array(self.data["Strikes"]).astype('float')
        self.strikes_array = self.strikes_array.reshape((1, len(self.data.index)))[0]
        self.current_stock_price = 290

    def set_options_date(self, date_index):
        return

    def get_option_index(self, strike, offset=0):
        length = len(self.strikes_array)
        strike -= strike % 5
        return offset + binary_search(self.strikes_array, 0, length, strike)

    def get_option_price(self, strike, offset=0):
        return self.data.iloc[self.get_option_index(strike, offset), :].astype('float')


class OptionData:
    def __init__(self):
        self.html = None
        self.soup = None
        self.option_date_value = None
        self.data = None
        self.strikes_array = None

        chrome_option = Options()
        chrome_option.add_argument("--headless")
        self.url = 'https://finance.yahoo.com/quote/FB/options?p=FB&straddle=true'
        driver_path = "/Users/rotem_zecharia/chromdriver/chromedriver"
        self.driver = webdriver.Chrome(options=chrome_option, executable_path=driver_path)
        self.init_page(self.url)
        self.current_stock_price = float(
            self.soup.find('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)
        self.dates_tags = [entry for entry in
                           self.soup.find('select', {'class': 'Fz(s) H(25px) Bd Bdc($seperatorColor)'})]

    def init_page(self, url):
        self.driver.get(url)
        self.html = self.driver.execute_script('return document.body.innerHTML;')
        self.soup = BeautifulSoup(self.html, "html.parser")

    def get_dates_texts(self):
        dates = [month.text for month in self.dates_tags]
        question = "Choose Date:\n"
        i = -1
        for date in dates:
            i += 1
            question += "Press {} for {}\n".format(i, date)
        return question

    def set_options_date(self, date_index):
        self.option_date_value = self.dates_tags[date_index]['value']
        self.get_options_data()

    def get_options_data(self):
        url = 'https://finance.yahoo.com/quote/FB/options?p=FB&straddle=true&date={}'.format(self.option_date_value)
        self.init_page(url)
        calls = pd.DataFrame([entry.text for entry in self.soup.find_all('td', {
            'class': 'data-col0 Ta(end) Pstart(10px) call-in-the-money_Bgc($hoverBgColor)'
                     ' Bdstartw(8px) Bdstarts(s) Bdstartc(t) call-in-the-money_Bdstartc($linkColor)'})])
        strikes = pd.DataFrame(
            [entry.text for entry in self.soup.find_all(
                'td', {'class': "data-col5 Ta(c) Px(10px) BdX Bdc($seperatorColor)"})])
        puts = pd.DataFrame([entry.text for entry in self.soup.find_all('td', {
            'class': "data-col6 Ta(end) Pstart(10px) put-in-the-money_Bgc($hoverBgColor)"})])
        data = pd.concat([calls, strikes, puts], axis=1)
        data.columns = ["Calls", "Strikes", "Puts"]
        self.data = data
        self.strikes_array = np.array(strikes).astype('float')
        self.strikes_array = self.strikes_array.reshape((1, len(self.data.index)))[0]

    def get_option_index(self, strike, offset=0):
        length = len(self.strikes_array)
        strike -= strike % 5
        return offset + binary_search(self.strikes_array, 0, length, strike)

    def get_option_price(self, strike, offset=0):
        return self.data.iloc[self.get_option_index(strike, offset), :].astype('float')


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


if input("For Training Data Press 1\nFor Real Data Press 2\n") == "1":
    option_data = OptionTrainingData()
    option_period = Question("option period", "Press 4 to Start\n", 4, 4, validate_int_range)

else:
    option_data = OptionData()
    option_period = Question("option period", option_data.get_dates_texts(), 0,
                             len(option_data.dates_tags), validate_int_range)

current_stock_price = option_data.current_stock_price
price_estimation = Question("price estimation",
                            "What do you think the price of the stock will be then?\n"
                            "Please write an Integer\n", 100, 400, validate_int_range)

estimation_likelihood = Question("estimation likelihood",
                                 "What are the chances the stock will reach your estimation?\nPlease write an Integer "
                                 "percentage %\n", 0, 100, validate_int_range, True)

risk_appetite = Question("risk appetite",
                         "What is the risk level you wish to peruse?\n"
                         "Please Choose 4-Extreme  3-High  2-Medium  1-Low\n", 1, 4, validate_int_range)

stock_increase_likelihood = Question("stock increase likelihood",
                                     "Whats are the chances the stock price will increase in this period?\nPlease "
                                     "write an Integer percentage %\n", 0, 100, validate_int_range, True)

stock_decrease_likelihood = Question("stock decrease likelihood",
                                     "Whats are the chances the stock price will decrease in this period?\n"
                                     "Please write am Integer percentage %\n", 0, 100, validate_int_range, True)

questions_array = [option_period, price_estimation, estimation_likelihood,
                   stock_increase_likelihood, stock_decrease_likelihood, risk_appetite]
