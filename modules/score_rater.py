## built-in libaries
import random
import typing
import msvcrt

## custom modules
from entities.word import word
from entities.vocab import vocab

from entities.typo import Typo as typo_blueprint
from entities.incorrect_typo import IncorrectTypo as incorrect_typo_blueprint

from modules.logger import Logger
from modules.toolkit import Toolkit
from modules.file_ensurer import FileEnsurer

from handlers.local_handler import LocalHandler
from handlers.file_handler import FileHandler

class ScoreRater:

    """

    The scoreRate class is used to determine which "word" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers, etc.
    
    """

##--------------------start-of-calculate_score()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def calculate_score(total_answer:int, correct_count:int) -> float:

        """
        
        Parameters:
        total_answers (int) : total number of answers for the word.
        correct_count (int) : total number of correct answers for the word.

        Returns:
        selection_weight (float) : the chance of the word getting selected.
 
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

    @staticmethod
    def get_kana_to_test(kana_list:typing.List[word]) -> typing.Tuple[word, typing.List[str]]:

        """

        This method is used to determine which "kana" will be given to the user based on a multitude of factors, such as the number of answers, the number of correct answers, the number of incorrect answers, etc.

        Parameters:
        kana_list (list - word): The list of kana we can test.

        Returns:
        kana_to_test (word): The kana we want to test.
        display_item_list (list - str): The list of display items. I.E. all the kana, their likelihoods, number of incorrect/correct answers.

        """

        Logger.log_action("Getting Kana to test...")

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

            kana_score += ScoreRater.calculate_score(raw_score, kana_item.correct_count) 

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

        Logger.log_action(kana_to_test.testing_material + " was selected, likelihood : " + str(kana_to_test.likelihood) + ", id : " + str(kana_to_test.word_id))

        return kana_to_test, display_item_list
    
##--------------------start-of-get_vocab_to_test()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_vocab_to_test(vocab_list:typing.List[vocab]) -> typing.Tuple[vocab, typing.List[str]]:
        
        """

        This method is used to determine which "vocab" will be given to the user based on a multitude of factors, such as the number of answers, the number of correct answers, the number of incorrect answers, etc.

        Parameters:
        vocab_list (list - vocab): The list of vocab we can test.

        Returns:
        vocab_to_test (vocab): The vocab we want to test.
        display_item_list (list - str): The list of display items. I.E. all the vocab, their likelihoods, number of incorrect/correct answers.
        
        """

        Logger.log_action("Getting Vocab to test...")

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

            vocab_score += ScoreRater.calculate_score(raw_score, vocab_item.correct_count) 

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

        Logger.log_action(vocab_to_test.testing_material + " was selected, likelihood : " + str(vocab_to_test.likelihood) + ", id : " + str(vocab_to_test.word_id))

        return vocab_to_test, display_item_list
    
##--------------------start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def levenshtein(string_one:str, string_two:str) -> int:

        """

        Compares two strings for similarity.

        Parameters:
        string_one (str) : the first string to compare.
        string_two (str) : the second string to compare.

        Returns:
        distance[sLength1][sLength2] (int) : the minimum number of single-character edits required to transform string_one into string_two.

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

    @staticmethod
    def get_intended_answer(typo:str, correct_answers:typing.List[str]) -> str:

        """
        
        When a typo has been previously encountered, we need to determine what they were trying to type and return that instead.

        Parameters:
        typo (str) : the typo the user made.
        correct_answers (list - str) : list of correct answers the typo could match.

        Returns:
        closest_string (str) : the string the user was trying to type.

        """

        closest_distance = float('inf')
        closest_string = ""

        for string in correct_answers:
            distance = ScoreRater.levenshtein(typo, string)
            if(distance < closest_distance):
                closest_distance = distance
                closest_string = string

        return closest_string

##--------------------start-of-check_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def check_typo(word:word, user_guess:str, prompt:str) -> str:  

        """

        hecks if the user's guess is a typo or not.

        Parameters:
        word (object - word) : the word we're checking typos for.
        user_guess (str) : the user's guess.
        prompt (str) : the prompt that was given to the user.
        
        Returns:
        final_answer (string) the user's final answer after being corrected for typos.

        """

        min_distance = 3
        lowest_distance = 3

        closest_match = None

        final_answer = user_guess

        typos = [typo.typo_value for typo in word.typos]
        incorrect_typos = [incorrect_typo.incorrect_typo_value for incorrect_typo in word.incorrect_typos]

        if(user_guess in typos):
            possible_intended_answers = [csep.csep_value for csep in word.testing_material_answer_all]
            return ScoreRater.get_intended_answer(user_guess, possible_intended_answers)
        elif(user_guess in incorrect_typos):
            return user_guess

        for correct_answer in word.testing_material_answer_all:

            new_distance = ScoreRater.levenshtein(user_guess, correct_answer.csep_value)

            if(new_distance < min_distance and new_distance < lowest_distance):
                lowest_distance = new_distance
                closest_match = correct_answer.csep_value

        if(closest_match is not None):

            Toolkit.clear_console()

            prompt += "\nDid you mean : " + closest_match + "? Press 1 to Confirm or 2 to Decline.\n"
        
            print(prompt)

            userA = int(Toolkit.input_check(4 ,str(msvcrt.getch().decode()), 2, prompt))
        
            Toolkit.clear_console()

            if(userA == 1):

                final_answer = closest_match

                ScoreRater.log_new_typo(word, typo=user_guess)

                return final_answer
        
            else:
                ScoreRater.log_new_incorrect_typo(word, incorrect_typo=user_guess)

        
        return final_answer
    
