## Built-in Libraries
import typing

## Custom Modules
from entities.entity import Entity

from entities.testing_material import TestingMaterial
from entities.reading import Reading

from entities.synonym import Synonym

from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo

class Word(Entity):

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class.
    This class is also used to represent kana.
    
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, 
                id:int, 
                testing_material:typing.List[TestingMaterial],
                answers:typing.List[Synonym], 
                readings:typing.List[Reading],
                correct_count:int,
                incorrect_count:int) -> None:

        """
        
        Initializes a new Word object.

        Parameters:
        id (int) : The ID of the Word.
        testing_material (list - TestingMaterial) : The testing material of the Word.
        answers (list - Synonym) : The answers of the Word.
        readings (list - Reading) : The readings of the Word.
        correct_count (int) : The number of times the Word has been answered correctly.
        incorrect_count (int) : The number of times the Word has been answered incorrectly.

        """

        super().__init__(id)

        self.testing_material:typing.List[TestingMaterial] = testing_material
        self.main_testing_material:TestingMaterial = testing_material[0]

        self.answers:typing.List[Synonym] = answers
        self.main_answer:Synonym = answers[0]

        self.readings:typing.List[Reading] = readings
        self.main_reading:Reading = readings[0]

        self.typos: typing.List[Typo] = []
        self.incorrect_typos: typing.List[IncorrectTypo] = []

        self.correct_count:int = correct_count
        self.incorrect_count:int = incorrect_count

        self.likelihood:float = 0.0