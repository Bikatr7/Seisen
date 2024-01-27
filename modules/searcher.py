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
            if(vocab.id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise Searcher.IDNotFoundError(vocab_id)
        
        mini_testing_material_id_print = [str(testing_material.id) for testing_material in target_vocab.testing_material]
        mini_testing_material_value_print = [str(testing_material.value) for testing_material in target_vocab.testing_material]
        
        mini_reading_id_print = [str(reading.id) for reading in target_vocab.readings]
        mini_reading_values_print = [str(reading.romaji) + "/" + str(reading.furigana) for reading in target_vocab.readings]

        mini_id_print = [str(synonym.id) for synonym in target_vocab.answers]
        mini_value_print = [str(synonym.value) for synonym in target_vocab.answers]

        print_item = (
            f"---------------------------------\n"
            f"ID: {target_vocab.id}\n"
            f"Incorrect Guesses: {target_vocab.incorrect_count}\n"
            f"Correct Guesses: {target_vocab.correct_count}\n"
            f"Testing Material ID(S) : {mini_testing_material_id_print}\n"
            f"Testing Material Value(s): {mini_testing_material_value_print}\n"
            f"Reading ID(S): {mini_reading_id_print}\n"
            f"Reading Value(s): {mini_reading_values_print}\n"
            f"Synonym ID(S): {mini_id_print}\n"
            f"Synonym Values(s): {mini_value_print}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_synonym_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_synonym_print_item_from_id(id:int) -> str:

        """
        
        Gets a print item for a synonym given a synonym id.

        Parameters:
        id (int) : The id of the synonym we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.\n
        
        """
        
        target_vocab = None
        target_synonym = None

        for vocab in LocalHandler.vocab:
            for synonym in vocab.answers:
                if(synonym.id == id):
                    target_synonym = synonym
                    target_vocab = vocab

        if(target_synonym == None or target_vocab == None):
            raise Searcher.IDNotFoundError(id)
        
        mini_testing_material_value_print = [str(testing_material.value) for testing_material in target_vocab.testing_material]
        mini_testing_material_id_print = [str(testing_material.id) for testing_material in target_vocab.testing_material]

        print_item = (
            f"---------------------------------\n"
            f"Synonym: {target_synonym.value}\n"
            f"Synonym ID: {target_synonym.id}\n"
            f"VOCAB Testing Material: {mini_testing_material_value_print}\n"
            f"VOCAB Testing Material ID(s): {mini_testing_material_id_print}\n"
            f"VOCAB ID: {target_synonym.id}\n"
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
            if(vocab.id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise Searcher.IDNotFoundError(vocab_id)
        
        for synonym in target_vocab.answers:

            print_item = (
                f"---------------------------------\n"
                f"Synonym: {synonym.value}\n"
                f"Synonym ID: {synonym.id}\n"
                f"VOCAB: {target_vocab.testing_material}\n"
                f"VOCAB ID {synonym.id}\n"
                f"---------------------------------\n"
            )

            print_items.append(print_item)

        return print_items
    
##--------------------start-of-get_testing_material_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_testing_material_print_item_from_id(id:int) -> str:

        """
        
        Gets a print item for a testing material given a testing material id.

        Parameters:
        id (int) : the id of the testing material we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
        
        target_vocab = None
        target_testing_material = None

        for vocab in LocalHandler.vocab:
            for testing_material in vocab.testing_material:
                if(testing_material.id == id):
                    target_testing_material = testing_material
                    target_vocab = vocab

        if(target_testing_material == None or target_vocab == None):
            raise Searcher.IDNotFoundError(id)
        
        mini_id_print = [str(synonym.id) for synonym in target_vocab.answers]
        mini_value_print = [str(synonym.value) for synonym in target_vocab.answers]

        print_item = (
            f"---------------------------------\n"
            f"Testing Material: {target_testing_material.value}\n"
            f"Testing Material ID: {target_testing_material.id}\n"
            f"VOCAB Synonym(s): {mini_value_print}\n"
            f"VOCAB Synonym ID(s): {mini_id_print}\n"
            f"VOCAB ID: {target_testing_material.id}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_reading_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_reading_print_item_from_id(id:int) -> str:

        """
        
        Gets a print item for a reading given a reading id.

        Parameters:
        id (int) : the id of the reading we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
        
        target_vocab = None
        target_reading = None

        for vocab in LocalHandler.vocab:
            for reading in vocab.readings:
                if(reading.id == id):
                    target_reading = reading
                    target_vocab = vocab

        if(target_reading == None or target_vocab == None):
            raise Searcher.IDNotFoundError(id)
        
        print_item = (
            f"---------------------------------\n"
            f"Romaji: {target_reading.romaji}\n"
            f"Furigana: {target_reading.furigana}\n"
            f"Reading ID: {target_reading.id}\n"
            f"VOCAB ID: {target_reading.id}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_incorrect_typo_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_incorrect_typo_print_item_from_id(id:int) -> str:

        """
        
        Gets a print item for an incorrect typo given an incorrect typo id.

        Parameters:
        id (int) : the id of the incorrect typo we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
        
        target_vocab = None
        target_incorrect_typo = None

        for vocab in LocalHandler.vocab:
            for incorrect_typo in vocab.incorrect_typos:
                if(incorrect_typo.id == id):
                    target_incorrect_typo = incorrect_typo
                    target_vocab = vocab

        if(target_incorrect_typo == None or target_vocab == None):
            raise Searcher.IDNotFoundError(id)
        
        mini_testing_material_id_print = [str(testing_material.id) for testing_material in target_vocab.testing_material]
        mini_testing_material_value_print = [str(testing_material.value) for testing_material in target_vocab.testing_material]
        
        print_item = (
            f"---------------------------------\n"
            f"Incorrect Typo: {target_incorrect_typo.value}\n"
            f"Incorrect Typo ID: {target_incorrect_typo.id}\n"
            f"VOCAB Testing Material ID(s): {mini_testing_material_id_print}\n"
            f"VOCAB Testing Material Value(s): {mini_testing_material_value_print}\n"
            f"VOCAB ID: {target_incorrect_typo.id}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_typo_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_typo_print_item_from_id(id:int) -> str:
            
        """
        
        Gets a print item for a typo given a typo id.

        Parameters:
        id (int) : the id of the typo we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
        
        target_vocab = None
        target_typo = None

        for vocab in LocalHandler.vocab:
            for typo in vocab.typos:
                if(typo.id == id):
                    target_typo = typo
                    target_vocab = vocab

        if(target_typo == None or target_vocab == None):
            raise Searcher.IDNotFoundError(id)
        
        mini_testing_material_id_print = [str(testing_material.id) for testing_material in target_vocab.testing_material]
        mini_testing_material_value_print = [str(testing_material.value) for testing_material in target_vocab.testing_material]
        
        print_item = (
            f"---------------------------------\n"
            f"Typo: {target_typo.value}\n"
            f"Typo ID: {target_typo.id}\n"
            f"VOCAB Testing Material ID(s): {mini_testing_material_id_print}\n"
            f"VOCAB Testing Material Value(s): {mini_testing_material_value_print}\n"
            f"VOCAB ID: {target_typo.id}\n"
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
            if(vocab.id == vocab_id):
                return vocab

        raise Searcher.IDNotFoundError(vocab_id)
    
##--------------------start-of-get_overlying_vocab_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_overlying_vocab_from_attribute_id(id:int, attribute_type:typing.Literal["synonym", "testing_material", "reading", "incorrect_typo", "typo"]) -> Vocab:

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
                for synonym in vocab.answers:
                    if(synonym.id == id):
                        return vocab
                    
            elif(attribute_type == "testing_material"):
                for testing_material in vocab.testing_material:
                    if(testing_material.id == id):
                        return vocab
                    
            elif(attribute_type == "reading"):
                for reading in vocab.readings:
                    if(reading.id == id):
                        return vocab
                    
            elif(attribute_type == "incorrect_typo"):
                for incorrect_typo in vocab.incorrect_typos:
                    if(incorrect_typo.id == id):
                        return vocab
                    
            elif(attribute_type == "typo"):
                for typo in vocab.typos:
                    if(typo.id == id):
                        return vocab

        raise Searcher.IDNotFoundError(id)
    
##--------------------start-of-get_synonym_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_synonym_from_id(id:int) -> Synonym:

        """

        Gets a synonym given an id.

        Parameters:
        id (int) : the id of the synonym we are getting a print item for.

        Returns:
        synonym (Synonym) : the synonym for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for synonym in vocab.answers:
                if(synonym.id == id):
                    return synonym

        raise Searcher.IDNotFoundError(id)

##--------------------start-of-get_testing_material_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

    @staticmethod
    def get_testing_material_from_id(id:int) -> TestingMaterial:

        """

        Gets a testing material given an id.

        Parameters:
        id (int) : the id of the testing material we are getting a print item for.

        Returns:
        testing_material (TestingMaterial) : the testing material for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for testing_material in vocab.testing_material:
                if(testing_material.id == id):
                    return testing_material

        raise Searcher.IDNotFoundError(id)
    
##--------------------start-of-get_reading_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_reading_from_id(id:int) -> Reading:

        """

        Gets a reading given an id.

        Parameters:
        id (int) : the id of the reading we are getting a print item for.

        Returns:
        reading (Reading) : the reading for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for reading in vocab.readings:
                if(reading.id == id):
                    return reading

        raise Searcher.IDNotFoundError(id)
    
##--------------------start-of-get_incorrect_typo_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_incorrect_typo_from_id(id:int) -> IncorrectTypo:

        """

        Gets an incorrect typo given an id.

        Parameters:
        id (int) : the id of the incorrect typo we are getting a print item for.

        Returns:
        incorrect_typo (IncorrectTypo) : the incorrect typo for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for incorrect_typo in vocab.incorrect_typos:
                if(incorrect_typo.id == id):
                    return incorrect_typo

        raise Searcher.IDNotFoundError(id)

##--------------------start-of-get_typo_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_typo_from_id(id:int) -> Typo:

        """

        Gets a typo given an id.

        Parameters:
        id (int) : the id of the typo we are getting a print item for.

        Returns:
        typo (Typo) : the typo for the id.

        Raises:
        IDNotFoundError : if the id is not found.
        
        """

        for vocab in LocalHandler.vocab:
            for typo in vocab.typos:
                if(typo.id == id):
                    return typo

        raise Searcher.IDNotFoundError(id)
    
##--------------------start-of-perform_search_by_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def perform_search_by_id(id:int) -> None:

        """
        
        Performs a search by id.

        Parameters:
        id (int) : the id we are searching for.

        """

        ## Define the match types and their corresponding methods
        match_types = [
            ("vocab", Searcher.get_vocab_from_id, Searcher.get_vocab_print_item_from_id),
            ("synonym", Searcher.get_synonym_from_id, Searcher.get_synonym_print_item_from_id),
            ("testing_material", Searcher.get_testing_material_from_id, Searcher.get_testing_material_print_item_from_id),
            ("reading", Searcher.get_reading_from_id, Searcher.get_reading_print_item_from_id),
            ("typo", Searcher.get_typo_from_id, Searcher.get_typo_print_item_from_id),
            ("incorrect_typo", Searcher.get_incorrect_typo_from_id, Searcher.get_incorrect_typo_print_item_from_id)
        ]

        # Initialize the match list and the confirm message list
        match_list = [None] * len(match_types)
        confirm_message_list = ["", "Press any key to see matching synonyms.", "Press any key to see matching testing materials.", "Press any key to see matching readings.", "Press any key to see matching typos.", "Press any key to see matching incorrect typos."]

        # Try to get a match for each type
        for i, (match_type, get_from_id, get_print_item_from_id) in enumerate(match_types):
            try:
                match_list[i] = get_from_id(id)
            except Searcher.IDNotFoundError:
                pass

        ## Print the matches, do not a confirm message for the first match
        for i, match in enumerate(match_list):
            if(match is not None):
                if(i != 0):
                    print("\n" + confirm_message_list[i])
                    Toolkit.pause_console("")
                    Toolkit.clear_console()
                    
                print(match_types[i][2](match.id))
            
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