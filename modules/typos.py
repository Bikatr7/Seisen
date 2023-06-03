
class typo:

    '''

    The typo class is used to represent typos the user makes.
        
    '''

    def __init__(self, incoming_word_type, incoming_typo_id , incoming_word_id, incoming_typo_value):

        self.word_type = incoming_word_type

        self.typo_id  = incoming_typo_id

        self.word_id = incoming_word_id

        self.typo_value = incoming_typo_value


class incorrectTypo:

    '''

    The incorrectTypo class is used to represent typos the user makes but are not actually typos.
        
    '''

    def __init__(self, incoming_word_type, incoming_incorrect_typo_id , incoming_word_id, incoming_incorrect_typo_value):

        self.word_type = incoming_word_type

        self.typo_id  = incoming_incorrect_typo_id

        self.word_id = incoming_word_id

        self.typo_value = incoming_incorrect_typo_value