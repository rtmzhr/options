from Questions.OurQuestions import *
from Nodes import NodeList


def init_questions(question_manager):
    question_manager.questions = NodeList(option_period)
    question_manager.questions.set_child(option_period, price_estimation)
    question_manager.questions.set_child(price_estimation, estimation_likelihood)
    question_manager.questions.set_child(estimation_likelihood, stock_increase_likelihood)
    question_manager.questions.set_child(stock_increase_likelihood, stock_decrease_likelihood)
    question_manager.questions.set_child(stock_decrease_likelihood, risk_appetite)





