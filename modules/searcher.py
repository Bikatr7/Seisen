## built-in libraries
import typing

## custom modules
from modules.toolkit import Toolkit

from entities.vocab import Vocab
from entities.testing_material import TestingMaterial
from entities.synonym import Synonym
from entities.reading import Reading
from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo

from handlers.local_handler import LocalHandler


##--------------------start-of-searcher------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Searcher:

    '''

    The search class is used to search for things in localHandler.
        
    '''

##--------------------start-of-get_vocab_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_vocab_print_item_from_id(vocab_id:int) -> str:

        """
        
        Gets a print item for a vocab given an id.

        Parameters:
        vocab_id (int) : the id of the vocab we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
            
        target_vocab = None

        for vocab in LocalHandler.vocab:
            if(vocab.word_id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise Searcher.IDNotFoundError(vocab_id)
        
        mini_testing_material_id_print = [str(testing_material.testing_material_id) for testing_material in target_vocab.testing_material_all]
        mini_testing_material_value_print = [str(testing_material.testing_material_value) for testing_material in target_vocab.testing_material_all]
        
        mini_reading_id_print = [str(reading.reading_id) for reading in target_vocab.readings]
        mini_reading_values_print = [str(reading.romaji_value) + "/" + str(reading.furigana_value) for reading in target_vocab.readings]

        mini_synonym_id_print = [str(synonym.synonym_id) for synonym in target_vocab.testing_material_answer_all]
        mini_synonym_value_print = [str(synonym.synonym_value) for synonym in target_vocab.testing_material_answer_all]

        print_item = (
            f"---------------------------------\n"
            f"ID: {target_vocab.word_id}\n"
            f"Incorrect Guesses: {target_vocab.incorrect_count}\n"
            f"Correct Guesses: {target_vocab.correct_count}\n"
            f"Testing Material ID(S) : {mini_testing_material_id_print}\n"
            f"Testing Material Value(s): {mini_testing_material_value_print}\n"
            f"Reading ID(S): {mini_reading_id_print}\n"
            f"Reading Value(s): {mini_reading_values_print}\n"
            f"Synonym ID(S): {mini_synonym_id_print}\n"
            f"Synonym Values(s): {mini_synonym_value_print}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_synonym_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_synonym_print_item_from_id(synonym_id:int) -> str:

        """
        
        Gets a print item for a synonym given a synonym id.

        Parameters:
        synonym_id (int) : The id of the synonym we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.\n
        
        """
        
        target_vocab = None
        target_synonym = None

        for vocab in LocalHandler.vocab:
            for synonym in vocab.testing_material_answer_all:
                if(synonym.synonym_id == synonym_id):
                    target_synonym = synonym
                    target_vocab = vocab

        if(target_synonym == None or target_vocab == None):
            raise Searcher.IDNotFoundError(synonym_id)
        
        mini_testing_material_value_print = [str(testing_material.testing_material_value) for testing_material in target_vocab.testing_material_all]
        mini_testing_material_id_print = [str(testing_material.testing_material_id) for testing_material in target_vocab.testing_material_all]

        print_item = (
            f"---------------------------------\n"
            f"Synonym: {target_synonym.synonym_value}\n"
            f"Synonym ID: {target_synonym.synonym_id}\n"
            f"VOCAB Testing Material: {mini_testing_material_value_print}\n"
            f"VOCAB Testing Material ID(s): {mini_testing_material_id_print}\n"
            f"VOCAB ID: {target_synonym.word_id}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_synonym_print_items_from_vocab_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_synonym_print_items_from_vocab_id(vocab_id:int) -> typing.List[str]:

        """
        
        Gets a print item for a synonym given a vocab id.

        Parameters:
        vocab_id (int) : the id of the vocab we are getting a print item for.

        Returns:
        print_items (list - str) : the print item for the id.
        
        """
            
        target_vocab = None
        print_items = []

        for vocab in LocalHandler.vocab:
            if(vocab.word_id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise Searcher.IDNotFoundError(vocab_id)
        
        for synonym in target_vocab.testing_material_answer_all:

            print_item = (
                f"---------------------------------\n"
                f"Synonym: {synonym.synonym_value}\n"
                f"Synonym ID: {synonym.synonym_id}\n"
                f"VOCAB: {target_vocab.testing_material_all}\n"
                f"VOCAB ID {synonym.word_id}\n"
                f"---------------------------------\n"
            )

            print_items.append(print_item)

        return print_items
    
##--------------------start-of-get_testing_material_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_testing_material_print_item_from_id(testing_material_id:int) -> str:

        """
        
        Gets a print item for a testing material given a testing material id.

        Parameters:
        testing_material_id (int) : the id of the testing material we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
        
        target_vocab = None
        target_testing_material = None

        for vocab in LocalHandler.vocab:
            for testing_material in vocab.testing_material_all:
                if(testing_material.testing_material_id == testing_material_id):
                    target_testing_material = testing_material
                    target_vocab = vocab

        if(target_testing_material == None or target_vocab == None):
            raise Searcher.IDNotFoundError(testing_material_id)
        
        mini_synonym_id_print = [str(synonym.synonym_id) for synonym in target_vocab.testing_material_answer_all]
        mini_synonym_value_print = [str(synonym.synonym_value) for synonym in target_vocab.testing_material_answer_all]

        print_item = (
            f"---------------------------------\n"
            f"Testing Material: {target_testing_material.testing_material_value}\n"
            f"Testing Material ID: {target_testing_material.testing_material_id}\n"
            f"VOCAB Synonym(s): {mini_synonym_value_print}\n"
            f"VOCAB Synonym ID(s): {mini_synonym_id_print}\n"
            f"VOCAB ID: {target_testing_material.word_id}\n"
            f"---------------------------------\n"
        )

        return print_item

