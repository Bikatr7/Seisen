## built-in modules
import random
import typing
import msvcrt

## custom modules
from modules.words import word
from modules.vocab import vocab
from modules.localHandler import localHandler

class scoreRate:

    """

    The scoreRate class is used to determine which "word" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers, etc.
    
    """

    ##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, handler:localHandler) -> None:

        """

        This method is used to initialize the scoreRate class.\n

        Parameters:\n
        handler (object - localHandler) : the local handler.\n

        Returns:\n
        None.\n
        
        """

        self.handler = handler

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

        self.handler.file_ensurer.logger.log_action("Getting Kana to test...")

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

        self.handler.file_ensurer.logger.log_action(kana_to_test.testing_material + " was selected, likelihood : " + str(kana_to_test.likelihood) + ", id : " + str(kana_to_test.word_id))

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

        self.handler.file_ensurer.logger.log_action("Getting Vocab to test...")

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

        self.handler.file_ensurer.logger.log_action(vocab_to_test.testing_material + " was selected, likelihood : " + str(vocab_to_test.likelihood) + ", id : " + str(vocab_to_test.word_id))

        return vocab_to_test, display_item_list
    
##--------------------start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def levenshtein(self, string_one:str, string_two:str) -> int:

        """

        Compares two strings for similarity.\n

        Parameters:\n
        self (object - scoreRate): The scoreRate class object.\n
        string_one (str) : the first string to compare.\n
        string_two (str) : the second string to compare.\n

        Returns:\n
        distance[sLength1][sLength2] (int) : the minimum number of single-character edits required to transform string_one into string_two.\n

        """

        sLength1, sLength2 = len(string_one), len(string_two)
        distance = [[0] * (sLength2 + 1) for _ in range(sLength1 + 1)]
        
        for i in range(sLength1 + 1):
            distance[i][0] = i

        for ii in range(sLength2 + 1):
            distance[0][ii] = ii

        for i in range(1, sLength1 + 1):
            for ii in range(1, sLength2 + 1):

                if(string_one[i - 1] == string_two[ii - 1]):
                    cost = 0
                else:
                    cost = 1

                distance[i][ii] = min(distance[i - 1][ii] + 1, distance[i][ii- 1] + 1, distance[i - 1][ii - 1] + cost)

                if(i > 1 and ii > 1 and string_one[i-1] == string_two[ii-2] and string_one[i-2] == string_two[ii-1]):
                    distance[i][ii] = min(distance[i][ii], distance[i-2][ii-2] + cost)

        return distance[sLength1][sLength2]

##--------------------start-of-get_intended_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_intended_answer(self, typo:str, correct_answers:typing.List[str]) -> str:

        """
        
        When a typo has been previously encountered, we need to determine what they were trying to type and return that instead.\n

        Parameters:\n
        self (object - scoreRate) : The scoreRate class object.\n
        typo (str) : the typo the user made.\n
        correct_answers (list - str) : list of correct answers the typo could match.\n

        Returns:\n
        closest_string (str) : the string the user was trying to type.\n

        """

        closest_distance = float('inf')
        closest_string = ""

        for string in correct_answers:
            distance = self.levenshtein(typo, string)
            if(distance < closest_distance):
                closest_distance = distance
                closest_string = string

        return closest_string

##--------------------start-of-check_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_typo(self, word:word, user_guess:str, prompt:str, handler:localHandler) -> str:  

        """

        checks if a user_guess is a typo or not\n

        Parameters:\n
        self (object - scoreRate): The scoreRate class object.\n
        word (object - word) : the word we're checking typos for.\n
        user_guess (str) : the user's guess.\n
        prompt (str) : the prompt that was given to the user.\n
        handler (object - localHandler) : the localHandler object.\n
        
        Returns:\n
        final_answer (string) the user's final answer after being corrected for typos.\n

        """

        min_distance = 3
        lowest_distance = 3

        closest_match = None

        final_answer = user_guess

        typos = [typo.typo_value for typo in word.typos]
        incorrect_typos = [incorrect_typo.incorrect_typo_value for incorrect_typo in word.incorrect_typos]

        if(user_guess in typos):
            possible_intended_answers = [csep.csep_value for csep in word.testing_material_answer_all]
            return self.get_intended_answer(user_guess, possible_intended_answers )
        elif(user_guess in incorrect_typos):
            return user_guess

        for correct_answer in word.testing_material_answer_all:

            new_distance = self.levenshtein(user_guess, correct_answer.csep_value)

            if(new_distance < min_distance and new_distance < lowest_distance):
                lowest_distance = new_distance
                closest_match = correct_answer.csep_value

        if(closest_match is not None):

            handler.toolkit.clear_console()

            prompt += "\nDid you mean : " + closest_match + "? Press 1 to Confirm or 2 to Decline.\n"
        
            print(prompt)

            userA = int(self.handler.toolkit.input_check(4 ,str(msvcrt.getch().decode()), 2, prompt))
        
            self.handler.toolkit.clear_console()

            if(userA == 1):

                final_answer = closest_match

                word.log_new_typo(user_guess, handler)

                return final_answer
        
            else:
                word.log_new_incorrect_typo(user_guess, handler)

        
        return final_answer
    
##--------------------start-of-check_answers_word()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_answers_word(self, word:word, user_guess:str, prompt:str, handler:localHandler) -> typing.Tuple[typing.Union[bool ,None], str]: 

        """
        
        Checks if the user_guess is correct or incorrect.\n

        Parameters:\n
        self (object - scoreRate): The scoreRate class object.\n
        word (object - word) : the word we're checking answers for.\n
        user_guess (str) : the user's guess.\n
        prompt (str) : the prompt that was given to the user.\n
        handler (object - localHandler) : the localHandler object.

        Returns:\n
        bool or None : if the user's guess is correct or incorrect, or a None value iof the user decided to skip the question.\n 
        user_guess (str) : the user's guess after being corrected for typos.\n

        """

        answers = [value.csep_value for value in word.testing_material_answer_all]

        if(user_guess == 'q'): ## if the user wants to quit the program do so
            self.handler.toolkit.exit_seisen()
        
        if(user_guess not in answers and user_guess != 'z' and user_guess.strip() != ''): ## checks if user_guess is a typo
            user_guess = self.check_typo(word, user_guess, prompt, handler)

        if(user_guess in answers): 
            return True, user_guess
        
        elif(user_guess != 'z'): 
            return False, user_guess
        
        else: ## z indicates the user is skipping the word
            return None, user_guess
    
