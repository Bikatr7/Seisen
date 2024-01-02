## built-in libraries
import typing

## custom modules
from entities.synonym import Synonym
from entities.word import Word

class Vocab(Word):

    """
    
    The Vocab class is for testing material that is longer than a single kana. Inherits the Word class.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_romaji:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[Synonym], incoming_furigana:str, incoming_incorrect_count:int,incoming_correct_count:int, incoming_kanji_flag:bool):

        """
        
        Initializes the Vocab class.

        Parameters:
        incoming_id (int) : The ID of the Vocab.
        incoming_testing_material (str) : The testing material of the Vocab.
        incoming_romaji (str) : The romaji of the Vocab.
        incoming_testing_material_answer_main (str) : The main answer of the testing material.
        incoming_testing_material_answer_main_all (list - csep) : The list of all answers to the testing material of the Vocab.
        incoming_furigana (str) : The furigana of the Vocab.
        incoming_incorrect_count (int) : The number of incorrect guesses of the Vocab.
        incoming_correct_count (int) : The number of correct guesses of the Vocab.
        incoming_kanji_flag (bool) : If the Vocab contains kanji or not.
        
        """
        
        super().__init__(incoming_id, incoming_testing_material, incoming_testing_material_answer_main, incoming_testing_material_answer_main_all, incoming_incorrect_count, incoming_correct_count)

        self.romaji:str = incoming_romaji

        self.furigana:str = incoming_furigana

        self.is_kanji:bool = incoming_kanji_flag

        self.word_type:str = "vocab"