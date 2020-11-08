from Project.Components.Nodes import *


class QuestionManger:

    def __init__(self, questions_array, welcome_message=''):
        self.answers = {}
        self.welcome_message = welcome_message
        init_questions(self, questions_array)
        self.start()

    def start(self):
        print(self.welcome_message)
        qs_itr = self.questions.root
        while qs_itr is not None:
            answer = input(qs_itr.data.question_text)
            if qs_itr.data.translate_method is not None:
                while not qs_itr.data.translate_method(answer, qs_itr.data,
                                                       qs_itr.data.answer_lower_bound, qs_itr.data.answer_upper_bound,
                                                       qs_itr.data.percentageanswer):
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