##--------------------start-of-get_vocab_term_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_vocab_from_id(vocab_id:int) -> Vocab:

        """

        Gets a vocab given an id.

        Parameters:
        vocab_id (int) : the id of the vocab we are getting a print item for.

        Returns:
        vocab (Vocab) : the vocab for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            if(vocab.word_id == vocab_id):
                return vocab

        raise Searcher.IDNotFoundError(vocab_id)
    
##--------------------start-of-get_overlying_vocab_from_synonym_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_overlying_vocab_from_attribute_id(id:int, attribute_type:typing.Literal["synonym", "testing_material", "reading"]) -> Vocab:

        """

        Gets a vocab given an id.

        Parameters:
        id (int) : the id of the attribute we are getting a print item for.
        attribute_type (str) : the type of attribute we are getting a print item for.

        Returns:
        vocab (Vocab) : the vocab for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:

            if(attribute_type == "synonym"):
                for synonym in vocab.testing_material_answer_all:
                    if(synonym.synonym_id == id):
                        return vocab
                    
            elif(attribute_type == "testing_material"):
                for testing_material in vocab.testing_material_all:
                    if(testing_material.testing_material_id == id):
                        return vocab
                    
            elif(attribute_type == "reading"):
                for reading in vocab.readings:
                    if(reading.reading_id == id):
                        return vocab

        raise Searcher.IDNotFoundError(id)
    
##--------------------start-of-get_synonym_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_synonym_from_id(synonym_id:int) -> Synonym:

        """

        Gets a synonym given an id.

        Parameters:
        synonym_id (int) : the id of the synonym we are getting a print item for.

        Returns:
        synonym (Synonym) : the synonym for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for synonym in vocab.testing_material_answer_all:
                if(synonym.synonym_id == synonym_id):
                    return synonym

        raise Searcher.IDNotFoundError(synonym_id)

##--------------------start-of-get_testing_material_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

    @staticmethod
    def get_testing_material_from_id(testing_material_id:int) -> TestingMaterial:

        """

        Gets a testing material given an id.

        Parameters:
        testing_material_id (int) : the id of the testing material we are getting a print item for.

        Returns:
        testing_material (TestingMaterial) : the testing material for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for testing_material in vocab.testing_material_all:
                if(testing_material.testing_material_id == testing_material_id):
                    return testing_material

        raise Searcher.IDNotFoundError(testing_material_id)
    
