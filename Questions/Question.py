class Question:
    answer = None

    def __init__(self, title, question_text, translate_method=None):
        self.title = title
        self.question_text = question_text
        self.translate_method = translate_method

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