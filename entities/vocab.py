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
                id:int, 
                testing_material:typing.List[TestingMaterial],
                answers:typing.List[Synonym], 
                readings:typing.List[Reading],
                correct_count:int,
                incorrect_count:int
                ) -> None:
        
        """
        
        Initializes a new Vocab object.

        Parameters:
        id (int) : The ID of the Vocab.
        testing_material (list - TestingMaterial) : The testing material of the Vocab.
        answers (list - Synonym) : The answers of the Vocab.
        readings (list - Reading) : The readings of the Vocab.
        correct_count (int) : The number of times the Vocab has been answered correctly.
        incorrect_count (int) : The number of times the Vocab has been answered incorrectly.
        
        """

        super().__init__(id, testing_material, answers, readings, correct_count, incorrect_count)