##--------------------start-of-check_answers_word()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def check_answers_word(word:word, user_guess:str, prompt:str) -> typing.Tuple[typing.Union[bool ,None], str]: 

        """
        
        Checks if the user_guess is correct or incorrect.

        Parameters:
        word (object - word) : the word we're checking answers for.
        user_guess (str) : the user's guess.
        prompt (str) : the prompt that was given to the user.
        handler (object - localHandler) : the localHandler object.

        Returns:
        bool or None : if the user's guess is correct or incorrect, or a None value iof the user decided to skip the question.
        user_guess (str) : the user's guess after being corrected for typos.

        """

        answers = [value.csep_value for value in word.testing_material_answer_all]

        if(user_guess == 'q'): ## if the user wants to quit the program do so
            FileEnsurer.exit_seisen()
        
        if(user_guess not in answers and user_guess != 'z' and user_guess.strip() != ''): ## checks if user_guess is a typo
            user_guess = ScoreRater.check_typo(word, user_guess, prompt)

        if(user_guess in answers): 
            return True, user_guess
        
        elif(user_guess != 'z'): 
            return False, user_guess
        
        else: ## z indicates the user is skipping the word
            return None, user_guess
    
##--------------------start-of-log_new_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def log_new_typo(word:word, typo:str) -> None:

        """

        Logs a new typo to the word.

        Parameters:
        word (object - word) : the word we're logging the typo for.
        typo (str) : the typo to be logged.

        """

        if(isinstance(word, vocab)):
            new_typo_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(3))
            path_to_write_to = FileEnsurer.vocab_typos_path

        else:
            new_typo_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(1))
            path_to_write_to = FileEnsurer.kana_typos_path

        new_typo = typo_blueprint(word.word_id, new_typo_id, typo, word.word_type)

        ## updates local storage so the typo will be saved
        FileHandler.write_sei_line(path_to_write_to, [str(word.word_id), str(new_typo_id), str(new_typo.typo_value), str(new_typo.word_type)])

        ## updates the current session with the typo
        word.typos.append(new_typo)

        Logger.log_action("Logged a typo : " + typo + " for " + word.testing_material + ", id : " + str(word.word_id))

##--------------------start-of-log_new_incorrect_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def log_new_incorrect_typo(word:word, incorrect_typo:str) -> None:

        """
        
        Logs a new incorrect typo to the word.

        Parameters:
        word (object - word) : the word we're logging the incorrect typo for.
        incorrect_typo (str) : the incorrect_typo to be logged.
        
        """

        if(isinstance(word, vocab)):
            new_incorrect_typo_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(4))
            path_to_write_to = FileEnsurer.vocab_incorrect_typos_path

        else:
            new_incorrect_typo_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(2))
            path_to_write_to = FileEnsurer.kana_incorrect_typos_path

        new_incorrect_typo = incorrect_typo_blueprint(word.word_id, new_incorrect_typo_id, incorrect_typo, word.word_type)

        ## updates local storage so the incorrect typo will be saved
        FileHandler.write_sei_line(path_to_write_to, [str(word.word_id), str(new_incorrect_typo_id), str(new_incorrect_typo.incorrect_typo_value), str(new_incorrect_typo.word_type)])

        ## updates the current session with the incorrect typo
        word.incorrect_typos.append(new_incorrect_typo)

        Logger.log_action("Logged an incorrect typo : " + incorrect_typo + " for " + word.testing_material + ", id : " + str(word.word_id))

##--------------------start-of-log_correct_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def log_correct_answer(word:word) -> None:

        """

        Logs a correct answer to the word.

        Parameters:
        word (object - word) : the word we're logging the correct answer for.
        
        """

        ## where the correct count index is in the file
        KANA_CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 5
        VOCAB_CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 7
    
        if(isinstance(word, vocab)):
            word_ids = LocalHandler.get_list_of_all_ids(6)
            path_to_write_to = FileEnsurer.vocab_actual_path
            index_location = VOCAB_CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION
        
        else:
            word_ids = LocalHandler.get_list_of_all_ids(5)
            path_to_write_to = FileEnsurer.kana_actual_path
            index_location = KANA_CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION

        line_to_write_to = 0

        ## current session update
        word.correct_count += 1
                            
        ## line returned needs to be incremented by one to match file
        line_to_write_to = word_ids.index(word.word_id) + 1

        ## updates local storage so the correct answer will be saved for future sessions
        FileHandler.edit_sei_line(path_to_write_to, line_to_write_to, index_location, str(word.correct_count))

        Logger.log_action("Logged a correct answer for " + word.testing_material + ", id : " + str(word.word_id))

##--------------------start-of-log_incorrect_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def log_incorrect_answer(word:word) -> None:

        """
        
        Logs an incorrect answer to the word.

        Parameters:\n
        word (object - word) : the word we're logging the incorrect answer for.
        
        """

        ## where the incorrect count index is in the file
        KANA_INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 4
        VOCAB_INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 6

        if(isinstance(word, vocab)):
            word_ids = LocalHandler.get_list_of_all_ids(6)
            path_to_write_to = FileEnsurer.vocab_actual_path
            index_location = VOCAB_INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION

        else:
            word_ids = LocalHandler.get_list_of_all_ids(5)
            path_to_write_to = FileEnsurer.kana_actual_path
            index_location = KANA_INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION

        line_to_write_to = 0

        ## current session update
        word.incorrect_count += 1

        ## line returned needs to be incremented by one to match file
        line_to_write_to = word_ids.index(word.word_id) + 1

        ## updates local storage so the incorrect answer will be saved for future sessions
        FileHandler.edit_sei_line(path_to_write_to, line_to_write_to, index_location, str(word.incorrect_count))

        Logger.log_action("Logged an incorrect answer for " + word.testing_material + ", id : " + str(word.word_id))