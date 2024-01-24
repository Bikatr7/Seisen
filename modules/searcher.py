## built-in libraries
import typing

## custom modules
from modules.toolkit import Toolkit

from entities.vocab import Vocab
from entities.testing_material import TestingMaterial
from entities.synonym import Synonym

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
        
        mini_testing_material_print = [str(testing_material.testing_material_value) for testing_material in target_vocab.testing_material_all]
        mini_reading_print = [str(reading.romaji_value) + "/" + str(reading.furigana_value) for reading in target_vocab.readings]
        mini_synonym_print = [str(synonym.synonym_id) for synonym in target_vocab.testing_material_answer_all]


        print_item = (
            f"---------------------------------\n"
            f"ID: {target_vocab.word_id}\n"
            f"Incorrect Guesses: {target_vocab.incorrect_count}\n"
            f"Correct Guesses: {target_vocab.correct_count}\n"
            f"Testing Material ID(S) : {mini_testing_material_print}\n"
            f"Testing Material Value(s): {[testing_material.testing_material_value for testing_material in target_vocab.testing_material_all]}\n"
            f"Reading ID(S): {mini_reading_print}\n"
            f"Reading Value(s): {[str(reading.romaji_value) + '/' + str(reading.furigana_value) for reading in target_vocab.readings]}\n"
            f"Synonym ID(S): {mini_synonym_print}\n"
            f"Synonym Values(s): {[synonym.synonym_value for synonym in target_vocab.testing_material_answer_all]}\n"
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
        
        print_item = (
            f"---------------------------------\n"
            f"Synonym: {target_synonym.synonym_value}\n"
            f"Synonym ID: {target_synonym.synonym_id}\n"
            f"VOCAB: {target_vocab.testing_material_all}\n"
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
                f"VOCAB ID {synonym.word_id}\n"
                f"---------------------------------\n"
            )

            print_items.append(print_item)

        return print_items

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