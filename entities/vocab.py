## built-in libraries
import typing

## custom modules
from entities.reading import Reading
from entities.testing_material import TestingMaterial

from entities.synonym import Synonym
from entities.word import Word

class Vocab(Word):

    """
    
    The Vocab class is for testing material that is longer than a single kana. Inherits the Word class.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, 
                incoming_id:int, 
                incoming_testing_material:typing.List[TestingMaterial],
                incoming_testing_material_answer_main:Synonym,
                incoming_testing_material_answer_main_all:typing.List[Synonym], 
                incoming_incorrect_count:int,
                incoming_correct_count:int, 
                incoming_reading:Reading,
                incoming_kanji_flag:bool) -> None:

        """
        
        Initializes a new Vocab object.

        Parameters:
        incoming_id (int) : The ID of the Vocab.
        incoming_testing_material (list - TestingMaterial) : The TestingMaterial of the Vocab.
        incoming_testing_material_answer_main (Synonym) : The answer to the TestingMaterial of the Vocab, i.e. the dictionary definition of the Vocab.
        incoming_testing_material_answer_main_all (list - Synonym) : The list of all answers to the TestingMaterial of the Vocab.
        incoming_incorrect_count (int) : The number of times the user answered the TestingMaterial incorrectly.
        incoming_correct_count (int) : The number of times the user answered the TestingMaterial correctly.
        incoming_reading (Reading) : The Reading of the Vocab.
        incoming_kanji_flag (bool) : Whether or not the Vocab contains kanji.

        
        """
        
        super().__init__(incoming_id, incoming_testing_material, incoming_testing_material_answer_main, incoming_testing_material_answer_main_all, incoming_reading, incoming_incorrect_count, incoming_correct_count)

        self.is_kanji:bool = incoming_kanji_flag