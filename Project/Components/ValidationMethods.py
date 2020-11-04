def validate_general_number(number, question):
    if number.isdigit():
        question.answer = int(number)
        return True
    return False


def one_to_four_range(number, question):
    if number.isdigit() and 1 <= int(number) <= 4:
        question.answer = int(number)
        return True
    return False


def validate_percentage_number(number, question):
    if number.isdigit() and 0 <= int(number) <= 100:
        question.answer = int(number) / 100
        return True
    return False
