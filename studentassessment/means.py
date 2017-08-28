import random


# single answer function
def answer_item(answers_num=1, distractors_num=1):
    """Simulate passing one task of the assessment

    :param answers_num: the number of the answers in the particular task
    :param distractors_num: the number of the distractors in the particular task
    :return: the number of the answers, the number of marked answers, the number of the distractors, the number of the non-marked distractors
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
    """Simulate single assessment


    :param items_num: the number of the tasks in the assessment
    :param assesst_props: assessment description: a list of dictionaries, each dictionary describes one task
    :param choice: does every dict in the assessment props describe one task of the assessment (True), or it corresponds to a set of tasks (False)
    :param score_function: a function that computes the score for te assessment
    :return: the number of the answers, the number of marked answers, the number of the distractors, the number of the non-marked distractors
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