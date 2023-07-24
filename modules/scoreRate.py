## built-in modules
import random
import typing

## custom modules
from modules.words import word
from modules.vocab import vocab
from modules.localHandler import localHandler
from modules.logger import logger

class scoreRate:

    """
    The scoreRate class is used to determine which "word" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers, etc.
    """

    ##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, handler:localHandler, logger:logger) -> None:

        """

        This method is used to initialize the scoreRate class.\n

        Parameters:\n
        handler (object - localHandler) : the local handler.\n
        logger (object - logger) : the logger object.\n

        Returns:\n
        None.\n
        
        """

        self.handler = handler

        self.logger = logger

##--------------------start-of-calculate_score()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def calculate_score(self, total_answer:int, correct_count:int) -> float:

        """
        
        Parameters:\n
        self (object - scoreRate) : the scoreRate object.\n
        total_answers (int) : total number of answers for the word.\n
        correct_count (int) : total number of correct answers for the word.\n

        Returns:\n
        selection_weight (float) : the chance of the word getting selected.\n
 
        """

        incorrect_weight = 2.0 
        answer_count_weight = 0.75  
        correct_count_weight = 0.5  

        incorrect_score = incorrect_weight * (total_answer - correct_count)
        answer_count_score = answer_count_weight * (1 / (total_answer + 1))
        correct_count_score = correct_count_weight * (1 / (correct_count + 1))

        selection_weight = incorrect_score + answer_count_score + correct_count_score

        return selection_weight
    
##--------------------start-of-get_kana_to_test()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_kana_to_test(self, kana_list:typing.List[word]) -> typing.Tuple[word, typing.List[str]]:

        """

        This method is used to determine which "kana" will be given to the user based on a multitude of factors, such as the number of answers, the number of correct answers, the number of incorrect answers, etc.\n

        Parameters:\n
        self (object - scoreRate): The scoreRate class object.\n
        kana_list (list - word): The list of kana we can test.\n

        Returns:\n
        kana_to_test (word): The kana we want to test.\n
        display_item_list (list - str): The list of display items. I.E. all the kana, their likelihoods, number of incorrect/correct answers.\n

        """

        self.logger.log_action("Getting Kana to test...")

        raw_score_list = []
        kana_scores = []
        display_item_list = []

        default_score = 0

        for kana_item in kana_list: 
            total_answer = kana_item.incorrect_count + kana_item.correct_count
            raw_score_list.append(total_answer)

            kana_score = default_score

            raw_score = kana_item.incorrect_count + kana_item.correct_count

            if(raw_score > 0):
                kana_score -= raw_score
            elif(raw_score < 0):
                kana_score += abs(raw_score)

            total_answer_score = raw_score / (raw_score + 1)
            kana_score *= (1.0 - total_answer_score)  ## Invert the score here

            kana_score += self.calculate_score(raw_score, kana_item.correct_count) 

            kana_scores.append(kana_score + 1.0)

        kana_to_test = random.choices(kana_list, weights=kana_scores)[0]

        for i, kana in enumerate(kana_list):
            kana.likelihood = round(((kana_scores[i] / sum(kana_scores)) * 100), 4)

            display_item = (
                f"\n---------------------------------\n"
                f"Likelihood: {kana.likelihood}%\n"
                f"Kana: {kana.testing_material}\n"
                f"Incorrect Guesses: {kana.incorrect_count}\n"
                f"Correct Guesses: {kana.correct_count}\n"
                f"ID: {kana.word_id}\n"
                f"---------------------------------"
            )

            display_item_list.append((kana.likelihood, display_item))

        ## Sort the display_item_list based on the likelihoods (in ascending order)
        display_item_list.sort(key=lambda item: item[0])

        ## Rearrange the display_item_list and add index numbers
        display_item_list = [
            str(i + 1) + " " + str(item[1]) for i, item in enumerate(display_item_list)
        ]

        self.logger.log_action(kana_to_test.testing_material + " was selected, likelihood : " + str(kana_to_test.likelihood) + ", id : " + str(kana_to_test.word_id))

        return kana_to_test, display_item_list
    
##--------------------start-of-get_vocab_to_test()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_vocab_to_test(self, vocab_list:typing.List[vocab]) -> typing.Tuple[vocab, typing.List[str]]:
        
        """

        This method is used to determine which "vocab" will be given to the user based on a multitude of factors, such as the number of answers, the number of correct answers, the number of incorrect answers, etc.\n

        Parameters:\n
        self (object - scoreRate): The scoreRate class object.\n
        vocab_list (list - vocab): The list of vocab we can test.\n

        Returns:\n
        vocab_to_test (vocab): The vocab we want to test.\n
        display_item_list (list - str): The list of display items. I.E. all the vocab, their likelihoods, number of incorrect/correct answers.\n
        
        """

        self.logger.log_action("Getting Vocab to test...")

        raw_score_list = []
        vocab_scores = []
        display_item_list = []

        default_score = 0

        for vocab_item in vocab_list:
            total_answer = vocab_item.incorrect_count + vocab_item.correct_count
            raw_score_list.append(total_answer)

        default_score = max(abs(int(x)) for x in raw_score_list) + 1

        for vocab_item in vocab_list: 
            vocab_score = default_score

            raw_score = vocab_item.incorrect_count + vocab_item.correct_count

            if(raw_score > 0):
                vocab_score -= raw_score
            elif(raw_score < 0):
                vocab_score += abs(raw_score)

            total_answer_score = raw_score / (raw_score + 1)
            vocab_score *= (1.0 - total_answer_score)  ## Invert the score here

            vocab_score += self.calculate_score(raw_score, vocab_item.correct_count) 

            vocab_scores.append(vocab_score + 1.0)

        vocab_to_test = random.choices(vocab_list, weights=vocab_scores)[0]

        for i, vocab in enumerate(vocab_list):
            vocab.likelihood = round(((vocab_scores[i] / sum(vocab_scores)) * 100), 4)

            display_item = (
                f"\n---------------------------------\n"
                f"Likelihood: {vocab.likelihood}%\n"
                f"Vocab: {vocab.testing_material}\n"
                f"Incorrect Guesses: {vocab.incorrect_count}\n"
                f"Correct Guesses: {vocab.correct_count}\n"
                f"ID: {vocab.word_id}\n"
                f"---------------------------------"
            )

            display_item_list.append((vocab.likelihood, display_item)) 

        ## Sort the display_item_list based on the likelihoods (in ascending order)
        display_item_list.sort(key=lambda item: item[0])

        ## Rearrange the display_item_list and add index numbers
        display_item_list = [
            str(i + 1) + " " + str(item[1]) for i, item in enumerate(display_item_list)
        ]

        self.logger.log_action(vocab_to_test.testing_material + " was selected, likelihood : " + str(vocab_to_test.likelihood) + ", id : " + str(vocab_to_test.word_id))

        return vocab_to_test, display_item_list