## built-in libraries
import typing

## custom modules
from entities.testing_material import TestingMaterial
from entities.reading import Reading

from entities.synonym import Synonym

from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo

class Word:

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class.
    This class is also used to represent kana.
    
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, 
                incoming_id:int, 
                incoming_testing_material:typing.List[TestingMaterial],
                incoming_testing_material_answer_main:Synonym,
                incoming_testing_material_answer_main_all:typing.List[Synonym], 
                incoming_reading:Reading,
                incoming_incorrect_count:int,
                incoming_correct_count:int) -> None:

        """
        
        Initializes a new Word object.

        Parameters:
        incoming_id (int) : The ID of the Word.
        incoming_testing_material (list - TestingMaterial) : The TestingMaterial of the Word.
        incoming_testing_material_answer_main (Synonym) : The answer to the TestingMaterial of the Word, i.e. the dictionary definition of the Word.
        incoming_testing_material_answer_main_all (list - Synonym) : The list of all answers to the TestingMaterial of the Word.
        incoming_reading (Reading) : The Reading of the Word.
        incoming_incorrect_count (int) : The number of times the user answered the TestingMaterial incorrectly.
        incoming_correct_count (int) : The number of times the user answered the TestingMaterial correctly.

        """

        self.word_id:int = incoming_id

        self.testing_material:typing.List[TestingMaterial] = incoming_testing_material

        ## the answer to the testing_material, i.e. the dictionary definition of the Word
        self.testing_material_answer_main:Synonym = incoming_testing_material_answer_main

        ## the list of all answers to the testing_material
        self.testing_material_answer_all:typing.List[Synonym] = incoming_testing_material_answer_main_all

        ## the Reading of the Word
        self.reading:Reading = incoming_reading

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count:int = incoming_incorrect_count

        ## the number of times the user answer to testing_material was correct
        self.correct_count:int = incoming_correct_count

        ## the likelihood of the Word being selected for testing
        self.likelihood:float = 0.0

        ## the known typos of the Word
        self.typos: typing.List[Typo] = []

        ## the known incorrect typos of the Word
        self.incorrect_typos: typing.List[IncorrectTypo] = []
    
