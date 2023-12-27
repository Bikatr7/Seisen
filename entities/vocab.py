## built-in modules
import typing

## custom modules
from entities.csep import csep
from entities.words import word

class vocab(word):

    """
    
    The vocab class is for testing material that is longer than a single kana. Inherits the word class.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_romaji:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[csep], incoming_furigana:str, incoming_incorrect_count:int,incoming_correct_count:int, incoming_kanji_flag:bool):

        """
        
        Initializes the vocab class.

        Parameters:
        incoming_id (int) : the id of the vocab.
        incoming_testing_material (str) : the testing material of the vocab.
        incoming_romaji (str) : the romaji of the vocab.
        incoming_testing_material_answer_main (str) : the main answer of the testing material.
        incoming_testing_material_answer_main_all (list - str) : the list of all answers to the testing material of the vocab.
        incoming_furigana (str) : the furigana of the vocab.
        incoming_incorrect_count (int) : the number of incorrect guesses of the vocab.
        incoming_correct_count (int) : the number of correct guesses of the vocab.
        incoming_kanji_flag (bool) : if the vocab contains kanji or not.
        
        """
        
        super().__init__(incoming_id, incoming_testing_material, incoming_testing_material_answer_main, incoming_testing_material_answer_main_all, incoming_incorrect_count, incoming_correct_count)

        self.romaji:str = incoming_romaji

        self.furigana:str = incoming_furigana

        self.isKanji:bool = incoming_kanji_flag

        self.word_type:str = "3" ## really needs to be non-numerical, but this is fine for now