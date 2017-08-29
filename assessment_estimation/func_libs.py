import random


def answer_item(answers_num=1, distractors_num=1):
    """
    Answer an item in random way considering the item consists of answers_num answers and distractors_num distractors
    :param answers_num: The number of answers (correct answers) in the item
    :param distractors_num: The number of distractors (incorrect answers) in the item
    :return: four integer numbers: the whole number of the answers, the number of the answers the function 'checked' as
      correct, the whole number of the distrcators, the number of the distractors the function 'didn't checked'
    """
    correct_answers = random.sample(range(answers_num + distractors_num), answers_num)
    user_answers = random.sample(range(answers_num + distractors_num),
                                 1 if answers_num == 1 else random.choice(range(answers_num + distractors_num)))

    correct_answers_num = 0
    correct_distractors_num = 0
    for i in range(answers_num + distractors_num):
        correct_answers_num += 1 if i in correct_answers and i in user_answers else 0
        correct_distractors_num += 1 if i not in correct_answers and i not in user_answers else 0

    return answers_num, correct_answers_num, distractors_num, correct_distractors_num


def assesst(items_num=12, assesst_props=[{'answers_num': 1, 'distractors_num': 1}], choice=False,
            score_function=lambda answers_num, correct_answers_num, distractors_num, correct_distractors_num:
            float(correct_answers_num + correct_distractors_num) / float(answers_num + distractors_num)):
    """
    Calculate the score of the assessment answered by random
    :param items_num: the number of the item in the assessment
    :param assesst_props: the list of the dicts each of them contains answers num and distractors num. If the choice
    is False each item would be formed from randomly choosen dict.  In other case each dict corresponds one item.
    :param choice: Is the number of the dicts in assesst_props corresponds the number of the items in the assessment
    :param score_function: the function that calculates the score from whole number of answers, 'checked' number of
    answers, whole distractors number and the 'not checked' distractors number
    :return: The score of the test
    """
    if choice and len(assesst_props) != items_num:
        raise KeyError('The length of the assesst_props and the items_num should be the same!')

    answers_num, correct_answers_num, distractors_num, correct_distractors_num = 0, 0, 0, 0
    for i in range(items_num):
        cur_item = random.choice(assesst_props)

        if choice:
            assesst_props.remove(cur_item)

        a_num, c_a_num, d_num, c_d_num = answer_item(cur_item['answers_num'], cur_item['distractors_num'])
        answers_num += a_num
        correct_answers_num += c_a_num
        distractors_num += d_num
        correct_distractors_num += c_d_num

    return score_function(answers_num, correct_answers_num, distractors_num, correct_distractors_num)