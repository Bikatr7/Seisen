## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## custom modules
from modules.typos import typo as typo_blueprint
from modules.typos import incorrectTypo as incorrect_typo_blueprint
from modules import util
from modules import words

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from modules.localHandler import localHandler

class vocab(words.word):

    """
    
    The vocab class is for testing material that is longer than a single kana. Inherits the word class.\n

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[str], incoming_incorrect_count:int, incoming_correct_count:int, incoming_furigana:str, incoming_kanji_flag:bool):

        """
        
        Initializes the vocab class\n

        Parameters:\n
        self (object - word) : the object being initialized.\n
        incoming_id (int) : the id of the vocab.\n
        incoming_testing_material (str) : the testing material of the vocab.\n
        incoming_testing_material_answer_main (str) : the main answer of the testing material.\n
        incoming_testing_material_answer_main_all (list - str) : the list of all answers to the testing material of the vocab.\n
        incoming_incorrect_count (int) : the number of incorrect guesses of the vocab.\n
        incoming_correct_count (int) : the number of correct guesses of the vocab.\n
        incoming_furigana (str) : the furigana of the vocab.\n
        incoming_kanji_flag (bool) : if the vocab contains kanji or not.\n

        Returns:\n
        None.\n

        """
        
        super().__init__(incoming_id, incoming_testing_material, incoming_testing_material_answer_main, incoming_testing_material_answer_main_all, incoming_incorrect_count, incoming_correct_count)

        self.furigana = incoming_furigana

        self.isKanji = incoming_kanji_flag

        self.word_type = 3