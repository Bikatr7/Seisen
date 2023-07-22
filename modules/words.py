## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## custom modules
from modules.typos import typo as typo_blueprint
from modules.typos import incorrectTypo as incorrect_typo_blueprint

from modules.csep import csep

from modules import util

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from modules.localHandler import localHandler

class word:

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class.\n
    Kana also uses this class.\n
    
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[csep], incoming_incorrect_count:int, incoming_correct_count:int) -> None:

        """
        
        Initializes the word class\n

        Parameters:\n
        self (object - word) : the object being initialized.\n
        incoming_id (int) : the id of the word.\n
        incoming_testing_material (str) : the testing material of the word.\n
        incoming_testing_material_answer_main (str) : the main answer of the testing material.\n
        incoming_testing_material_answer_main_all (list - str) : the list of all answers to the testing material of the word.\n
        incoming_incorrect_count (int) : the number of incorrect guesses of the word.\n
        incoming_correct_count (int) : the number of correct guesses of the word.\n

        Returns:\n
        None.\n

        """

        ## the id of the word
        self.word_id = incoming_id

        ## the thing being tested
        self.testing_material = incoming_testing_material

        ## the answer to the testing_material, i.e. the dictionary definition of the word
        self.testing_material_answer_main = incoming_testing_material_answer_main

        ## the list of all answers to the testing_material
        self.testing_material_answer_all = incoming_testing_material_answer_main_all

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count = incoming_incorrect_count

        ## the number of times the user answer to testing_material was correct
        self.correct_count = incoming_correct_count

        ## the type of the word
        self.word_type = "2" ## is currently numerical, plan to change this later

        ## the likelihood of the word being selected for testing
        self.likelihood = 0.0

        ## the known typos of the word
        self.typos = []

        ## the know incorrect typos of the word
        self.incorrect_typos = []

##--------------------start-of-log_correct_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_correct_answer(self, handler:localHandler) -> None:

        """

        Logs a correct answer to the word.\n

        Parameters:\n
        self (object - word) : the word being tested.\n

        Returns:\n
        None.\n
        
        """

        ## where the correct count index is in the
        CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 5
        KANA_ID_FILE_INDEX_LOCATION = 1

        kana_ids = []

        line_to_write_to = 0

        self.correct_count += 1

        with open(handler.kana_path, 'r', encoding="utf-8") as file:
            kana_lines = file.readlines()

        for i, line in enumerate(kana_lines):
            kana_ids.append(util.read_sei_file(handler.kana_path, i+1, KANA_ID_FILE_INDEX_LOCATION))
                            
        ## line returned needs to be incremented by one to match file
        line_to_write_to = kana_ids.index(str(self.word_id)) + 1

        util.edit_sei_line(handler.kana_path, line_to_write_to, CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION , self.correct_count)

        handler.logger.log_action("Logged a correct answer for " + self.testing_material + ", id : " + str(self.word_id))

##--------------------start-of-log_incorrect_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_incorrect_answer(self ,handler:localHandler) -> None:

        """
        
        Logs an incorrect answer to the word.\n

        Parameters:\n
        self (object - word) : the object being tested.\n

        Returns:\n
        None.\n
        
        """

        ## where the incorrect count index is in the
        INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 4

        kana_ids = []

        line_to_write_to = 0

        self.incorrect_count += 1

        with open(handler.kana_path, 'r', encoding="utf-8") as file:
            kana_lines = file.readlines()

        for i, line in enumerate(kana_lines):
            kana_ids.append(util.read_sei_file(handler.kana_path, i+1,1))
                            
        ## line returned needs to be incremented by one to match file
        line_to_write_to = kana_ids.index(str(self.word_id)) + 1

        util.edit_sei_line(handler.kana_path, line_to_write_to, INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION , self.incorrect_count)

        handler.logger.log_action("Logged an incorrect answer for " + self.testing_material + ", id : " + str(self.word_id))

##--------------------start-of-log_new_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_new_typo(self, typo:str, handler:localHandler) -> None:

        """

        Logs a new typo to the word.\n

        Parameters:\n
        self (object - word) : the word being tested\n
        typo (str) : the typo to be logged.\n
        handler (object - localHandler) : the localHandler object.\n

        Returns:\n
        None.\n
        
        """

        ## gets a new id for the typo
        new_typo_id = util.get_new_id(handler.get_list_of_all_ids(1))

        new_typo = incorrect_typo_blueprint(self.word_id, new_typo_id, typo , self.word_type)

        ## updates local storage so the typo will be saved
        util.write_sei_line(handler.kana_typos_path, [str(self.word_id), str(new_typo_id), str(new_typo.incorrect_typo_value), str(new_typo.word_type)])

        ## updates the current session with the typo
        self.typos.append(new_typo)

        handler.logger.log_action("Logged a typo : " + typo + " for " + self.testing_material + ", id : " + str(self.word_id))

##--------------------start-of-log_new_incorrect_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_new_incorrect_typo(self, incorrect_typo:str, handler:localHandler) -> None:

        """
        
        Logs a new incorrect typo to the word.\n

        Parameters:\n
        self (object - word) : the object being tested.\n
        incorrect_typo (str) : the incorrect_typo to be logged.\n
        handler (object - localHandler) : the localHandler object.\n
        
        """

        ## gets a new id for the incorrect typo
        new_incorrect_typo_id = util.get_new_id(handler.get_list_of_all_ids(2))

        new_incorrect_typo = incorrect_typo_blueprint(self.word_id, new_incorrect_typo_id, incorrect_typo , self.word_type)

        ## updates local storage so the incorrect typo will be saved
        util.write_sei_line(handler.kana_incorrect_typos_path, [str(self.word_id), str(new_incorrect_typo_id), str(new_incorrect_typo.incorrect_typo_value), str(new_incorrect_typo.word_type)])

        ## updates the current session with the incorrect typo
        self.incorrect_typos.append(new_incorrect_typo)

        handler.logger.log_action("Logged an incorrect typo : " + incorrect_typo + " for " + self.testing_material + ", id : " + str(self.word_id))

##--------------------start-of-check_answers_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_answers_kana(self, user_guess:str, prompt:str, handler:localHandler) -> tuple[bool | None, str]: 

        """
        
        Checks if the user_guess is correct or incorrect.\n

        Parameters:\n
        self (object - word) : the word we're checking answers for.\n
        user_guess (str) : the user's guess.\n
        prompt (str) : the prompt that was given to the user.\n
        handler (object - localHandler) : the localHandler object.

        Returns:\n
        bool or None : if the user's guess is correct or incorrect, or a None value iof the user decided to skip the question.\n 
        user_guess (str) : the user's guess after being corrected for typos.\n

        """

        if(user_guess == 'q'): # if the user wants to quit the program do so
            exit()
        
        if(user_guess not in self.testing_material_answer_all and user_guess != 'z' and user_guess.strip() != ''): ## checks if user_guess is a typo
            user_guess = util.check_typo(self, user_guess, prompt, handler)

        if(user_guess in self.testing_material_answer_all): 
            return True, user_guess
        
        elif(user_guess != 'z'): 
            return False, user_guess
        
        else: ## z indicates the user is skipping the word
            return None, user_guess
    
