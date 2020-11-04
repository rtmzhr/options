from Project.Components.Question import Question
from Project.Components.ValidationMethods import *

option_period = Question("option period",
                         "How many months do you want to have options?"
                         "\nPlease write an Integer between 1 - 4\n",
                         one_to_four_range)

options_budget = Question("options budget",
                          "How much money you wish to invest?\nPlease write an Integer\n",
                          validate_general_number)

price_estimation = Question("price estimation",
                            "What do you think the price of the stock will be then?\n"
                            "Please write an Integer\n",
                            validate_general_number)

estimation_likelihood = Question("estimation likelihood",
                                 "What are the chances the stock will reach your estimation?\nPlease write an Integer "
                                 "percentage %\n",
                                 validate_percentage_number)

risk_appetite = Question("risk appetite",
                         "What is the risk level you wish to peruse?\n"
                         "Please Choose 4-Extreme  3-High  2-Medium  1-Low\n",
                         one_to_four_range)

stock_increase_likelihood = Question("stock increase likelihood",
                                     "Whats are the chances the stock price will increase in this period?\nPlease "
                                     "write an Integer percentage %\n",
                                     validate_percentage_number)

stock_decrease_likelihood = Question("stock decrease likelihood",
                                     "Whats are the chances the stock price will decrease in this period?\n"
                                     "Please write am Integer percentage %\n",
                                     validate_percentage_number)

questions_array = [option_period, price_estimation, estimation_likelihood,
                   stock_increase_likelihood, stock_decrease_likelihood, risk_appetite]