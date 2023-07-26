## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## custom modules

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from modules.localHandler import localHandler

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

    def get_term_from_id(self, local_handler:localHandler, id:int):

        """
        
        Gets a vocab term given an id.\n

        Parameters:\n
        self (object - searcher) : the searcher object.\n
        local_handler (object - localHandler) : the localHandler we are searching in.\n
        id (int) : the id for the term we are searching for.\n

        Returns:\n
        term (str) : the term if found, otherwise "-1".\n

        """
        pass

##--------------------start-of-get_id_from_term()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_id_from_term(self, local_handler:localHandler, term:str):

        """
        
        Gets a vocab id given an verb.\n

        Parameters:\n
        self (object - searcher) : the searcher object.\n
        local_handler (object - localHandler) : the localHandler we are searching in.\n
        tern (str) : the term for the id we are searching for.\n 

        Returns:\n
        id (int) : the id if found, otherwise -1.\n


        """
        pass