## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import msvcrt

## custom modules
from modules import util

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from modules.localHandler import localHandler

##--------------------start-of-IDNotFoundError------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class IDNotFoundError(Exception):

    """
    
    Is raised when an id is not found.\n

    """


##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, id_value:int):

        """
        
        Initializes a new IDNotFoundError Exception.\n

        Parameters:\n
        id_value (int) : The id value that wasn't found.\n
        None.\n

        Returns:\n
        None.\n

        """

        self.message = f"ID '{id_value}' not found."

##--------------------start-of-searcher------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class searcher:

    '''

    The search class is used to search for things in localHandler.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        """
        
        Initializes a new searcher object.\n

        Parameters:\n
        inc_local_handler (object - localHandler) : the local handler.\n
        None.\n

        Returns:\n
        None.\n

        """

##--------------------start-of-get_term_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_print_item_from_id(self, local_handler:localHandler, vocab_id:int):

        """
        
        Gets a print item for a vocab given an id.\n

        Parameters:\n
        self (object - searcher) : the searcher object.\n
        local_handler (object - localHandler) : the localHandler object.\n
        vocab_id (int) : the id of the vocab we are getting a print item for.\n

        Returns:\n
        print_item (str) : the print item for the id.\n
        
        """
            
        target_vocab = None

        for vocab in local_handler.vocab:
            if(vocab.word_id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise IDNotFoundError(vocab_id)

        print_item = (
            f"\n---------------------------------\n"
            f"Vocab: {target_vocab.testing_material}\n"
            f"Romaji: {target_vocab.romaji}\n"
            f"Furigana: {target_vocab.furigana}\n"
            f"Definition: {target_vocab.testing_material_answer_main}\n"
            f"Incorrect Guesses: {target_vocab.incorrect_count}\n"
            f"Correct Guesses: {target_vocab.correct_count}\n"
            f"ID: {target_vocab.word_id}\n"
            f"---------------------------------"
        )

        return print_item

##--------------------start-of-get_term_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_term_from_id(self, local_handler:localHandler, vocab_id:int):

        """
        
        Gets a vocab term given an id.\n

        Parameters:\n
        self (object - searcher) : the searcher object.\n
        local_handler (object - localHandler) : the localHandler we are searching in.\n
        vocab_id (int) : the id for the term we are searching for.\n

        Returns:\n
        term (str) : the term if found, otherwise "-1".\n

        """

        term = "-1"
        
        for vocab in local_handler.vocab:
            if(vocab.word_id == vocab_id):
                term = vocab.testing_material

        return term
    
##--------------------start-of-get_id_from_term()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_id_from_term(self, local_handler:localHandler, term:str):

        """
        
        Gets a vocab id given an verb.\n

        Parameters:\n
        self (object - searcher) : the searcher object.\n
        local_handler (object - localHandler) : the localHandler we are searching in.\n
        tern (str) : the term for the id we are searching for.\n 

        Returns:\n
        final_id (int) : the id if found, otherwise -1.\n


        """

        matching_ids = []

        id_print_message = ""

        final_id = -1

        for vocab in local_handler.vocab:
            if(vocab.testing_material == term):
                matching_ids.append(vocab.word_id)

        if(len(matching_ids) == 0):
            return final_id
        elif(len(matching_ids) == 1):
            final_id = matching_ids[0]
            return final_id
        
        for id in matching_ids:
            id_print_message += self.get_print_item_from_id(local_handler, id)

        id_print_message += "\n\nWhich vocab are you looking for? (Enter position 1-" + str(len(matching_ids)) + ")"

        target_index = int(util.input_check(4, str(msvcrt.getch().decode()), len(matching_ids), id_print_message)) - 1

        final_id = matching_ids[target_index]

        return final_id
        
