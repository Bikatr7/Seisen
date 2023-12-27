## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## custom modules
from entities.csep import csep

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from entities.typo import Typo
    from entities.incorrect_typo import IncorrectTypo

class word:

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class.\n
    Kana also uses this class.\n
    
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[csep], incoming_incorrect_count:int, incoming_correct_count:int) -> None:

        """
        
        Initializes the word class.

        Parameters:
        incoming_id (int) : the id of the word.
        incoming_testing_material (str) : the testing material of the word.
        incoming_testing_material_answer_main (str) : the main answer of the testing material.
        incoming_testing_material_answer_main_all (list - str) : the list of all answers to the testing material of the word.
        incoming_incorrect_count (int) : the number of incorrect guesses of the word.
        incoming_correct_count (int) : the number of correct guesses of the word.

        """

        ## the id of the word
        self.word_id:int = incoming_id

        ## the thing being tested
        self.testing_material:str = incoming_testing_material

        ## the answer to the testing_material, i.e. the dictionary definition of the word
        self.testing_material_answer_main:str = incoming_testing_material_answer_main

        ## the list of all answers to the testing_material
        self.testing_material_answer_all:typing.List[csep] = incoming_testing_material_answer_main_all

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count:int = incoming_incorrect_count

        ## the number of times the user answer to testing_material was correct
        self.correct_count:int = incoming_correct_count

        ## the type of the word
        self.word_type:str = "2" ## is currently numerical, plan to change this later

        ## the likelihood of the word being selected for testing
        self.likelihood:float = 0.0

        ## the known typos of the word
        self.typos: typing.List[Typo] = []

        ## the known incorrect typos of the word
        self.incorrect_typos: typing.List[IncorrectTypo] = []
    