##--------------------start-of-get_reading_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_reading_from_id(reading_id:int) -> Reading:

        """

        Gets a reading given an id.

        Parameters:
        reading_id (int) : the id of the reading we are getting a print item for.

        Returns:
        reading (Reading) : the reading for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for reading in vocab.readings:
                if(reading.reading_id == reading_id):
                    return reading

        raise Searcher.IDNotFoundError(reading_id)
    
##--------------------start-of-get_incorrect_typo_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_incorrect_typo_from_id(incorrect_typo_id:int) -> IncorrectTypo:

        """

        Gets an incorrect typo given an id.

        Parameters:
        incorrect_typo_id (int) : the id of the incorrect typo we are getting a print item for.

        Returns:
        incorrect_typo (IncorrectTypo) : the incorrect typo for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for incorrect_typo in vocab.incorrect_typos:
                if(incorrect_typo.incorrect_typo_id == incorrect_typo_id):
                    return incorrect_typo

        raise Searcher.IDNotFoundError(incorrect_typo_id)

##--------------------start-of-get_typo_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_typo_from_id(typo_id:int) -> Typo:

        """

        Gets a typo given an id.

        Parameters:
        typo_id (int) : the id of the typo we are getting a print item for.

        Returns:
        typo (Typo) : the typo for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for typo in vocab.typos:
                if(typo.typo_id == typo_id):
                    return typo

        raise Searcher.IDNotFoundError(typo_id)

##--------------------start-of-get_ids_from_japanese()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_ids_from_japanese(term:str) -> typing.List[int]:
    
        """
        
        Gets vocab ids that match a given japanese term.

        Parameters:
        term (str) : the term we are searching with.\n

        Returns:
        vocab_ids (list = int) : matching vocab ids.\n

        """

        vocab_ids = []

        for vocab in LocalHandler.vocab:

            for reading in vocab.readings:
                if(term == reading.furigana_value):
                    vocab_ids.append(vocab.word_id)

            for testing_material in vocab.testing_material_all:
                if(term == testing_material.testing_material_value):
                    vocab_ids.append(vocab.word_id)

            vocab_ids = [int(id) for id in set(vocab_ids)]
            
        return vocab_ids

##--------------------start-of-get_ids_from_alpha_term()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_ids_from_alpha_term(term:str) -> typing.Tuple[typing.List[int], typing.List[int]]:

        """
        
        Gets vocab and synonym ids that match a given term.

        Parameters:
        term (str) : the term we are searching with.

        Returns:
        vocab_ids (list = int) : matching vocab ids.
        synonym_ids (list - int) : matching synonym ids.

        """

        vocab_ids = []
        synonym_ids = []

        for vocab in LocalHandler.vocab:

            ## if term matches romaji or definition 
            for reading in vocab.readings:
                if(term == reading.romaji_value):
                    vocab_ids.append(vocab.word_id)

            for synonym in vocab.testing_material_answer_all:
                if(synonym.synonym_value == term):
                    vocab_ids.append(vocab.word_id)
                    synonym_ids.append(synonym.synonym_id)
            
            
        vocab_ids = [int(id) for id in set(vocab_ids)]
        synonym_ids = [int(id) for id in set(synonym_ids)]

        return vocab_ids, synonym_ids
        
##--------------------start-of-IDNotFoundError------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    class IDNotFoundError(Exception):

        """
    
        Is raised when an id is not found.

        """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        def __init__(self, id_value:int):

            """
            
            Initializes a new IDNotFoundError Exception.

            Parameters:\n
            id_value (int) : The id value that wasn't found.

            """

            self.message = f"ID '{id_value}' not found."