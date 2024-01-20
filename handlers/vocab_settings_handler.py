## built-in modules
import time

## custom modules
from handlers.local_handler import LocalHandler
from handlers.file_handler import FileHandler

from modules.searcher import Searcher
from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from entities.vocab import Vocab as vocab_blueprint 
from entities.synonym import Synonym as synonym_blueprint

class VocabSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings.
    
    """
##--------------------start-of-change_vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_vocab_settings() -> None:

        """

        Controls the pathing for all vocab settings.

        """ 

        Logger.log_action("User is changing vocab settings.")

        vocab_message = "What are you trying to do?\n\n1.Add Entity\n2.Edit Entity\n3.Delete Entity\n4.Search Entity\n"

        print(vocab_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 4, vocab_message)


##--------------------start-of-add_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def add_entity() -> None:

        """

        Adds a vocab entity to the database.

        """ 

        Logger.log_action("User is adding a vocab entity.")

        entity_message = "What type of entity are you trying to add?\n\n1.Add Vocab\n2.Add Synonym to Existing Vocab\n3.Add TestingMaterial to Existing Vocab\n4.Add Reading to Existing Vocab\n5.Add Typo to Existing Vocab\n6.Add IncorrectTypo to Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)


##--------------------start-of-edit_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_entity() -> None:

        """

        Edits a vocab entity in the database.

        """ 

        Logger.log_action("User is editing a vocab entity.")

        entity_message = "What type of entity are you trying to edit?\n\n1.Edit Vocab\n2.Edit Synonym of Existing Vocab\n3.Edit TestingMaterial of Existing Vocab\n4.Edit Reading of Existing Vocab\n5.Edit Typo of Existing Vocab\n6.Edit IncorrectTypo of Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)

##--------------------start-of-delete_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def delete_entity() -> None:

        """

        Deletes a vocab entity from the database.

        """ 

        Logger.log_action("User is deleting a vocab entity.")

        entity_message = "What type of entity are you trying to delete?\n\n1.Delete Vocab\n2.Delete Synonym of Existing Vocab\n3.Delete TestingMaterial of Existing Vocab\n4.Delete Reading of Existing Vocab\n5.Delete Typo of Existing Vocab\n6.Delete IncorrectTypo of Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)