class Question:
    answer = None

    def __init__(self, title, question_text, answer_lower_bound, answer_upper_bound,
                 translate_method=None, percentageanswer=False):
        self.percentageanswer = percentageanswer
        self.title = title
        self.question_text = question_text
        self.translate_method = translate_method
        self.answer_lower_bound = answer_lower_bound
        self.answer_upper_bound = answer_upper_bound

    def answer_question(self, answer):
        if self.translate_method is None and answer.isdigit():
            self.answer = int(answer)
            return True
        else:
            for answer in self.translate_method:
                if answer == self.answer:
                    self.answer = int(answer)
                    return True
        return False

    def __str__(self):
        return "Question: {}\n" \
               "Answer:  {}".format(self.question_text, self.answer)