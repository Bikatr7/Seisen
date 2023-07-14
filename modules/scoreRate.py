## built-in modules
import random
import typing

## custom modules
from modules.words import word
from modules.vocab import vocab

from modules.localHandler import localHandler

class scoreRate:

    """
    
    The scoreRate class is used to determine which "word" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers etc.\n

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, handler:localHandler) -> None:

        """
        
        This method is used to initialize the scoreRate class.

        """
        
        ## sets up the localHandler
        self.handler = handler

##--------------------start-of-get_kana_to_test()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_kana_to_test(self, kana_list:typing.List[word]) -> typing.Tuple[word, typing.List[str]]:

        """
        
        This method is used to determine which "kana" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers etc.\n

        Parameters:\n
        self (object - scoreRate) : The scoreRate class object.\n
        kana_list (list - word) : The list of kana we can test.\n
        
        Returns:\n
        kana_to_test (word) : The kana we want to test.\n
        display_item_list (list - str) : The list of display items. I.E. all the kana, their likelihoods, number of incorrect/correct answers.\n

        """
        
        raw_score_list = []
        kana_scores = []
        display_item_list = []

        default_score = 0
        i = 0

        for kana in kana_list:
            total_answer = kana.incorrect_count + kana.correct_count
            raw_score_list.append(kana.correct_count - kana.incorrect_count)
            
        default_score = max(abs(int(x)) for x in raw_score_list) + 1

        for index, raw_score in enumerate(raw_score_list):
            kana_score = default_score

            if raw_score > 0:
                kana_score -= raw_score
            elif raw_score < 0:
                kana_score += abs(raw_score)

            total_answer_score = total_answer / (total_answer + 1)
            kana_score *= total_answer_score

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

            display_item_list.append(display_item)

        display_item_list.sort()
        display_item_list = list(map(lambda x: str(display_item_list.index(x) + 1) + " " + str(x), display_item_list))

        return kana_to_test, display_item_list
    
##--------------------start-of-get_vocab_to_test()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_vocab_to_test(self, vocab_list:typing.List[vocab]) -> typing.Tuple[vocab, typing.List[str]]:

        """
        
        This method is used to determine which "vocab" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers etc.\n

        Parameters:\n
        self (object - scoreRate) : The scoreRate class object.\n
        vocab_list (list - vocab) : The list of vocab we can test.\n
        
        Returns:\n
        vocab_to_test (vocab) : The vocab we want to test.\n
        display_item_list (list - str) : The list of display items. I.E. all the vocab, their likelihoods, number of incorrect/correct answers.\n

        """
        
        raw_score_list = []
        vocab_scores = []
        display_item_list = []

        default_score = 0
        i = 0

        for vocab in vocab_list:
            total_answer = vocab.incorrect_count + vocab.correct_count
            raw_score_list.append(vocab.correct_count - vocab.incorrect_count)
            
        default_score = max(abs(int(x)) for x in raw_score_list) + 1

        for index, raw_score in enumerate(raw_score_list):
            vocab_score = default_score

            if raw_score > 0:
                vocab_score -= raw_score
            elif raw_score < 0:
                vocab_score += abs(raw_score)

            total_answer_score = total_answer / (total_answer + 1)
            vocab_score *= total_answer_score

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

            display_item_list.append(display_item)

        display_item_list.sort()
        display_item_list = list(map(lambda x: str(display_item_list.index(x) + 1) + " " + str(x), display_item_list))

        return vocab_to_test, display_item_list
    
    