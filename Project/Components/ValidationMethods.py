
def validate_int_range(number_string, question, lower_bound, upper_bound, aspercentage=False):
    if number_string.isdigit() and lower_bound <= int(number_string) <= upper_bound:
        question.answer = int(number_string)
        if aspercentage:
            question.answer /= 100
        return True
    return False

