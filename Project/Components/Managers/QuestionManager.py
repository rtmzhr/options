from Project.Consts.Stats import current_stock_price
from Project.Components.Nodes import *


class QuestionManger:

    def __init__(self, questions_array):
        self.welcome_message = "Hi!\n" \
                               "We will ask you a few questions to get to know you better\n" \
                               "The current Facebook stock is {}\n".format(current_stock_price)
        self.answers = {}
        init_questions(self, questions_array)

    def start(self):
        print(self.welcome_message)
        qs_itr = self.questions.root
        while qs_itr is not None:
            answer = input(qs_itr.data.question_text)
            if qs_itr.data.translate_method is not None:
                while not qs_itr.data.translate_method(answer, qs_itr.data):
                    answer = input("Invalid input!\n" + qs_itr.data.question_text)
            self.answers[qs_itr.data.title] = qs_itr.data.answer
            qs_itr = qs_itr.next

    def reset_answers(self):
        self.answers = {}


def init_questions(question_manager, qs_array):
    current = qs_array[0]
    question_manager.questions = NodeList(current)
    for i in range(1, len(qs_array)):
        question_manager.questions.set_child(current, qs_array[i])
        current = qs_array[i]