## built-in modules
from __future__ import annotations

import typing

## custom modules
from modules.typos import typo as typo_blueprint
from modules import util

if(typing.TYPE_CHECKING):
    from dataHandler import dataHandler

class word:

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class

    Kana also uses this class.
    
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[str], incoming_incorrect_count:int, incoming_correct_count:int) -> None:

        """
        
        Initializes the word class\n

        Parameters:\n
        self (object - word) : the object being initialized\n
        incoming_id (int) : the id of the word\n
        incoming_testing_material (str) : the testing material of the word\n
        incoming_testing_material_answer_main (str) : the main answer of the testing material\n
        incoming_testing_material_answer_main_all (list - str) : the list of all answers to the testing material of the word\n
        incoming_incorrect_count (int) : the number of incorrect guesses of the word\n
        incoming_correct_count (int) : the number of correct guesses of the word\n

        Returns:\n
        self (object - word) : the object being initialized\n

        """

        ## the id of the word
        self.word_id = incoming_id

        ## the thing being tested
        self.testing_material = incoming_testing_material

        ## the answer to the testing_material, i.e. the dictionary definition of the word
        self.testing_material_answer_main = incoming_testing_material_answer_main

        ## the list of all answers to the testing_material
        self.testing_material_answer_all = incoming_testing_material_answer_main_all
        self.testing_material_answer_all.append(self.testing_material_answer_main)

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count = incoming_incorrect_count

        ## the number of times the user answer to testing_material was correct
        self.correct_count = incoming_correct_count

        ## the type of the word
        self.word_type = 2 ## is currently numerical, plan to change this later

        ## the likelihood of the word being selected for testing
        self.likelihood = 0.0

        ## the known typos of the word
        self.typos = []

        ## the know incorrect typos of the word
        self.incorrect_typos = []

##--------------------start-of-log_correct_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_correct_answer(self) -> None:

        """

        Logs a correct answer to the word\n

        Parameters:\n
        self (object - word) : the object being tested\n

        Returns:\n
        None\n
        
        """

        self.correct_count += 1

##--------------------start-of-log_incorrect_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_incorrect_answer(self) -> None:

        """
        
        Logs an incorrect answer to the word\n

        Parameters:\n
        self (object - word) : the object being tested\n

        Returns:\n
        None\n
        
        """

        self.incorrect_count += 1

##--------------------start-of-log_new_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_new_typo(self, typo, handler:dataHandler) -> None:

        """

        Logs a new typo to the word\n

        Parameters:\n
        self (object - word) : the object being tested\n

        Returns:\n
        None\n
        
        """

        new_typo_id = util.get_new_id(handler.get_list_of_all_ids(1))

        new_typo = typo_blueprint(self.word_type, new_typo_id, self.word_id, typo)

        util.write_sei_line(handler.kana_typos_file, [str(self.word_id), str(new_typo_id), str(new_typo.typo_value), str(new_typo.word_type)])

        self.typos.append(new_typo)

##--------------------start-of-check_answers_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_answers_kana(self, user_guess:str, prompt:str, handler:dataHandler) -> tuple[bool | None, str]: 

        """
        
        Checks if the user_guess is correct or incorrect\n

        Parameters:\n
        self (object - word) : the word we're checking answers for\n
        user_guess (str) : the user's guess\n
        prompt (str) : the prompt that was given to the user\n

        Returns:\n
        bool or None : if the user's guess is correct or incorrect, or a None value iof the user decided to skip the question\n 
        user_guess (str) : the user's guess after being corrected for typos\n

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
    
